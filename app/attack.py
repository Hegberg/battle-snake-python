from app.common import get_location_from_direction
from app.common import get_directions
from app.common import check_if_path_in_between_walls
from app.common import get_straight_path_directions_to_border
from app.common import determine_if__snake_growing

from app.a_star import AStar

from app.survive import flood_fill_recursive

def attack_chase(data, aStar, walls, survival_directions):
    chase_directions = []
    shortest_path = None

    #find shortest path to a opposing snake head
    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self

        path = None

        #get areas it's head can move to, try to move to closest one
        possible_moves = get_opposing_snake_survival_moves(data, walls, i)

        for j in range(len(possible_moves)):
            aStar.reset_grid((possible_moves[j][0], possible_moves[j][1]))
            path = aStar.solve()

            #check if path goes through single lane, if so mark as bad and None
            if (path != None):
                print("Attack Path is before wall check: " + str(path))
                single_lane = check_if_path_in_between_walls(data, path, walls)
                if (single_lane):
                    print("Attack Path is between walls, ignore it: " + str(path))
                    path = None

            if (path != None and (shortest_path == None or len(path) < len(shortest_path))):
                shortest_path = path
                snake_following_name = str(data['board']['snakes'][i]['name'])

    if (shortest_path != None):
        chase_directions = get_directions(data['you']['body'][0]['x'],data['you']['body'][0]['y'], 
                                    shortest_path[1][0], shortest_path[1][1])

        print("Path to chasing snake " + snake_following_name + " head direction = " + str(chase_directions))

        return chase_directions

    print("No path to chasing opposing snakes heads")

    return chase_directions

def attack_collide(data, walls, survival_directions):
    #if can collide with snake and win, do it
    collide_directions = get_collide_directions(data, walls, survival_directions)

    if (len(collide_directions) > 0):
        return collide_directions

    return []

def attack_cutoff(data, aStar, walls, survival_directions):

    cutoff_directions = []

    #if straight path available from me to wall in any direction, and snake in that corner, 
    #check if it will cut them off
    #if so, go in straight line to wall

    #directions that have straight path to wall
    border_directions, border_paths = get_straight_path_directions_to_border(data, walls, survival_directions)

    #if can move to border without hitting a wall, check if this movement will block off an enemy
    if (len(border_directions) == 0):
        return cutoff_directions

    #if path available from my to his head (including small 1 lanes)
    #and
    #if space in rectangle between cutoff area and opposing snake head < size of enemy snakes continue with other checks
    """
    0 1 0 0 2
    0 1 0 2 2
    0 1 0 2 2
    """
    #if path from snakes head to tail, longer than cutoff path
    #or (no path to tail and no path to my tail), and flood fill of area is less than body size
    #do cutoff

    shortest_path = None
    snake_following_name = ''
    snake_cutoff_index = -1

    #for all snakes find closest with valid path to head
    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self


        path = None

        #get areas it's head can move to, try to move to closest one
        possible_moves = get_opposing_snake_survival_moves(data, walls, i)

        for j in range(len(possible_moves)):
            aStar.reset_grid((possible_moves[j][0], possible_moves[j][1]))
            path = aStar.solve()

            #check if path goes through single lane, if so mark as bad and None
            if (path != None):
                print("Attack Cutoff Possible Path check: " + str(path))

            if (path != None and (shortest_path == None or len(path) < len(shortest_path))):
                shortest_path = path
                snake_following_name = str(data['board']['snakes'][i]['name'])
                snake_cutoff_index = i

    if (shortest_path == None):
        print("Attack Cutoff Shortest Path to head: " + str(shortest_path) + " of snake: " + str(snake_following_name))
        return cutoff_directions

    #for all border directions, see if one cuts off closest snake
    for i in range(len(border_directions)):

        too_much_free_space = rectangle_check(data, border_directions[i], border_paths, snake_cutoff_index)

        #too much free space, don't cutoff
        if (too_much_free_space):
            print("Too much free space not cutting off in direction: " + str(border_directions[i]))
            continue
        
        #see if path to tail is loger than cutoff path
        snake_path_to_tail, snake_path_to_you_tail = get_snake_path_to_tail(data, walls, border_paths, snake_cutoff_index, i)

        #if path longer than cutoff path, proceed to cutoff
        if (snake_head_to_tail_path != None and len(snake_head_to_tail_path) < border_paths[i]):
            print("Path to tail to short for effective cutoff in direction: " + str(border_directions[i]))
            continue

        if (snake_head_to_tail_path != None and len(snake_head_to_tail_path) >= border_paths[i]):
            print("Path for snake to escape long enough to justify cutoff in direction: " + str(border_directions[i]))
            cutoff_directions.append(border_directions[i])
            continue

        #if both paths don't exist, flood fill area too see if small enough (< body size) to trap snake
        if (snake_head_to_tail_path == None and snake_path_to_you_tail == None):
            if (flood_fill_snake(data, walls, snake_cutoff_index)):
                print("Too large of area to for snake to survive in, don't cutoff in direction: " + str(border_directions[i]))
                continue

            #cutoff
            print("Too small area for snake to survive in, cutoff in direction: " + str(border_directions[i]))
            cutoff_directions.append(border_directions[i])

    return cutoff_directions


    #get distance of opposing snakes head from my body to border

    #create path to cutoff (go to wall)
    #count path now as wall, and see if opposing snake can path plan out of area

