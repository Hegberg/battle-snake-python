from app.common import get_location_from_direction
from app.common import get_directions
from app.common import check_if_path_in_between_walls
from app.common import get_straight_path_directions_to_border
from app.common import determine_if__snake_growing
from app.common import get_shortest_direction_to_border

from app.a_star import AStar
from app.a_star import init_astar_with_custom_snake

from app.survive import flood_fill_recursive

import copy

#TODO
#if path too tail too long, longer than own body size???
#or wraps around my own body or something
#than just head to snake general direction
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
                #print("Attack Path is before wall check: " + str(path))
                single_lane = check_if_path_in_between_walls(data, aStar, path, walls)
                if (single_lane):
                    #print("Attack Path is between walls, ignore it: " + str(path))
                    path = None

            if (path != None and (shortest_path == None or len(path) < len(shortest_path))):
                shortest_path = path
                snake_following_name = str(data['board']['snakes'][i]['name'])

    if (shortest_path != None):
        chase_directions = get_directions(data['you']['body'][0]['x'],data['you']['body'][0]['y'], 
                                    shortest_path[1][0], shortest_path[1][1])

        print("Path to chasing snake " + snake_following_name + " head direction = " + str(chase_directions) + " on path: " + str(shortest_path))

        return chase_directions

    #TODO
    #if no path to their head, but are only 1 other snake and still larger than them, go to cutoff
    #find their exit path, and cutoff exit instead of going for food
    # 1 1 1 1 - > 0 0 0
    # 1 1 1 1 1 1 1 0 0
    # 2 2 2 2 2 2 0 0 0
    # 2 2 - > 0 0 0 0 0

    #either need to follow own tail if they can't get out, to prevent them from getting out
    #or find where they can get out and create wall
    
    #if only 1 other snake
    if (len(data['board']['snakes']) > 2):
        print("No path to chasing opposing snakes heads")
        return chase_directions

    opposing_snake = -1
    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] != data['you']['id']):
            opposing_snake = i
            break

    print("Creating wall to block in snake")
    wall_in_directions = create_wall(data, aStar, walls, opposing_snake, survival_directions)

    if (len(wall_in_directions) > 0):
        chase_directions = wall_in_directions
        print("Path to wall in snake " + snake_following_name + " head direction = " + str(chase_directions) + " on path: " + str(shortest_path))
        return chase_directions

    print("No path to chasing opposing snakes heads")

    return chase_directions

def create_wall(data, aStar, walls, opposing_snake, survival_directions):
    #block head
    #find path to head
    #find last space adjacent to my body
    #find space in path including that spot or before that is not in between walls
    #from that space, create a path to closest border to wall off snake
    block_head_directions = block_head(data, aStar, walls, opposing_snake, survival_directions)

    if (block_head_directions != None and len(block_head_directions) > 0):
        print("Blocking off head of opponent in directions: " + str(block_head_directions))
        return block_head_directions

    #fill in wall
    #find path to any part of snake body
    #find last space adjacent to my body
    block_body_directions = block_body(data, aStar, walls, opposing_snake, survival_directions)

    if (block_body_directions != None and len(block_body_directions) > 0):
        print("Blocking off body of opponent in directions: " + str(block_body_directions))
        return block_body_directions

    #if no paths to it's body, follow tail
    #only follow tail, if they don't have path to my head (ie can't cut me off as I'm following my tail)
    #for eating, find food closest to body loop, eat that if hungry
    maintian_block_directions = maintian_block(data, aStar, walls, opposing_snake, survival_directions)

    #TODO
    #choose path that keeps snake closest to cuting off opposing snake, to keep more area control, even if can't cutoff

    if (maintian_block_directions != None and len(maintian_block_directions) > 0):
        print("Maintaining blocking off opponent in directions: " + str(maintian_block_directions))
        return maintian_block_directions

    return []

