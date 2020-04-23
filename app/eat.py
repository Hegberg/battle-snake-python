
from app.a_star import AStar
from app.common import get_directions
from app.common import check_if_path_in_between_walls
from app.common import DEBUG_LOGS

def consumption_choices(data, aStar, walls):
    
    nearest_food_directions, nearest_food = locate_food(data['you']['body'][0]['x'], data['you']['body'][0]['y'], data, aStar, walls)

    if (nearest_food_directions != None):
        #return directions of nearest food
        if (DEBUG_LOGS):
            print("Direction of closest food: ", nearest_food_directions)
        return nearest_food_directions, nearest_food

    return None, None

def locate_food(x,y,data, aStar, walls):

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
        aStar.reset_grid_and_start((x,y), (food[i][0], food[i][1]))
        
        #find path, returns list of x,y tuple, starting at head, returns None if no path
        path = aStar.solve()

        #check if path goes through single lane, if so mark as bad and None
        if (path != None):
            single_lane = check_if_path_in_between_walls(data, aStar, path, walls)

            if (single_lane):
                #print("Eat Path is between walls, ignore it: " + str(path))
                path = None

            #if not single lane and path exists, see if opposing snake that is larger is closer, if so, don't go for food
            else:
                for j in range(len(data['board']['snakes'])):
                    if (data['board']['snakes'][j]['id'] == data['you']['id']):
                        continue #skip self
                    
                    #if opponent snake is larger
                    """
                    if (len(data['board']['snakes'][j]['body']) > len(data['you']['body'])):
                        path = None
                        break
                    """

                    p1_x = data['board']['snakes'][j]['body'][0]['x']
                    p1_y = data['board']['snakes'][j]['body'][0]['y']

                    #goal is current location
                    if ((p1_x, p1_y) == (food[i][0], food[i][1])):
                        continue

                    #remove head from unreachable cells to allow for aStar to path from opponent head to location
                    aStar.reset_grid_and_remove_wall((p1_x, p1_y), (food[i][0], food[i][1]), (p1_x, p1_y))
                    opponent_path = aStar.solve()
                    aStar.add_wall((p1_x, p1_y))

                    if (opponent_path != None and (len(path) > len(opponent_path))):
                        if (DEBUG_LOGS):
                            print("Can't eat food: " + str((food[i][0], food[i][1])) + " " + str(len(path)) + " " + str(len(opponent_path)))
                        path = None
                        break

        #if path is good and is horter than other food paths, choose
        if ((path != None) and ((shortest_path == None) or (len(path) < len(shortest_path)))):
            directions = get_directions(x,y, path[1][0], path[1][1])
            shortest_path = path
            closest_food = food[i]

    if (DEBUG_LOGS):
        print("Path Chosen: " + str(shortest_path))
    if (shortest_path != None):
        return directions, closest_food

    return None, None