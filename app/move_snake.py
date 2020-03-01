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
        for direction in food_directions:
            if (direction not in directions):
                food_directions.remove(direction)
        directions = food_directions

    #no path availabe that won't kill us, so just return any response
    if (len(directions) <= 0):
        directions = ["up", "down", "left", "right"]

    direction = random.choice(directions)
    return direction