def block_head(data, aStar, walls, opposing_snake, survival_directions):
    shortest_path = None
    path = None

    #get areas it's head can move to, try to move to closest one
    possible_moves = get_opposing_snake_survival_moves(data, walls, opposing_snake)

    for j in range(len(possible_moves)):
        aStar.reset_grid((possible_moves[j][0], possible_moves[j][1]))
        path = aStar.solve()

        if (path != None and (shortest_path == None or len(path) < len(shortest_path))):
            shortest_path = path

    if (shortest_path == None):
        print("No viable path to opposing snake " + str(data['board']['snakes'][opposing_snake]['name']) + " head to block")
        return None

    print("Shortest path to opposing snakes " + str(data['board']['snakes'][opposing_snake]['name']) + "head on path: " + str(shortest_path))

    self_body = []

    for i in range(0, len(data['you']['body'])):
        self_body.append((data['you']['body'][i]['x'], data['you']['body'][i]['y']))

    #find last space adjacent to my body
    body_adjacent_index = -1
    for i in range(len(shortest_path) - 1, 0, -1):
        if ((shortest_path[i][0] + 1, shortest_path[i][1]) in self_body):
            body_adjacent_index = i
            break
        if ((shortest_path[i][0] - 1, shortest_path[i][1]) in self_body):
            body_adjacent_index = i
            break
        if ((shortest_path[i][0], shortest_path[i][1] + 1) in self_body):
            body_adjacent_index = i
            break
        if ((shortest_path[i][0], shortest_path[i][1] - 1) in self_body):
            body_adjacent_index = i
            break

    #from last place in path, find closest border to go to to block off
    print("Space blocking off head from: " + str(shortest_path[body_adjacent_index]))

    #TODO
    #shortest path isn't necessarily the one that blocks off snake, use one that is relative to snake directions as well
    direction_to_border, path_to_border = get_shortest_direction_to_border(data, walls, shortest_path[body_adjacent_index])

    if (direction_to_border == None or path_to_border == None):
        print("No path to head of snake and too border")
        return None

    #get flood fill of now blocked off area from perspective of opponent snake, if small enough, than do cutoff
    #otherwise, don't block

    if (not (flood_fill_snake(data, walls, aStar, opposing_snake, path_to_border))):
        #small enough area to trap snake
        block_head_directions = get_directions(data['you']['body'][0]['x'], data['you']['body'][0]['y'], shortest_path[0][0], shortest_path[0][1]) 
        print("Blocking path: " + str(shortest_path) + " and to border path: " + str(path_to_border) + " in direction: " + str(block_head_directions) + " will trap opposing snake")
        return block_head_directions

    #TODO
    #even if floodfill too large, still keep them stuck in smaller area

    print("Unable to block off head in 1v1")
    return None

def block_body(data, aStar, walls, opposing_snake, survival_directions):
    return []

def maintian_block(data, aStar, walls, opposing_snake, survival_directions):
    return []

def attack_collide(data, walls, survival_directions):
    #if can collide with snake and win, do it
    collide_directions = get_collide_directions(data, walls, survival_directions)

    if (len(collide_directions) > 0):
        return collide_directions

    return []

