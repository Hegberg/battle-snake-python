
from app.a_star import AStar
from app.common import get_direction
from app.common import check_if_path_in_between_walls

def consumption_choices(data, directions, aStar, walls):
    
    nearest_food_directions, nearest_food = locate_food(data['you']['body'][0]['x'], data['you']['body'][0]['y'], data, directions, aStar, walls)

    if (nearest_food_directions != None):
        #return directions of nearest food
        print("Direction of closest food: ", nearest_food_directions)
        return nearest_food_directions, nearest_food

    return None, None

def locate_food(x,y,data,directions, aStar, walls):

    food = []
    
    for i in range(len(data['board']['food'])):
        food.append((data['board']['food'][i]['x'], data['board']['food'][i]['y']))

    if (len(food) == 0):
        return None

    shortest_path = None
    directions = []
    closest_food = None

    #for each food, get path, use shortest path
    for i in range(len(food)):
        
        #set goal to food
        aStar.reset_grid((food[i][0], food[i][1]))
        
        #find path, returns list of x,y tuple, starting at head, returns None if no path
        path = aStar.solve()

        #check if path goes through single lane, if so mark as bad and None
        single_lane = check_if_path_in_between_walls(data, path, walls)
        if (single_lane):
            print("Path is between walls, ignore it: " + str(path))
            path = None

        #if path is good and is horter than other food paths, choose
        if ((path != None) and ((shortest_path == None) or (len(path) < len(shortest_path)))):
            directions = get_direction(x,y, path[1][0], path[1][1])
            shortest_path = path
            closest_food = food[i]

    print("Path Chosen: " + str(shortest_path))
    if (shortest_path != None):
        return directions, closest_food

    return None, None