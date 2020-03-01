

def consumption_choices(data, directions):
    
    nearest_food = locate_food(data['you']['body'][0]['x'], data['you']['body'][0]['y'], data, directions)

    if (nearest_food != None):
        #return directions of nearest food
        print("Direction of closest food: ", nearest_food)
        return nearest_food[0]

    return None

def locate_food(x,y,data,directions):

    food = []

    for i in range(len(data['board']['food'])):
        food.append(get_direction(x,y, data['board']['food'][i]['x'], data['board']['food'][i]['y']))

    if (len(food) > 0):
        closest = food[0]
    else:
        return None

    for i in range(1, len(food)):
        for j in range(len(food[i][0])):
            #if food is in moveable direction and is closest food, choose as best choice
            if (food[i][0][j] in directions and food[i][1] < closest[1]):
                closest = food[i]
                continue

    return closest


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

    distance = abs(x - x2) + abs(y - y2)

    return directions,distance
