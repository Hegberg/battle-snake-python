from app.common import get_directions
from app.common import determine_if_snake_growing
from app.common import get_location_from_direction
from app.common import check_if_location_in_between_walls
from app.common import path_from_closest_snake_head_to_location
from app.common import get_distance_between_points
from app.common import get_large_opponent_move_walls
from app.common import get_small_opponent_move_walls
from app.common import DEBUG_LOGS

from app.a_star import init_astar
from app.a_star import init_astar_with_custom_snake

from app.longest_path import find_longest_path

import copy

def survival_choices(data, walls, aStar):
    directions = check_bounds(data)

    if (DEBUG_LOGS):
        print("Check Bounds After: ", directions)
    directions = check_self_collisions(directions, data)
    if (DEBUG_LOGS):
        print("Check Self After: ", directions)
    directions = check_snake_collisions(directions, data)
    if (DEBUG_LOGS):
        print("Check Snakes After: ", directions)

    return directions

def check_bounds(data):
    directions = ["up", "down", "left", "right"]
    #check if space below us is on board
    if (data['board']['height'] - data['you']['body'][0]['y'] <= 1):
        directions.remove("down")

    #check if not on upper row
    if (data['you']['body'][0]['y'] <= 0):
        directions.remove("up")

    #check if not on right wall
    if (data['board']['width'] - data['you']['body'][0]['x'] <= 1):
        directions.remove("right")
    
    #check if not on left wall
    if (data['you']['body'][0]['x'] <= 0):
        directions.remove("left")
    
    return directions

def check_self_collisions(directions, data):
    x = data['you']['body'][0]['x']
    y = data['you']['body'][0]['y']

    for i in range(1, len(data['you']['body'])):
        #if own tail, ignore
        if (i == len(data['you']['body']) - 1):
            continue

        collision = check_beside_self(x,y,data['you']['body'][i]['x'],data['you']['body'][i]['y'])
        if (collision != 0 and collision in directions):
            directions.remove(collision)
            #print("Head x y: " + str(x) + " " + str(y) + " body x y: " + str(data['you']['body'][i]['x']) + " " + str(data['you']['body'][i]['y']))

    return directions

def check_snake_collisions(directions, data):
    x = data['you']['body'][0]['x']
    y = data['you']['body'][0]['y']

    if (DEBUG_LOGS):
        print("Amount of opponents: ", len(data['board']['snakes']))
    
    for j in range(len(data['board']['snakes'])):
        #if snake is self, ignore
        if (data['board']['snakes'][j]['id'] == data['you']['id']):
            continue

        for i in range(len(data['board']['snakes'][j]['body'])):
            
            #if tail, don't count as wall
            #need to check if eating, will do later
            if (i == len(data['board']['snakes'][j]['body']) - 1):
                continue
            
            collision = check_beside_self(x,y,data['board']['snakes'][j]['body'][i]['x'],data['board']['snakes'][j]['body'][i]['y'])
            if (collision != 0 and collision in directions):
                directions.remove(collision)

    return directions

def check_beside_self(x,y,x2,y2):
    #to the direct left
    if (x - x2 == 1 and y - y2 == 0):
        return 'left'

    #to the direct right
    if (x - x2 == -1 and y - y2 == 0):
        return 'right'

    #to the direct top
    if (x - x2 == 0 and y - y2 == 1):
        return 'up'

    #to the direct bottom
    if (x - x2 == 0 and y - y2 == -1):
        return 'down'

    #nothing directly beside
    return 0

