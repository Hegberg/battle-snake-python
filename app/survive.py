

def survival_choices(data):
    directions = check_bounds(data)

    directions = check_self_collisions(directions, data)
    directions = check_snake_collisions(directions, data)

    return directions

def check_bounds(data):
    directions = ["up", "down", "left", "right"]
    #check if space above us is on board
    if (data['board']['height'] - data['you']['body'][0]['y'] <= 1):
        directions.remove("up")

    #check if not on bottom row
    if (data['you']['body'][0]['y'] <= 0):
        directions.remove("down")

    if (data['board']['width'] - data['you']['body'][0]['x'] <= 1):
        directions.remove("right")
    
    if (data['you']['body'][0]['x'] <= 0):
        directions.remove("left")

    return directions

def check_self_collisions(directions, data):
    return directions

def check_snake_collisions(directions, data):
    return directions