def get_collide_directions(data, walls, survival_directions):
    #get locations you can move to
    you_locations = []
    for i in range(len(survival_directions)):
        you_locations.append(get_location_from_direction(survival_directions[i], data['you']['body'][0]['x'], data['you']['body'][0]['y']))

    collide_directions =[]

    #if moving puts me in collision zone of opposing snake, and im larger, move into collision area
    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self
        
        if (len(data['you']['body']) <= len(data['board']['snakes'][i]['body'])):
            continue #skip snake if you smaller or same size

        #get areas it's head can move to, if can move to one of them, do it
        possible_moves = get_opposing_snake_survival_moves(data, walls, i)

        for j in range(len(possible_moves)):
            if (possible_moves[j] in you_locations):
                directions = get_directions(data['you']['body'][0]['x'],data['you']['body'][0]['y'],
                                possible_moves[j][0],possible_moves[j][1])
                for direction in directions:
                    if (not (direction in collide_directions)):
                        collide_directions.append(direction)

    print("Collision directions and larger: " + str(collide_directions))
    return collide_directions

#return list of possible x,y locations for opposing snake to move to
def get_opposing_snake_survival_moves(data, walls, snake_index):

    head_x = data['board']['snakes'][snake_index]['body'][0]['x']
    head_y = data['board']['snakes'][snake_index]['body'][0]['y']

    possible_moves = []

    additional_walls = walls[:]

    #add border to walls
    for i in range(data['board']['width']):
        additional_walls.append((i, -1))
        additional_walls.append((i, data['board']['height']))
    
    for i in range(data['board']['height']):
        additional_walls.append((-1, i))
        additional_walls.append((data['board']['width'], i))

    if (not ((head_x + 1, head_y) in additional_walls)):
        possible_moves.append((head_x + 1, head_y))
    if (not ((head_x - 1, head_y) in additional_walls)):
        possible_moves.append((head_x - 1, head_y))

    if (not ((head_x, head_y + 1) in additional_walls)):
        possible_moves.append((head_x, head_y + 1))
    if (not ((head_x, head_y - 1) in additional_walls)):
        possible_moves.append((head_x, head_y - 1))

    return possible_moves

#return True on too much space, False otherwise
def rectangle_check(data, border_direction, border_paths, snake_cutoff_index):
    #create rectangle to snake, and border past usng cutoff wall
        
    snake_relative_directions = get_directions(data['you']['body'][0]['x'], data['you']['body'][0]['y'], data['board']['snakes'][snake_cutoff_index]['body'][0]['x'], data['board']['snakes'][snake_cutoff_index]['body'][0]['y'])
    #border going up or down, create rectangle to right or left, depending on where snake is
    if (border_direction == 'up' or border_direction == 'down'):

        for direction in snake_relative_directions:
            #create box to left of cutoff
            free_space = 0
            if (direction == 'left'):
                #along vertical line of cutoff wall
                for j in range(border_paths[i][0][1], border_paths[i][len(border_paths[i]) - 1][1]):
                    #from left border to cutoff wall (horizontal line)
                    for k in range(0, border_paths[i][0][0]):
                        if (not ((k,j) in walls)):
                            free_space += 1
            #create box to right of cutoff
            if (direction == 'right'):
                #along vertical line of cutoff wall
                for j in range(border_paths[i][0][1], border_paths[i][len(border_paths[i]) - 1][1]):
                    #from left border to cutoff wall (horizontal line)
                    for k in range(border_paths[i][0][0] + 1, data['board']['width']): # +1 to avoid using border wall in free space calc
                        if (not ((k,j) in walls)):
                            free_space += 1

            print("Free space calculated: " + str(free_space))
            #if too much free space, don't cutoff
            if (free_space >= len(data['board']['snakes'][snake_index]['body'])):
                return True

            return False

    if (border_directions[i] == 'left' or border_directions[i] == 'right'):

        for direction in snake_relative_directions:
            #create box to up of cutoff
            free_space = 0
            if (direction == 'up'):
                #along horizontal line of cutoff wall
                for j in range(border_paths[i][0][0], border_paths[i][len(border_paths[i]) - 1][0]):
                    #from up border to cutoff wall (vertical line)
                    for k in range(0, border_paths[i][0][1]):
                        if (not ((j,k) in walls)):
                            free_space += 1
            #create box to down of cutoff
            if (direction == 'down'):
                #along horizontal line of cutoff wall
                for j in range(border_paths[i][0][0], border_paths[i][len(border_paths[i]) - 1][0]):
                    #from left border to cutoff wall (vertical line)
                    for k in range(border_paths[i][0][1] + 1, data['board']['height']): # +1 to avoid using border wall in free space calc
                        if (not ((j,k) in walls)):
                            free_space += 1

            print("Free space calculated: " + str(free_space))
            #if too much free space, don't cutoff
            if (free_space >= len(data['board']['snakes'][snake_index]['body'])):
                return True

            return False

    return False