def flood_fill(data, walls, available_directions, aStar):
   
    x = data['you']['body'][0]['x']
    y = data['you']['body'][0]['y']

    #add head as wall
    walls.append((x,y))

    big_move_walls = get_large_opponent_move_walls(data, aStar, walls)
    small_move_walls = get_small_opponent_move_walls(data, aStar, walls)

    flood_directions = []
    single_lane_flood_directions = []
    flood_areas = []
    single_lane_flood_areas = []
    flood_matrixs = []

    for i in range(len(available_directions)):
        matrix = []
        tile_order_queue = []
        for j in range(len(big_move_walls)):
            tile_order_queue.append((big_move_walls[j][0],big_move_walls[j][1],3))

        for j in range(data['board']['width']):
            row = []
            for k in range(data['board']['height']):
                row.append(0)
            matrix.append(row)

        for j in range(len(walls)):
            #access by column, row
            matrix[walls[j][0]][walls[j][1]] = 1

        if (available_directions[i] == 'up'):
            tile_order_queue.append((x, y-1))
            for j in range(len(small_move_walls)):
                tile_order_queue.append((small_move_walls[j][0],small_move_walls[j][1],3))
            flood_matrix = flood_fill_recursive(matrix, data, walls, aStar, tile_order_queue)
            flood_size, flood_area = get_flood_size(matrix)

            flood_directions.append(('up', flood_size, False))
            flood_areas.append(flood_area)
            flood_matrixs.append(flood_matrix)

        elif (available_directions[i] == 'down'):
            tile_order_queue.append((x, y+1))
            for j in range(len(small_move_walls)):
                tile_order_queue.append((small_move_walls[j][0],small_move_walls[j][1],3))
            flood_matrix = flood_fill_recursive(matrix, data, walls, aStar, tile_order_queue)
            flood_size, flood_area = get_flood_size(matrix)

            flood_directions.append(('down', flood_size, False))
            flood_areas.append(flood_area)
            flood_matrixs.append(flood_matrix)
        
        elif (available_directions[i] == 'left'):
            tile_order_queue.append((x-1, y))
            for j in range(len(small_move_walls)):
                tile_order_queue.append((small_move_walls[j][0],small_move_walls[j][1],3))
            flood_matrix = flood_fill_recursive(matrix, data, walls, aStar, tile_order_queue)
            flood_size, flood_area = get_flood_size(matrix)

            flood_directions.append(('left', flood_size, False))
            flood_areas.append(flood_area)
            flood_matrixs.append(flood_matrix)

        elif (available_directions[i] == 'right'):
            tile_order_queue.append((x+1, y))
            for j in range(len(small_move_walls)):
                tile_order_queue.append((small_move_walls[j][0],small_move_walls[j][1],3))
            flood_matrix = flood_fill_recursive(matrix, data, walls, aStar, tile_order_queue)
            flood_size, flood_area = get_flood_size(matrix)

            flood_directions.append(('right', flood_size, False))
            flood_areas.append(flood_area)
            flood_matrixs.append(flood_matrix)

        if (DEBUG_LOGS and True):
            print("Flood Area: " + str(available_directions[i]) + " size: " + str(len(flood_areas[i])))

            x_print = 0
            y_print = 0
            while (True):
                while (x_print < len(flood_matrix)):
                    print(flood_matrix[x_print][y_print], end=' ')
                    x_print += 1
                y_print += 1
                x_print = 0
                print('')
                if (y_print >= len(flood_matrix[x_print - 1])):
                    break

            #print(flood_area)


    walls.remove((x,y))

    #check to include any single lane flood fill in flood directions

    largest_flood = ['', 0]
    large_flood_area = []
    largest_flood_single_lane = False
    final_directions = []

    tail_directions = []

    if (DEBUG_LOGS):
        print("Flood directions before longest path: " + str(flood_directions))

    #for flood directions, go through small sizes and see if can survive in
    for i in range(len(flood_directions)):
        if (DEBUG_LOGS):
            print("Flood Direction: " + str(flood_directions[i]))

        if (flood_directions[i][1] > len(data['you']['body'])):
            #append direction, and single lane
            final_directions.append((flood_directions[i][0], flood_directions[i][2]))
        
        #If snake goes to area smaller than itself, start moving through and occuping space and see if space opens up, or path to tail open
        else:
            longest_path, closest_tail = find_longest_path(data, get_location_from_direction(flood_directions[i][0],x,y), flood_areas[i])
            if (DEBUG_LOGS):
                print("longest chosen path: " + str(longest_path))

            #traverse longest path, and see if path to tail opens up during path traversal, if so, area is viable to go through
            if (len(longest_path) > 0):
                extra_walls = []
                #print (flood_matrixs[i])
                for j in range(len(flood_matrixs[i])):
                    for k in range(len(flood_matrixs[i][j])):
                        if (flood_matrixs[i][j][k] == 3):
                            extra_walls.append((j,k))
                #print("extra walls: " + str(extra_walls))
                path_availabe, single_lane = traverse_longest_path(data, longest_path, closest_tail, extra_walls)
                if (path_availabe):
                    final_directions.append((flood_directions[i][0], single_lane))
                    tail_directions.append((flood_directions[i][0], single_lane))
                    if (DEBUG_LOGS):
                        print("flood directions after longest path: " + str(final_directions))
        
        #check if largest flood area is less than body size, if so, go with direction that has longest path, 
        #not just direction with largest flood that may or may not have same flood size as other direction
        if (flood_directions[i][1] > largest_flood[1]):
            largest_flood[0] = flood_directions[i][0]
            largest_flood[1] = flood_directions[i][1]
            large_flood_area = flood_areas[i]
            largest_flood_single_lane = flood_directions[i][2]
        #same size, choose flood with longer path
        elif (flood_directions[i][1] == largest_flood[1] and flood_directions[i][1] > 0 and flood_directions[i][1] < len(data['you']['body'])):
            longest_path, closest_tail = find_longest_path(data, get_location_from_direction(flood_directions[i][0],x,y), flood_areas[i])
            large_longest_path, large_closest_tail = find_longest_path(data, get_location_from_direction(largest_flood[0],x,y), large_flood_area)

            if (DEBUG_LOGS):
                print("Finding longest path")

            #if path longer, or path the same and distance to tail shorter
            if ((len(longest_path) > len(large_longest_path)) or 
                ((len(longest_path) == len(large_longest_path) and len(longest_path) > 0 and len(large_longest_path) > 0)
                and (get_distance_between_points(longest_path[len(longest_path) - 1], closest_tail) < 
                get_distance_between_points(large_longest_path[len(large_longest_path) - 1], large_closest_tail)))):
                largest_flood[0] = flood_directions[i][0]
                largest_flood[1] = flood_directions[i][1]
                large_flood_area = flood_areas[i]
                largest_flood_single_lane = flood_directions[i][2]
            #if largest area path does not exist but smaller area does
            elif (len(large_longest_path) == 0 and len(longest_path) > 0):
                largest_flood[0] = flood_directions[i][0]
                largest_flood[1] = flood_directions[i][1]
                large_flood_area = flood_areas[i]
                largest_flood_single_lane = flood_directions[i][2]

    if (DEBUG_LOGS):
        print("Large flood area: " + str(len(large_flood_area)) + ' data:' + str(large_flood_area))

    if (len(final_directions) == 0):
        #if largest flood was actually replaced with a direction
        if (largest_flood[0] != ''):
            final_directions.append((largest_flood[0], largest_flood_single_lane))
        #no large enough area found
        #return directions with lane, and if floodable
        return final_directions, False, tail_directions, large_flood_area

    #Found a large enough area
    #return directions with lane, and if floodable
    return final_directions, True, tail_directions, large_flood_area

