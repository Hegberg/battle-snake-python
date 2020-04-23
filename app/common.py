DEBUG_LOGS = False

def directions1_in_directions2(directions1, directions2):
    directions = []
    if (directions1 != None and len(directions1) > 0):
        #if direction in direction1 not in viable direction, remove option
        for direction in directions1:
            if (direction in directions2):
                directions.append(direction)

        return directions

    return None

def get_directions(x,y,x2,y2):
 
    directions = []

    #to the left
    if (x - x2 > 0):
        directions.append('left')

    #to the right
    elif (x - x2 < 0):
        directions.append('right')

    #to the top
    if (y - y2 > 0):
        directions.append('up')

    #to the bottom
    elif (y - y2 < 0):
        directions.append('down')

    return directions

def get_location_from_direction(direction, x, y):
    if (direction == 'up'):
        return (x,y-1)
    if (direction == 'down'):
        return (x,y+1)
    if (direction == 'left'):
        return (x-1,y)
    if (direction == 'right'):
        return (x+1,y)

    return None

def add_to_dict(x, y, dict, val = 1):
    if (not (x,y) in dict):
        dict[(x,y)] = val
    else:
        dict[(x,y)] += val

#return true if path stuck between 2 walls
def check_if_path_in_between_walls(data, aStar, path, walls):

    snake_walls, border_walls, self_walls = seperate_walls(data,walls)

    for i in range(1, len(path)):

        path_between_walls = check_if_location_pass_between_walls(data, (path[i][0], path[i][1]), snake_walls, border_walls, self_walls)

        if (path_between_walls):
            #path in between 2 opposing walls
            return check_if_cutoff_closer(data, aStar, (path[i][0], path[i][1]))

    return False


def check_if_direction_in_between_walls(data, aStar, walls, direction):
    
    location = get_location_from_direction(direction, data['you']['body'][0]['x'], data['you']['body'][0]['y'])

    snake_walls, border_walls, self_walls = seperate_walls(data,walls)

    if (check_if_location_pass_between_walls(data, location, snake_walls, border_walls, self_walls)):
        return check_if_cutoff_closer(data, aStar, location)

    return False

def check_if_location_in_between_walls(data, aStar, walls, location):
    snake_walls, border_walls, self_walls = seperate_walls(data,walls)

    if (check_if_location_pass_between_walls(data, location, snake_walls, border_walls, self_walls)):
        #if closer, returns true, so inverse to say false, not between walls
        return check_if_cutoff_closer(data, aStar, location)
    return False

#returns true if opponent snake closer
def check_if_cutoff_closer(data, aStar, location):
    short_path, snake_head_loc = path_from_closest_snake_head_to_location(data, aStar, location)

    if ((data['you']['body'][0]['x'], data['you']['body'][0]['y']) == location):
        return False

    aStar.reset_grid_and_start((data['you']['body'][0]['x'], data['you']['body'][0]['y']), location)
    own_path = aStar.solve()

    if (short_path != None and own_path != None):
        #if opposing snake can beat me to cutoff, don't use, + 2 to account for actually escaping cutoff
        if (len(own_path) >= (len(short_path) - 2)):
            return True
        else:
            return False

    elif (short_path != None):
        return True

    return False

def seperate_walls(data, walls):
    snake_walls = walls[:]

    self_walls = []

    for i in range(0, len(data['you']['body'])):
        #remove own body from walls
        #check to make sure not trying to remove tail or growing tail that is not included
        if ((data['you']['body'][i]['x'], data['you']['body'][i]['y']) in snake_walls):
            snake_walls.remove((data['you']['body'][i]['x'], data['you']['body'][i]['y']))

        #ignore start of own body, and tail
        if (i >= 2 and i < len(data['you']['body']) - 1):
            self_walls.append((data['you']['body'][i]['x'], data['you']['body'][i]['y']))

    #add border to walls
    border_walls = []
    for i in range(data['board']['width']):
        border_walls.append((i, -1))
        border_walls.append((i, data['board']['height']))
    
    for i in range(data['board']['height']):
        border_walls.append((-1, i))
        border_walls.append((data['board']['width'], i))

    return snake_walls, border_walls, self_walls

