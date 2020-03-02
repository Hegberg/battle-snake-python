

def survival_choices(data, walls, aStar):
    directions = check_bounds(data)

    print("Check Bounds After: ", directions)
    directions = check_self_collisions(directions, data)
    print("Check Self After: ", directions)
    directions = check_snake_collisions(directions, data)
    print("Check Snakes After: ", directions)

    #check flood fill to see if space
    flood_directions = flood_fill(data, walls, directions)

    revised_flood_directions = []
    for direction in flood_directions:
        if (direction in directions):
            revised_flood_directions.append(direction)

    print("revised flood directions: " + str(revised_flood_directions))
    if (len(revised_flood_directions) > 0):
        return revised_flood_directions

    #check if can follow tail
    tail_direction = tail_path(aStar, data)

    #avoid being cut off

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
        collision = check_beside_self(x,y,data['you']['body'][i]['x'],data['you']['body'][i]['y'])
        if (collision != 0 and collision in directions):
            directions.remove(collision)

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
    matrix = [ [0] * data['board']['height'] ] * data['board']['width']
    
    x = data['you']['body'][0]['x']
    y = data['you']['body'][0]['y']

    #add head as wall
    walls.append((x,y))

    print("Walls: " + str(walls))

    for i in range(len(walls)):
        matrix[walls[i][0]][walls[i][1]] = 1

    flood_directions = []

    for i in range(len(matrix)):
        print("Flood Matrix " + str(i) + ": " + str(matrix[i]))
    

    for i in range(len(available_directions)):
        clean_matrix = matrix
        flood_size = 0
        if (available_directions[i] == 'up'):
            flood_size = flood_fill_recursive(clean_matrix, x, y-1, 0)
            print("Up flood size: ", flood_size)
            if (flood_size > len(data['you']['body'])):
                flood_directions.append('up')

        elif (available_directions[i] == 'down'):
            flood_size = flood_fill_recursive(clean_matrix, x, y+1, 0)
            print("Down flood size: ", flood_size)
            if (flood_size > len(data['you']['body'])):
                flood_directions.append('down')
        
        elif (available_directions[i] == 'left'):
            flood_size = flood_fill_recursive(clean_matrix, x-1, y, 0)
            print("Left flood size: ", flood_size)
            if (flood_size > len(data['you']['body'])):
                flood_directions.append('left')

        elif (available_directions[i] == 'right'):
            flood_size = flood_fill_recursive(clean_matrix, x+1, y, 0)
            print("Right flood size: ", flood_size)
            if (flood_size > len(data['you']['body'])):
                flood_directions.append('right')

    return flood_directions

def flood_fill_recursive(matrix, x, y, count):
    if (matrix[x][y] == 0):
        matrix[x][y] = 1

        if (x > 0):
            count += flood_fill_recursive(matrix, x-1, y, count)
        if (x < len(matrix[y]) - 1):
            count += flood_fill_recursive(matrix, x+1, y, count)
        if (y > 0):
            count += flood_fill_recursive(matrix, x, y-1, count)
        if (y < len(matrix) - 1):
            count += flood_fill_recursive(matrix, x, y+1, count)

        return count

    return 1

def tail_path(aStar, data):
    pass