#tile_order_queue((x,y),(x,y),(x,y)...)
#or for multi snakes
#tile_order_queue((x,y,number_fill),(x,y,number_fill),(x,y,number_fill)...)
#1 for wall, 2 for current snake, 3 for opposing
def flood_fill_recursive(matrix, data, walls, aStar, tile_order_queue):
    while (len(tile_order_queue) > 0):
        matrix = flood_fill_tile_check(matrix, data, walls, aStar, tile_order_queue)

    return matrix

def flood_fill_tile_check(matrix, data, walls, aStar, tile_order_queue):
    x = tile_order_queue[0][0]
    y = tile_order_queue[0][1]

    #if item in queue has unique number grab it, otherwise assume default
    if (len(tile_order_queue[0]) > 2):
        number_fill = tile_order_queue[0][2]
    else:
        number_fill = 2

    tile_order_queue.pop(0)

    if (matrix[x][y] == 0):
        """
        #don't check if location is between walls, since this is literally who can get their fastest
        if (number_fill == 2):
            between_walls = check_if_location_in_between_walls(data, aStar, walls, (x,y))
            #if between walls, check if opposing snake is close enough to cut off from that point, if so, remove option from floodfill
            if(between_walls):
                return matrix
        """

        matrix[x][y] = number_fill

        if (x > 0):
            tile_order_queue.append((x-1, y, number_fill))
        if (x < len(matrix[y]) - 1):
            tile_order_queue.append((x+1, y, number_fill))
        if (y > 0):
            tile_order_queue.append((x, y-1, number_fill))
        if (y < len(matrix) - 1):
            tile_order_queue.append((x, y+1, number_fill))

        return matrix
    return matrix


