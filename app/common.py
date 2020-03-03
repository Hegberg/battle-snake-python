

def directions1_in_directions2(directions1, directions2):
    directions = []
    if (directions1 != None and len(directions1) > 0):
        #if direction of food not in viable direction, remove option
        for direction in directions1:
            if (direction in directions2):
                directions.append(direction)

        return directions

    return None

def get_direction(x,y,x2,y2):
 
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

def add_to_dict(x, y, dict):
    if (not (x,y) in dict):
        dict[(x,y)] = 1
    else:
        dict[(x,y)] += 1

#return true if path stuck between 2 walls
def check_if_path_in_between_walls(data, path, walls):

    for i in range(0, len(path)):
        adjacent_x_axis_walls = 0
        adjacent_y_axis_walls = 0
        if ((path[0] + 1, path[1]) in walls):
            adjacent_x_axis_walls += 1
        if ((path[0] - 1, path[1]) in walls):
            adjacent_x_axis_walls += 1
        if ((path[0], path[1] + 1) in walls):
            adjacent_y_axis_walls += 1
        if ((path[0], path[1] - 1) in walls):
            adjacent_y_axis_walls += 1

        if (adjacent_x_axis_walls >= 2 or adjacent_y_axis_walls >= 2):
            #path in between 2 opposing walls
            return True

    return False
