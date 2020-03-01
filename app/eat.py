
from app.a_star import AStar

def consumption_choices(data, directions, aStar):
    
    nearest_food = locate_food(data['you']['body'][0]['x'], data['you']['body'][0]['y'], data, directions, aStar)

    if (nearest_food != None):
        #return directions of nearest food
        print("Direction of closest food: ", nearest_food)
        return nearest_food

    return None

def locate_food(x,y,data,directions, aStar):

    food = []
    
    for i in range(len(data['board']['food'])):
        food.append((data['board']['food'][i]['x'], data['board']['food'][i]['y']))

    if (len(food) == 0):
        return None

    shortest_path = None
    directions = []

    #for each food, get path, use shortest path
    for i in range(len(food)):
        
        #set goal to food
        aStar.reset_grid((food[i][0], food[i][1]))
        
        #find path, returns list of x,y tuple, starting at head, returns None if no path
        path = aStar.solve()

        if ((path != None) and ((shortest_path == None) or (len(path) < len(shortest_path)))):
            directions = get_direction(x,y, path[1][0], path[1][1])
            shortest_path = path

    print("Path Chosen: " + str(shortest_path))
    if (shortest_path != None):
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