def get_flood_size(matrix):
    flood_size = 0
    flood_area = {}

    for j in range(len(matrix)):
        for k in range(len(matrix[j])):
            if (matrix[j][k] == 2):
                flood_size += 1
                flood_area[j,k] = 0

    return flood_size, flood_area

def path_single_lane_check(data, aStar, walls, path):
    anywhere_between_walls = False
    for i in range(len(path)):
        between_walls = check_if_location_in_between_walls(data, aStar, walls, path[i])
        if(between_walls):
            anywhere_between_walls = True
            break

    return anywhere_between_walls

#TODO
#if space between head and tail
#remove body that gets in way to tail from walls in path if body would move out of way once head
#arrvies at that location
def find_own_tail_path(aStar, walls, data, growing, valid_move_tiles):
    #reset grid to have tail space as goal
    tail_x = data['you']['body'][len(data['you']['body']) - 1]['x']
    tail_y = data['you']['body'][len(data['you']['body']) - 1]['y']

    #if head and tail are the same space, ie starting turn
    if ((tail_x == data['you']['body'][0]['x']) and (tail_y == data['you']['body'][0]['y'])):
        directions = []
        if (DEBUG_LOGS):
            print("Tail and head are on the same tile: " + str(tail_x) + " " + str(tail_y))
        return directions

    #if growing, need to find path to space before tail and solid tail
    if (growing):
        new_aStar, new_walls = init_astar(data, False, True)
        new_aStar.set_ending_for_init_grid((tail_x, tail_y))
        path = new_aStar.solve()
    else:
        aStar.reset_grid((tail_x, tail_y))
        path = aStar.solve()

    if (DEBUG_LOGS):
        print("Path to tail = " + str(path))

    if (path != None and check_if_path_goes_through_valid_survival_tiles(path, valid_move_tiles)):
        directions = get_directions(data['you']['body'][0]['x'],data['you']['body'][0]['y'], 
                                    path[1][0], path[1][1])

        if (growing):
            single_lane = path_single_lane_check(data, aStar, new_walls, path)
        else:
            single_lane = path_single_lane_check(data, aStar, walls, path)

        for i in range(len(directions)):
            directions[i] = (directions[i], single_lane)

        if (DEBUG_LOGS):
            print("Path to tail direction = " + str(directions))

        return directions

    if (DEBUG_LOGS):
        print("No path to tail")

    return [(None, False)]