#TODO
#if snake like 1 1 1 1 1 1
#              0 0 0 1 1 1
#              2 2 2 2 2 2
#              0 0 0 2 2 1
#recognize the snake is on the border and i can still cut him off by going the relative direction to cut him off
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

            if (path != None and (shortest_path == None or len(path) < len(shortest_path))):
                shortest_path = path
                snake_following_name = str(data['board']['snakes'][i]['name'])
                snake_cutoff_index = i

    if (shortest_path == None):
        print("Attack Cutoff Shortest Path to head: " + str(shortest_path) + " of snake: " + str(snake_following_name))
        return cutoff_directions

    #for all border directions, see if one cuts off closest snake
    for i in range(len(border_directions)):

        too_much_free_space = rectangle_check(data, walls, border_directions[i], border_paths, snake_cutoff_index, i)

        #too much free space, don't cutoff
        if (too_much_free_space):
            print("Too much free space not cutting off in direction: " + str(border_directions[i]))
            continue
        
        #see if path to tail is loger than cutoff path
        snake_head_to_tail_path, snake_path_to_you_tail = get_snake_path_to_tail(data, walls, border_paths, snake_cutoff_index, i)

        #if path longer than cutoff path, proceed to cutoff
        if (snake_head_to_tail_path != None and len(snake_head_to_tail_path) < len(border_paths[i])):
            print("Path to tail to short for effective cutoff in direction: " + str(border_directions[i]))
            continue

        if (snake_head_to_tail_path != None and len(snake_head_to_tail_path) >= len(border_paths[i])):
            print("Path for snake to escape long enough to justify cutoff in direction: " + str(border_directions[i]))
            cutoff_directions.append(border_directions[i])
            continue

        #if both paths don't exist, flood fill area too see if small enough (< body size) to trap snake
        if (snake_head_to_tail_path == None and snake_path_to_you_tail == None):
            if (flood_fill_snake(data, walls, aStar, snake_cutoff_index, border_paths[i])):
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
def rectangle_check(data, walls, border_direction, border_paths, snake_cutoff_index, i):
    #create rectangle to snake, and border past usng cutoff wall

    snake_relative_directions = get_directions(data['you']['body'][0]['x'], data['you']['body'][0]['y'], data['board']['snakes'][snake_cutoff_index]['body'][0]['x'], data['board']['snakes'][snake_cutoff_index]['body'][0]['y'])
    #border going up or down, create rectangle to right or left, depending on where snake is

    #print("For border direction: " + str(border_direction) + " snake relative directions: " + str(snake_relative_directions))
    #print("border_path: " str(border_paths[i]))

    #if ((border_direction == 'up' and 'up' in snake_relative_directions) or (border_direction == 'down' and 'down' in snake_relative_directions)):
    #below bugs out in case of snake not actually in cutoff area, but algorithm assuming it is, so cuts off nothing
    if ((border_direction == 'up') or (border_direction == 'down')):

        for direction in snake_relative_directions:
            #create box to left of cutoff
            free_space = 0
            blocked_off_cells = []
            
            #start at head for free space calculations
            j_start = data['you']['body'][0]['y']
            #j_start = border_paths[i][0][1]
            j_stop = border_paths[i][len(border_paths[i]) - 1][1]
            if (border_direction == 'up'):
                j_stop -= 1
                step = -1
            elif (border_direction == 'down'):
                j_stop += 1
                step = 1

            if (direction == 'left'):
                #along vertical line of cutoff wall
                for j in range(j_start, j_stop, step):
                    #from left border to cutoff wall (horizontal line)
                    for k in range(0, border_paths[i][0][0]):
                        if (not ((k,j) in walls)):
                            free_space += 1
                            blocked_off_cells.append((k,j))

                print("Direction left border up/down")
                """
                for j in range(j_start, j_stop, step):
                    for k in range(0, border_paths[i][0][0]):
                        if (not ((k,j) in walls)):
                            print("0 " , end='')
                        else:
                            print("1 " , end='')
                    print(" ")
                """

            #create box to right of cutoff
            elif (direction == 'right'):
                #along vertical line of cutoff wall
                for j in range(j_start, j_stop, step):
                    #from left border to cutoff wall (horizontal line)
                    for k in range(border_paths[i][0][0] + 1, data['board']['width']): # +1 to avoid using border wall in free space calc
                        if (not ((k,j) in walls)):
                            free_space += 1
                            blocked_off_cells.append((k,j))

                print("Direction right border up/down")
                """
                for j in range(j_start, j_stop, step):
                    for k in range(border_paths[i][0][0] + 1, data['board']['width']):
                        if (not ((k,j) in walls)):
                            print("0 " , end='')
                        else:
                            print("1 " , end='')
                    print(" ")
                """

            #else not right or left so go to start of loop
            else:
                continue

            print("Free space calculated: " + str(free_space) + " in direction: " + str(direction) + " border_direction: " + border_direction)
            print("Border path used: " + str(border_paths[i]))
            #if too much free space, don't cutoff
            if (free_space >= len(data['board']['snakes'][snake_cutoff_index]['body'])):
                return True

            #else, if path for other snake to first border cutoff cell, passes through blocked off cells, cutoff, otherwise don't
            return (not can_cutoff_head_and_tail_check(data, border_paths, blocked_off_cells, snake_cutoff_index, i))

        #else direction == left or right, and in such case return true, meaning too much free space
        return True

    #if ((border_direction == 'left' and 'left' in snake_relative_directions) or (border_direction == 'right' and 'right' in snake_relative_directions)):
    #below bugs out in case of snake not actually in cutoff area, but algorithm assuming it is, so cuts off nothing
    if ((border_direction == 'left') or (border_direction == 'right')):

        for direction in snake_relative_directions:
            #create box to up of cutoff
            free_space = 0
            blocked_off_cells = []

            #start at head for free space calculations
            j_start = data['you']['body'][0]['x']
            #j_start = border_paths[i][0][0]
            j_stop = border_paths[i][len(border_paths[i]) - 1][0]
            if (border_direction == 'left'):
                j_stop -= 1
                step = -1
            elif (border_direction == 'right'):
                j_stop += 1
                step = 1

            if (direction == 'up'):
                #along horizontal line of cutoff wall
                for j in range(j_start, j_stop, step):
                    #from up border to cutoff wall (vertical line)
                    for k in range(0, border_paths[i][0][1]):
                        if (not ((j,k) in walls)):
                            free_space += 1
                            blocked_off_cells.append((k,j))

                print("Direction up border left/right")
                """
                for k in range(0, border_paths[i][0][1]):
                    for j in range(j_start, j_stop, step):
                        if (not ((j,k) in walls)):
                            print("0 " , end='')
                        else:
                            print("1 " , end='')
                    print(" ")
                """
            #create box to down of cutoff
            elif (direction == 'down'):
                #along horizontal line of cutoff wall
                for j in range(j_start, j_stop, step):
                    #from left border to cutoff wall (vertical line)
                    for k in range(border_paths[i][0][1] + 1, data['board']['height']): # +1 to avoid using border wall in free space calc
                        if (not ((j,k) in walls)):
                            free_space += 1
                            blocked_off_cells.append((k,j))

                print("Direction down border left/right")
                """
                for k in range(border_paths[i][0][1] + 1, data['board']['height']):
                    for j in range(j_start, j_stop, step):
                        if (not ((j,k) in walls)):
                            print("0 " , end='')
                        else:
                            print("1 " , end='')
                    print(" ")
                """
            
            #else not up or down so go to start of loop
            else:
                continue

            print("Free space calculated: " + str(free_space) + " in direction: " + str(direction) + " border_direction: " + border_direction)
            print("Border path used: " + str(border_paths[i]))
            #if too much free space, don't cutoff
            if (free_space >= len(data['board']['snakes'][snake_cutoff_index]['body'])):
                return True

            #else, if path for other snake to first border cutoff cell, passes through blocked off cells, cutoff, otherwise don't
            return (not can_cutoff_head_and_tail_check(data, border_paths, blocked_off_cells, snake_cutoff_index, i))

        #else direction == left or right, and in such case return true, meaning too much free space
        return True

    return True