def check_if_location_pass_between_walls(data, location, snake_walls, border_walls, self_walls):

    snake_x_axis_walls = 0
    snake_y_axis_walls = 0
    if ((location[0] + 1, location[1]) in snake_walls):
        snake_x_axis_walls += 1
    if ((location[0] - 1, location[1]) in snake_walls):
        snake_x_axis_walls += 1
    if ((location[0], location[1] + 1) in snake_walls):
        snake_y_axis_walls += 1
    if ((location[0], location[1] - 1) in snake_walls):
        snake_y_axis_walls += 1

    border_x_axis_walls = 0
    border_y_axis_walls = 0
    if ((location[0] + 1, location[1]) in border_walls):
        border_x_axis_walls += 1
    if ((location[0] - 1, location[1]) in border_walls):
        border_x_axis_walls += 1
    if ((location[0], location[1] + 1) in border_walls):
        border_y_axis_walls += 1
    if ((location[0], location[1] - 1) in border_walls):
        border_y_axis_walls += 1

    self_x_axis_walls = 0
    self_y_axis_walls = 0
    if ((location[0] + 1, location[1]) in self_walls):
        self_x_axis_walls += 1
    if ((location[0] - 1, location[1]) in self_walls):
        self_x_axis_walls += 1
    if ((location[0], location[1] + 1) in self_walls):
        self_y_axis_walls += 1
    if ((location[0], location[1] - 1) in self_walls):
        self_y_axis_walls += 1

    """
    if (location[0] == 7 and location[1] == 9):
        print("between_walls check")
        print(self_x_axis_walls)
        print(self_y_axis_walls)
        print(border_x_axis_walls)
        print(border_y_axis_walls)
        print(snake_x_axis_walls)
        print(snake_y_axis_walls)
    """
    #passing between 2 snakes
    if (snake_x_axis_walls >= 2 or snake_y_axis_walls >= 2):
        return True

    #passing between snake and border
    if (snake_x_axis_walls == 1 and border_x_axis_walls == 1) or (snake_y_axis_walls == 1 and border_y_axis_walls == 1):
        return True
    
    #passing between own body and snake
    if (snake_x_axis_walls == 1 and self_x_axis_walls == 1) or (snake_y_axis_walls == 1 and self_y_axis_walls == 1):
        return True

    #passing between self and border ok
    #passing between self and self ok

    return False

def path_from_closest_snake_head_to_location(data, aStar, location):
    shortest_path = None
    snake_head = None

    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self

        p1_x = data['board']['snakes'][i]['body'][0]['x']
        p1_y = data['board']['snakes'][i]['body'][0]['y']

        #goal is current location
        if ((p1_x, p1_y) == location):
            return [location], (p1_x, p1_y)

        #remove head from unreachable cells to allow for aStar to path from opponent head to location
        aStar.reset_grid_and_remove_wall((p1_x, p1_y), location, (p1_x, p1_y))
        path = aStar.solve()
        aStar.add_wall((p1_x, p1_y))

        if (path != None):
            if (shortest_path == None or len(path) < len(shortest_path)):
                shortest_path = path
                snake_head = (p1_x,p1_y)

    return shortest_path, snake_head

def get_distance_between_points(self, point_1, point_2):
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])

def determine_if__snake_growing(data, snake_index):
    if (len(data['board']['snakes'][snake_index]) > 2):
        t1_x = data['board']['snakes'][snake_index]['body'][len(data['board']['snakes'][snake_index]['body']) - 1]['x']
        t1_y = data['board']['snakes'][snake_index]['body'][len(data['board']['snakes'][snake_index]['body']) - 1]['y']
        t2_x = data['board']['snakes'][snake_index]['body'][len(data['board']['snakes'][snake_index]['body']) - 2]['x']
        t2_y = data['board']['snakes'][snake_index]['body'][len(data['board']['snakes'][snake_index]['body']) - 2]['y']
        if (t1_x == t2_x and t1_y == t2_y):
            return True
    return False


def get_previous_direction(data, snake_index):
    if (len(data['board']['snakes'][snake_index]) > 2):
        t1_x = data['board']['snakes'][snake_index]['body'][0]['x']
        t1_y = data['board']['snakes'][snake_index]['body'][0]['y']
        t2_x = data['board']['snakes'][snake_index]['body'][1]['x']
        t2_y = data['board']['snakes'][snake_index]['body'][1]['y']

        directions = get_direction(t1_x, t1_y, t2_x, t2_y)

        #should only be 1 direction
        if (len(directions) == 1):
            return directions[0]

    return None

