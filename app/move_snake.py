import random

from app.survive import survival_choices
from app.attack import attack_choices
from app.eat import consumption_choices
from app.a_star import AStar

def get_move(data):
 
    aStar = AStar()
    
    walls = []

    for i in range(1, len(data['you']['body'])):
        walls.append((data['you']['body'][i]['x'], data['you']['body'][i]['y']))

    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self

        for j in range(len(data['board']['snakes'][i]['body'])):
            walls.append((data['board']['snakes'][i]['body'][j]['x'], data['board']['snakes'][i]['body'][j]['y']))

    print("Obstacles in board: " + str(walls))

    #init astar with new board, set end goal as temp value
    x = data['you']['body'][0]['x']
    y = data['you']['body'][0]['y']
    current_position = (x, y)
    goal = (0,0)
    aStar.init_grid(data['board']['width'], data['board']['height'], walls, current_position, goal)  

    #directions = ["up", "down", "left", "right"]
    directions = survival_choices(data) #get bad options, remove them from contention
    
    attack_percentages = attack_choices(data, directions)

    food_directions = consumption_choices(data, directions, aStar)

    if (food_directions != None):
        #if direction of food not in viable direction, remove option
        #need to double check because still grab a food at index of 0 regardless of if in good direction
        revised_food_directions = []
        for direction in food_directions:
            if (direction in directions):
                revised_food_directions.append(direction)
        
        print("Food move after direction clear: ", revised_food_directions)

        #if there are resulting options, replace direction list with smaller one
        if (len(revised_food_directions) > 0):
            directions = revised_food_directions
    print("Directions after food merge: ", directions)

    #no path availabe that won't kill us, so just return any response
    if (len(directions) <= 0):
        directions = ["up", "down", "left", "right"]

    direction = random.choice(directions)
    return direction