def find_other_snake_tail_path(data, aStar, walls, valid_move_tiles):
    shortest_path = None
    snake_following_name = ''
    short_walls = walls
    #reset grid to have tail space as goal
    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self

        tail_x = data['board']['snakes'][i]['body'][len(data['board']['snakes'][i]['body']) - 1]['x']
        tail_y = data['board']['snakes'][i]['body'][len(data['board']['snakes'][i]['body']) - 1]['y']

        #if head and tail are the same space, ie starting turn
        if ((tail_x == data['board']['snakes'][i]['body'][0]['x']) and (tail_y == data['board']['snakes'][i]['body'][0]['y'])):
            directions = []
            if (DEBUG_LOGS):
                print("Tail and head of snake " + str(data['board']['snakes'][i]['name']) + " are on the same tile: " + str(tail_x) + " " + str(tail_y))
            return directions

        growing = determine_if_snake_growing(data, i)

        #if growing, need to find path to space before tail and solid tail
        if (growing):
            new_aStar, new_walls = init_astar(data, False, False, i)
            new_aStar.set_ending_for_init_grid((tail_x, tail_y))
            path = new_aStar.solve()
        else:
            aStar.reset_grid((tail_x, tail_y))
            path = aStar.solve()

        if (path != None and (shortest_path == None or len(path) < len(shortest_path))
            and check_if_path_goes_through_valid_survival_tiles(path, valid_move_tiles)):
            shortest_path = path
            snake_following_name = str(data['board']['snakes'][i]['name'])

            if (growing):
                short_walls = new_walls
            else:
                short_walls = walls


    if (shortest_path != None):
        directions = get_directions(data['you']['body'][0]['x'],data['you']['body'][0]['y'], 
                                    shortest_path[1][0], shortest_path[1][1])


        single_lane = path_single_lane_check(data, aStar, short_walls, shortest_path)

        for i in range(len(directions)):
            directions[i] = (directions[i], single_lane)

        if (DEBUG_LOGS):
            print("Path to snake " + snake_following_name + " tail direction = " + str(directions))

        return directions

    if (DEBUG_LOGS):
        print("No path to snake opposing snakes tails")

    return [(None, False)]

#check path against flood tiles that use possible enemy movement
def check_if_path_goes_through_valid_survival_tiles(path, valid_move_tiles):
    #ignore tail of path, since that is snake tail and not part of valid tiles
    for i in range(len(path) - 1):
        #ignore head of path, since that is snake head and not part of valid tiles
        if (i == 0):
            continue
        if (path[i] not in valid_move_tiles):
            return False

    return True


def traverse_longest_path(data, longest_path, closest_tail, extra_walls):

    update_own_tail_as_target = False
    tail_x = closest_tail[0]
    tail_y = closest_tail[1]

    #print("Tail: " + str((tail_x, tail_y)))

    #if closest tail is own, target tail is always own tail, otherwise do not change target tail
    if (closest_tail == (data['you']['body'][len(data['you']['body']) - 1]['x'], data['you']['body'][len(data['you']['body']) - 1]['y'])):
        update_own_tail_as_target = True

    snake_body = copy.deepcopy(data['you']['body'][:])

    for i in range(len(longest_path)):

        growing = False
        #check if going over food
        for j in range(len(data['board']['food'])):
            #if picking up food on this square
            if ((data['board']['food'][j]['x'], data['board']['food'][j]['y']) == (longest_path[i][0], longest_path[i][1])):
                growing = True
                break

        if (not growing):

            for j in range(len(snake_body) - 1, 0, - 1):
                snake_body[j]['x'] = snake_body[j - 1]['x']
                snake_body[j]['y'] = snake_body[j - 1]['y']

            snake_body[0]['x'] = longest_path[i][0]
            snake_body[0]['y'] = longest_path[i][1]

        else:
            if (DEBUG_LOGS):
                print(snake_body[0])
            snake_body.insert(0, {'x': longest_path[i][0], 'y': longest_path[i][1]})

        head_x = snake_body[0]['x']
        head_y = snake_body[0]['y']

        #if tail closest, or if new tail posistion is cloasest, make target
        if (update_own_tail_as_target or 
            get_distance_between_points((snake_body[len(snake_body) - 1]['x'], snake_body[len(snake_body) - 1]['y']), (head_x, head_y))):
            tail_x = snake_body[len(snake_body) - 1]['x']
            tail_y = snake_body[len(snake_body) - 1]['y']

        if ((tail_x, tail_y) == (head_x, head_y)):
            if (DEBUG_LOGS):
                print("Path to tail (0 distance) in blocked in area available: " + str((tail_x, tail_y)))
            return True

        custom_aStar, walls = init_astar_with_custom_snake(data, snake_body, data['you']['id'], (tail_x, tail_y), extra_walls)
        path = custom_aStar.solve()

        if (path != None):
            if (DEBUG_LOGS):
                print("Path to tail in blocked in area available: " + str(path))

            between_walls = path_single_lane_check(data, custom_aStar, walls, path)

            #return if path is available, and if it is between walls
            return True, between_walls
        
    #return if path is available, and if it is between walls
    return False, False


def get_distance_between_points(point_1, point_2):
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])