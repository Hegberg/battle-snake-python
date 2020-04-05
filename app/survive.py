from app.common import get_directions
from app.common import determine_if__snake_growing
from app.a_star import init_astar
from app.longest_path import find_longest_path

def survival_choices(data, walls, aStar):
    directions = check_bounds(data)

    print("Check Bounds After: ", directions)
    directions = check_self_collisions(directions, data)
    print("Check Self After: ", directions)
    directions = check_snake_collisions(directions, data)
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

def flood_fill(data, walls, available_directions):
   
    x = data['you']['body'][0]['x']
    y = data['you']['body'][0]['y']

    #add head as wall
    walls.append((x,y))


    flood_directions = []
    flood_areas = {}

    for i in range(len(available_directions)):
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
        flood_area = {}
        if (available_directions[i] == 'up'):
            flood_matrix = flood_fill_recursive(matrix, x, y-1)
            for j in range(len(matrix)):
                for k in range(len(matrix[j])):
                    if (matrix[j][k] == 2):
                        flood_size += 1
                        flood_area[j,k] = 0
            print("Up flood size: ", flood_size)
            """
            for k in range(len(flood_matrix)):
                print("Flood Matrix Up " + str(i) + ": " + str(flood_matrix[k]))
            for j in range(len(flood_matrix[0])):
                print("Flood Matrix Up: ", end='')
                for k in range(len(flood_matrix)):
                    print(str(flood_matrix[k][j]) + " " , end='')
                print(" ")
            """
            flood_directions.append(('up',flood_size))
            flood_areas.append(flood_area)

        elif (available_directions[i] == 'down'):
            flood_matrix = flood_fill_recursive(matrix, x, y+1)
            for j in range(len(matrix)):
                for k in range(len(matrix[j])):
                    if (matrix[j][k] == 2):
                        flood_size += 1
                        flood_area[j,k] = 0
            print("Down flood size: ", flood_size)
            """
            for k in range(len(flood_matrix)):
                print("Flood Matrix Down " + str(i) + ": " + str(flood_matrix[k]))
            for j in range(len(flood_matrix[0])):
                print("Flood Matrix Down: ", end='')
                for k in range(len(flood_matrix)):
                    print(str(flood_matrix[k][j]) + " " , end='')
                print(" ")
            """
            flood_directions.append(('down',flood_size))
            flood_areas.append(flood_area)
        
        elif (available_directions[i] == 'left'):
            flood_matrix = flood_fill_recursive(matrix, x-1, y)
            for j in range(len(matrix)):
                for k in range(len(matrix[j])):
                    if (matrix[j][k] == 2):
                        flood_size += 1
                        flood_area[j,k] = 0
            print("Left flood size: ", flood_size)
            """
            for k in range(len(flood_matrix)):
                print("Flood Matrix Left " + str(i) + ": " + str(flood_matrix[k]))
            for j in range(len(flood_matrix[0])):
                print("Flood Matrix Left: ", end='')
                for k in range(len(flood_matrix)):
                    print(str(flood_matrix[k][j]) + " " , end='')
                print(" ")
            """
            flood_directions.append(('left',flood_size))
            flood_areas.append(flood_area)

        elif (available_directions[i] == 'right'):
            flood_matrix = flood_fill_recursive(matrix, x+1, y)
            for j in range(len(matrix)):
                for k in range(len(matrix[j])):
                    if (matrix[j][k] == 2):
                        flood_size += 1
                        flood_area[j,k] = 0
            print("Right flood size: ", flood_size)
            """
            for k in range(len(flood_matrix)):
                print("Flood Matrix Right " + str(i) + ": " + str(flood_matrix[k]))
            for j in range(len(flood_matrix[0])):
                print("Flood Matrix Right: ", end='')
                for k in range(len(flood_matrix)):
                    print(str(flood_matrix[k][j]) + " " , end='')
                print(" ")
            """
            flood_directions.append(('right',flood_size))
            flood_areas.append(flood_area)
    
    largest_flood = ['', 0]
    final_directions = []
    for i in range(len(flood_directions)):
        if (flood_directions[i][1] > len(data['you']['body'])):
            final_directions.append(flood_directions[i][0])
        #TODO
        #If snake goes to area smaller than itself, start moving through and occuping space and see if space opens up, or path to tail open
        else:
            longest_path = find_longest_path(data, get_location_from_direction(flood_directions[i][0],x,y), flood_areas[i])
            #TODO
            #traverse longest path, and see if path to tail opens up during path traversal, if so, area is viable to go through

        if (flood_directions[i][1] > largest_flood[1]):
            largest_flood[0] = flood_directions[i][0]
            largest_flood[1] = flood_directions[i][1]
    
    if (len(final_directions) == 0):
        final_directions.append(largest_flood[0])
        #no large enough area found
        return final_directions, False

    #Found a large enough area
    return final_directions, True