def can_cutoff_head_and_tail_check(data, border_paths, blocked_off_cells, snake_cutoff_index, i):
    #else, if path for other snake to first border cutoff cell, passes through blocked off cells, cutoff, otherwise don't
    snake_body = copy.deepcopy(data['board']['snakes'][snake_cutoff_index]['body'][:])
    snake_goal =  (border_paths[i][0][0], border_paths[i][0][1])
    if (snake_goal == (snake_body[0]['x'], snake_body[0]['y'])):
        print("Snake goal same as snake head: " + str(snake_goal))
        return False

    custom_aStar, walls = init_astar_with_custom_snake(data, snake_body, data['board']['snakes'][snake_cutoff_index]['id'], snake_goal)
    path = custom_aStar.solve()

    print("Cutoff path to start of cutoff: " + str(path))

    if (path != None):
        can_cutoff = False
        for s in range(len(path)):
            #path to get out of cutoff goes through cutoff area, so cutoff
            if ((path[s][0], path[s][1]) in blocked_off_cells):
                can_cutoff = True
                break

        print("Cutoff: " + str(can_cutoff))

        #if path doesn't go through cutoff space, but snake is right beside border path (so in space, but path not in space since head on edge of space)
        #check if larger, if so see if have less than or equal distance, if so, cutoff
        if (not can_cutoff and len(path) == 2 and (len(data['you']['body']) > len(data['board']['snakes'][snake_cutoff_index]['body']))):
            can_cutoff = True
            print("Cutoff beside: " + str(can_cutoff))

        #if can cutoff, check if with cutoff path, have path too my tail, if so, don't cut off
        if (can_cutoff):
            snake_goal = (data['you']['body'][len(data['you']['body']) - 1]['x'], data['you']['body'][len(data['you']['body']) - 1]['y'])
            custom_aStar, walls = init_astar_with_custom_snake(data, snake_body, data['board']['snakes'][snake_cutoff_index]['id'], snake_goal, border_paths[i])
            path = custom_aStar.solve()

            print("Cutoff path to my tail: " + str(path))

            if (path != None):
                print("Cutoff path to my tail valid: " + str(path))
                can_cutoff = False

            #check if can also reach its own tail, if it can, don't cutoff, otherwise, do
            if (can_cutoff):
                snake_goal = (data['board']['snakes'][snake_cutoff_index]['body'][len(data['board']['snakes'][snake_cutoff_index]['body']) - 1]['x'],
                    data['board']['snakes'][snake_cutoff_index]['body'][len(data['board']['snakes'][snake_cutoff_index]['body']) - 1]['y'])
                custom_aStar.reset_grid(snake_goal)
                path = custom_aStar.solve()

                if (path != None):
                    print("Cutoff path to snakes own tail valid: " + str(path))
                    can_cutoff = False


        #inverse reply, since if can cutoff, means there is not enough room for snake to survive
        #so return false
        return can_cutoff

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
                                    data['you']['body'][len(data['you']['body']) - 2]['y']))
            break
    

    cutoff_walls = walls[:]
    #for cuttoff path corresponding to direction, add path to walls
    for j in range(len(border_paths[border_paths_index])):
        cutoff_walls.append(border_paths[border_paths_index][j])


    #init astar with new board
    new_aStar = AStar()
    x = data['board']['snakes'][snake_cutoff_index]['body'][0]['x']
    y = data['board']['snakes'][snake_cutoff_index]['body'][0]['y']
    current_position = (x, y)
    gx = data['board']['snakes'][snake_cutoff_index]['body'][snake_len - 1]['x']
    gy = data['board']['snakes'][snake_cutoff_index]['body'][snake_len - 1]['y']
    goal = (gx,gy)
    new_aStar.init_grid(data['board']['width'], data['board']['height'], cutoff_walls, current_position, goal)

    #if goal is start, ie first turn, return none path
    if ((x,y) == (gx,gy) or data['turn'] == 0):
        snake_head_to_tail_path = None
        snake_head_to_you_tail_path = None
        return snake_head_to_tail_path, snake_head_to_you_tail_path

    snake_head_to_tail_path = new_aStar.solve()

    #try getting path to my tail
    new_aStar.reset_grid((data['you']['body'][len(data['you']['body']) - 1]['x'], data['you']['body'][len(data['you']['body']) - 1]['y']))
    snake_head_to_you_tail_path = new_aStar.solve()

    return snake_head_to_tail_path, snake_head_to_you_tail_path

