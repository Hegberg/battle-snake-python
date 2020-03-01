import random

from app.survive import survival_choices
from app.attack import attack_choices
from app.eat import consumption_choices

def get_move(data):
    #directions = ["up", "down", "left", "right"]
    directions = survival_choices(data) #get bad options, remove them from contention
    
    attack_percentages = attack_choices(data, directions)

    food_directions = consumption_choices(data, directions)

    if (food_directions != None):
        #if direction of food not in viable direction, remove option
        #need to double check because still grab a food at index of 0 regardless of if in good direction
        revised_food_directions = food_directions
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