def flood_fill_recursive(matrix, x, y):
    if (matrix[x][y] == 0):
        matrix[x][y] = 2
        if (x > 0):
            matrix = flood_fill_recursive(matrix, x-1, y)
        if (x < len(matrix[y]) - 1):
            matrix = flood_fill_recursive(matrix, x+1, y)
        if (y > 0):
            matrix = flood_fill_recursive(matrix, x, y-1)
        if (y < len(matrix) - 1):
            matrix = flood_fill_recursive(matrix, x, y+1)

        return matrix
    return matrix

#TODO
#if space between head and tail
#remove body that gets in way to tail from walls in path if body would move out of way once head
#arrvies at that location
def find_own_tail_path(aStar, data, growing):
    #reset grid to have tail space as goal
    tail_x = data['you']['body'][len(data['you']['body']) - 1]['x']
    tail_y = data['you']['body'][len(data['you']['body']) - 1]['y']

    #if head and tail are the same space, ie starting turn
    if ((tail_x == data['you']['body'][0]['x']) and (tail_y == data['you']['body'][0]['y'])):
        directions = []
        print("Tail and head are on the same tile: " + str(tail_x) + " " + str(tail_y))
        return directions

    #if growing, need to find path to space before tail and solid tail
    if (growing):
        new_aStar, walls = init_astar(data, False, True)
        new_aStar.set_ending_for_init_grid((tail_x, tail_y))
        path = new_aStar.solve()
    else:
        aStar.reset_grid((tail_x, tail_y))
        path = aStar.solve()


    if (path != None):
        directions = get_directions(data['you']['body'][0]['x'],data['you']['body'][0]['y'], 
                                    path[1][0], path[1][1])

        print("Path to tail direction = " + str(directions))

        return directions

    print("No path to tail")

    return None

def find_other_snake_tail_path(data, aStar, walls):
    shortest_path = None
    snake_following_name = ''
    #reset grid to have tail space as goal
    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self

        tail_x = data['board']['snakes'][i]['body'][len(data['board']['snakes'][i]['body']) - 1]['x']
        tail_y = data['board']['snakes'][i]['body'][len(data['board']['snakes'][i]['body']) - 1]['y']

        #if head and tail are the same space, ie starting turn
        if ((tail_x == data['board']['snakes'][i]['body'][0]['x']) and (tail_y == data['board']['snakes'][i]['body'][0]['y'])):
            directions = []
            print("Tail and head of snake " + str(data['board']['snakes'][i]['name']) + " are on the same tile: " + str(tail_x) + " " + str(tail_y))
            return directions

        growing = determine_if__snake_growing(data, i)

        #if growing, need to find path to space before tail and solid tail
        if (growing):
            new_aStar, walls = init_astar(data, False, False, i)
            new_aStar.set_ending_for_init_grid((tail_x, tail_y))
            path = new_aStar.solve()
        else:
            aStar.reset_grid((tail_x, tail_y))
            path = aStar.solve()

        if (path != None and (shortest_path == None or len(path) < len(shortest_path))):
            shortest_path = path
            snake_following_name = str(data['board']['snakes'][i]['name'])


    if (shortest_path != None):
        directions = get_directions(data['you']['body'][0]['x'],data['you']['body'][0]['y'], 
                                    shortest_path[1][0], shortest_path[1][1])

        print("Path to snake " + snake_following_name + " tail direction = " + str(directions))

        return directions

    print("No path to snake opposing snakes tails")

    return None