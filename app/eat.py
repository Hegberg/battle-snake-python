
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
    shortest_walls = []

    #for each food, get path, use shortest path
    for k in range(len(food)):
        aStar = AStar()
        
        walls = []

        for i in range(1, len(data['you']['body'])):
            walls.append((data['you']['body'][i]['x'], data['you']['body'][i]['y']))

        for i in range(len(data['board']['snakes'])):
            if (data['board']['snakes'][i]['id'] == data['you']['id']):
                continue #skip self

                for j in range(len(data['board']['snakes'][i]['body'])):
                    walls.append((data['board']['snakes'][i]['body'][j]['x'], data['board']['snakes'][i]['body'][j]['y']))

        #init astar with new board, set end goal as temp value
        x = data['you']['body'][0]['x']
        y = data['you']['body'][0]['y']
        current_position = (x, y)
        goal = (food[k][0], food[k][1])
        aStar.init_grid(data['board']['width'], data['board']['height'], walls, current_position, goal)  
        
        #set goal to food
        #aStar.reset_grid((food[i][0], food[i][1]))
        
        #find path, returns list of x,y tuple, starting at head, returns None if no path
        path = aStar.solve()

        if ((path != None) and ((shortest_path == None) or (len(path) < len(shortest_path)))):
            directions = get_direction(x,y, path[1][0], path[1][1])
            shortest_path = path
            shortest_walls = walls

    if (shortest_path != None):
        print("Path Chosen: " + str(shortest_path))
        print("Wall in chosen path: " + str(shortest_walls))
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
