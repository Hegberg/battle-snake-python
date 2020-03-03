from app.common import get_location_from_direction
from app.common import get_direction

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
            single_lane = check_if_path_in_between_walls(data, path, walls)
            if (single_lane):
                print("Attack Path is between walls, ignore it: " + str(path))
                path = None

        if (path != None and (shortest_path == None or len(path) < len(shortest_path))):
            shortest_path = path
            snake_following_name = str(data['board']['snakes'][i]['name'])

    if (shortest_path != None):
        chase_directions = get_direction(data['you']['body'][0]['x'],data['you']['body'][0]['y'], 
                                    path[1][0], path[1][1])

        print("Path to chasing snake " + snake_following_name + " head direction = " + str(chase_directions))

        return chase_directions

    print("No path to chasing opposing snakes heads")

    return chase_directions

def attack_cutoff(data, aStar, walls, survival_directions):
    #if can collide with snake and win, do it
    collide_directions = get_collide_directions(data, walls, survival_directions)

    if (len(collide_directions) > 0):
        return collide_directions

    cutoff_directions = []

    #get distance of opposing snakes head from my body to border

    #create path to cutoff (go to wall)
    #count path now as wall, and see if opposing snake can path plan out of area

    return cutoff_directions

def get_collide_directions(data, walls, survival_directions):
    #get locations you can move to
    you_locations = []
    for i in range(len(survival_directions)):
        you_locations.append(get_location_from_direction(survival_directions[i]))

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
            if (possible_moves[i] in you_locations):
                direction = get_direction(data['you']['body'][0]['x'],data['you']['body'][0]['y'],
                                possible_moves[i][0],possible_moves[i][1])
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