def get_straight_path_directions_to_border(data, walls, moveable_directions):

    border_directions = []
    straight_paths = []

    for direction in moveable_directions:

        hit_wall = False
        hit_border = False

        straight_path = []
        
        if (direction == 'up'):
            cur_x = data['you']['body'][0]['x']
            cur_y = data['you']['body'][0]['y']
            #moving up, keep checking if in walls
            while (not hit_wall and not hit_border):
                cur_y -= 1
                straight_path.append((cur_x, cur_y))
                if ((cur_x, cur_y) in walls):
                    hit_wall = True
                    straight_path = []
                if (cur_y < 0):
                    hit_border = True
                    straight_path.pop()

            if (hit_border and not hit_wall):
                border_directions.append('up')
            else:
                straight_path = []

        elif (direction == 'down'):
            cur_x = data['you']['body'][0]['x']
            cur_y = data['you']['body'][0]['y']
            #moving down, keep checking if in walls
            while (not hit_wall and not hit_border):
                cur_y += 1
                straight_path.append((cur_x, cur_y))
                if ((cur_x, cur_y) in walls):
                    hit_wall = True
                if (cur_y >= data['board']['height']):
                    hit_border = True
                    straight_path.pop()

            if (hit_border and not hit_wall):
                border_directions.append('down')
            else:
                straight_path = []

        elif (direction == 'left'):
            cur_x = data['you']['body'][0]['x']
            cur_y = data['you']['body'][0]['y']
            #moving left, keep checking if in walls
            while (not hit_wall and not hit_border):
                cur_x -= 1
                straight_path.append((cur_x, cur_y))
                if ((cur_x, cur_y) in walls):
                    hit_wall = True
                if (cur_x < 0):
                    hit_border = True
                    straight_path.pop()

            if (hit_border and not hit_wall):
                border_directions.append('left')
            else:
                straight_path = []

        elif (direction == 'right'):
            cur_x = data['you']['body'][0]['x']
            cur_y = data['you']['body'][0]['y']
            #moving right, keep checking if in walls
            while (not hit_wall and not hit_border):
                cur_x += 1
                straight_path.append((cur_x, cur_y))
                if ((cur_x, cur_y) in walls):
                    hit_wall = True
                if (cur_x >= data['board']['width']):
                    hit_border = True
                    straight_path.pop()

            if (hit_border and not hit_wall):
                border_directions.append('right')
            else:
                straight_path = []

        if (len(straight_path) > 0):
            straight_paths.append(straight_path)

    if (DEBUG_LOGS):
        print("Possible border directions: " + str(border_directions))
        print("Possible border paths: " + str(straight_paths))


    return border_directions, straight_paths

def get_shortest_direction_to_border(data, walls, location):

    border_directions = []

    hit_wall = False
    hit_border = False

    straight_path = []
    straight_paths = []

    cur_x = location[0]
    cur_y = location[1]
    
    #moving up, keep checking if in walls
    while (not hit_wall and not hit_border):
        cur_y -= 1
        straight_path.append((cur_x, cur_y))
        if ((cur_x, cur_y) in walls):
            hit_wall = True
            straight_path = []
        if (cur_y < 0):
            hit_border = True
            straight_path.pop()

    if (hit_border and not hit_wall):
        border_directions.append('up')
        straight_paths.append(straight_path)
        straight_path = []
    else:
        straight_path = []

    cur_x = location[0]
    cur_y = location[1]
    hit_wall = False
    hit_border = False
    #moving down, keep checking if in walls
    while (not hit_wall and not hit_border):
        cur_y += 1
        straight_path.append((cur_x, cur_y))
        if ((cur_x, cur_y) in walls):
            hit_wall = True
        if (cur_y >= data['board']['height']):
            hit_border = True
            straight_path.pop()

    if (hit_border and not hit_wall):
        border_directions.append('down')
        straight_paths.append(straight_path)
        straight_path = []
    else:
        straight_path = []

    cur_x = location[0]
    cur_y = location[1]
    hit_wall = False
    hit_border = False
    #moving left, keep checking if in walls
    while (not hit_wall and not hit_border):
        cur_x -= 1
        straight_path.append((cur_x, cur_y))
        if ((cur_x, cur_y) in walls):
            hit_wall = True
        if (cur_x < 0):
            hit_border = True
            straight_path.pop()

    if (hit_border and not hit_wall):
        border_directions.append('left')
        straight_paths.append(straight_path)
        straight_path = []
    else:
        straight_path = []

    cur_x = location[0]
    cur_y = location[1]
    hit_wall = False
    hit_border = False
    #moving right, keep checking if in walls
    while (not hit_wall and not hit_border):
        cur_x += 1
        straight_path.append((cur_x, cur_y))
        if ((cur_x, cur_y) in walls):
            hit_wall = True
        if (cur_x >= data['board']['width']):
            hit_border = True
            straight_path.pop()

    if (hit_border and not hit_wall):
        border_directions.append('right')
        straight_paths.append(straight_path)
        straight_path = []
    else:
        straight_path = []

    if (DEBUG_LOGS):
        print("Possible block border directions: " + str(border_directions))
        print("Possible block border paths: " + str(straight_paths))

    if (len(straight_paths) == 0):
        return None, None

    short_path = straight_paths[0]
    short_direction = border_directions[0]
    for i in range(1, len(straight_paths)):
        if (len(straight_paths[i]) < len(short_path)):
            short_path = straight_paths[i]
            short_direction = border_directions[i]

    if (DEBUG_LOGS):
        print("Block border direction: " + str(short_direction))
        print("Block border path: " + str(short_path))

    return short_direction, short_path
