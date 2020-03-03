from app.common import get_direction

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
            print("Head x y: " + str(x) + " " + str(y) + " body x y: " + str(data['you']['body'][i]['x']) + " " + str(data['you']['body'][i]['y']))

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
        if (available_directions[i] == 'up'):
            flood_matrix = flood_fill_recursive(matrix, x, y-1)
            for j in range(len(matrix)):
                for k in range(len(matrix[j])):
                    if (matrix[j][k] == 2):
                        flood_size += 1
            print("Up flood size: ", flood_size)
            for k in range(len(flood_matrix)):
                print("Flood Matrix Up " + str(i) + ": " + str(flood_matrix[k]))
            flood_directions.append(('up',flood_size))

        elif (available_directions[i] == 'down'):
            flood_matrix = flood_fill_recursive(matrix, x, y+1)
            for j in range(len(matrix)):
                for k in range(len(matrix[j])):
                    if (matrix[j][k] == 2):
                        flood_size += 1
            print("Down flood size: ", flood_size)
            for k in range(len(flood_matrix)):
                print("Flood Matrix Down " + str(i) + ": " + str(flood_matrix[k]))
            flood_directions.append(('down',flood_size))
        
        elif (available_directions[i] == 'left'):
            flood_matrix = flood_fill_recursive(matrix, x-1, y)
            for j in range(len(matrix)):
                for k in range(len(matrix[j])):
                    if (matrix[j][k] == 2):
                        flood_size += 1
            print("Left flood size: ", flood_size)
            for k in range(len(flood_matrix)):
                print("Flood Matrix Left " + str(i) + ": " + str(flood_matrix[k]))
            flood_directions.append(('left',flood_size))

        elif (available_directions[i] == 'right'):
            flood_matrix = flood_fill_recursive(matrix, x+1, y)
            for j in range(len(matrix)):
                for k in range(len(matrix[j])):
                    if (matrix[j][k] == 2):
                        flood_size += 1
            print("Right flood size: ", flood_size)
            for k in range(len(flood_matrix)):
                print("Flood Matrix Right " + str(i) + ": " + str(flood_matrix[k]))
            flood_directions.append(('right',flood_size))
    
    largest_flood = ['', 0]
    final_directions = []
    for i in range(len(flood_directions)):
        if (flood_directions[i][1] > len(data['you']['body'])):
            final_directions.append(flood_directions[i][0])
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

def find_tail_path(aStar, data):
    #reset grid to have tail space as goal
    tail_x = data['you']['body'][len(data['you']['body']) - 1]['x']
    tail_y = data['you']['body'][len(data['you']['body']) - 1]['y']

    #if head and tail are the same space, ie starting turn
    if (tail_x == data['you']['body'][0]['x'] and tail_y == data['you']['body'][0]['y']):
        directions = []
        return directions

    aStar.reset_grid((tail_x, tail_y))

    path = aStar.solve()

    if (path != None):
        directions = get_direction(data['you']['body'][0]['x'],data['you']['body'][0]['y'], 
                                    path[1][0], path[1][1])

        return directions

    return None
