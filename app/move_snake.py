import random

from app.survive import survival_choices
from app.attack import attack_choices
from app.eat import consumption_choices

def get_move(data):
    #directions = ["up", "down", "left", "right"]
    directions = survival_choices(data) #get bad options, remove them from contention
    
    attack_percentages = attack_choices(data, directions)

    directions = consumption_choices(data, directions)

    if (len(directions) <= 0):
        directions = ["up", "down", "left", "right"]

    direction = random.choice(directions)
    return direction