def get_snake_path_to_tail(data, walls, border_paths, snake_cutoff_index, border_paths_index):
    #get new path planned for opposing snake assuming cutoff has been made, 
    #see if path to tail is loger than cutoff path
    cutoff_walls = walls[:]

    snake_len = len(data['board']['snakes'][snake_cutoff_index]['body'])

    #remove extra tail spaces of snake and me if growing
    if (determine_if__snake_growing(data, snake_cutoff_index)):
        cutoff_walls.remove((data['board']['snakes'][snake_cutoff_index]['body'][snake_len - 2]['x'],
                            data['board']['snakes'][snake_cutoff_index]['body'][snake_len - 2]['y']))

    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            if (determine_if__snake_growing(data, i)):
                cutoff_walls.remove((data['you']['body'][len(data['you']['body']) - 2]['x'], 
                                    data['you']['body'][len(data['you']['body']) - 2]['x']))
            break
    

    cutoff_walls = walls[:]
    #for cuttoff path corresponding to direction, add path to walls
    for j in range(len(border_paths[border_paths_index])):
        cutoff_walls.append(border_paths[border_paths_index][j])


    #init astar with new board
    new_aStar - AStar()
    x = data['board']['snakes'][snake_cutoff_index]['body'][0]['x']
    y = data['board']['snakes'][snake_cutoff_index]['body'][0]['y']
    current_position = (x, y)
    gx = data['board']['snakes'][snake_cutoff_index]['body'][snake_len - 1]['x']
    gy = data['board']['snakes'][snake_cutoff_index]['body'][snake_len - 1]['y']
    goal = (gx,gy)
    new_aStar.init_grid(data['board']['width'], data['board']['height'], cutoff_walls, current_position, goal)

    snake_head_to_tail_path = new_aStar.solve()

    #try getting path to my tail
    new_aStar.reset_grid((data['you']['body'][len(data['you']['body']) - 1]['x'], data['you']['body'][len(data['you']['body']) - 1]['y']))
    snake_head_to_you_tail_path = new_aStar.solve()

    return snake_head_to_tail_path, snake_head_to_you_tail_path

#return true if large enough area for it too survive, false otherwise
def flood_fill_snake(data, walls, snake_index):
    x = data['board']['snakes'][snake_index]['body'][0]['x']
    y = data['board']['snakes'][snake_index]['body'][0]['y']

    flood_directions = []

    matrix = []
    for j in range(data['board']['width']):
        row = []
        for k in range(data['board']['height']):
            row.append(0)
        matrix.append(row)
            
    for j in range(len(walls)):
        #access by column, row
        matrix[walls[j][0]][walls[j][1]] = 1

    flood_size = 0
    flood_matrix = flood_fill_recursive(matrix, x, y)
    for j in range(len(matrix)):
        for k in range(len(matrix[j])):
            if (matrix[j][k] == 2):
                flood_size += 1
    print("Cutoff flood size: ", flood_size)
    for k in range(len(flood_matrix)):
        print("Flood Matrix Cutoff " + str(i) + ": " + str(flood_matrix[k]))
    
    #to accomidate for not adding head to flood walls
    flood_size -= 1

    if (flood_size > len(data['board']['snakes'][snake_index]['body'])):
        #large enough area found
        return True

    #Did not find a large enough area
    return False