#return true if large enough area for it too survive, false otherwise
def flood_fill_snake(data, walls, aStar, snake_index, cutoff_path):
    x = data['board']['snakes'][snake_index]['body'][0]['x']
    y = data['board']['snakes'][snake_index]['body'][0]['y']

    flood_directions = []
    flood_walls = walls[:]

    matrix = []
    for j in range(data['board']['width']):
        row = []
        for k in range(data['board']['height']):
            row.append(0)
        matrix.append(row)

    for location in cutoff_path:
        flood_walls.append(location)
            
    for j in range(len(flood_walls)):
        #access by column, row
        matrix[flood_walls[j][0]][flood_walls[j][1]] = 1

    #set head of snake to not a wall so flood fill calculates correctly
    matrix[x][y] = 0

    #-1 not 0 to accomidate for removing head from walls 
    flood_size =  -1
    flood_matrix = flood_fill_recursive(matrix, x, y, data, walls, aStar)
    for j in range(len(matrix)):
        for k in range(len(matrix[j])):
            if (matrix[j][k] == 2):
                flood_size += 1
    print("Cutoff flood size: ", flood_size)
    """
    for j in range(len(flood_matrix[0])):
        print("Flood Matrix Cutoff: ", end='')
        for k in range(len(flood_matrix)):
            print(str(flood_matrix[k][j]) + " " , end='')
        print(" ")
    """
    #to accomidate for not adding head to flood walls
    flood_size -= 1

    if (flood_size > len(data['board']['snakes'][snake_index]['body'])):
        #large enough area found
        return True

    #Did not find a large enough area
    return False