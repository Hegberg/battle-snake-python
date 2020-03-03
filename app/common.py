

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