

def avoid_death_collisions(data, walls, survival_directions):
    #get list of heads of other snakes that are equal or larger to me in size
    head_list = []
    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self

        head_list.append((data['board']['snakes'][i]['body'][0]['x'],
                        data['board']['snakes'][i]['body'][0]['y']))

    #get spaces they can move to that is not walls, and if tile has food
    #if there is food, try to choose any move but that one, since they will most likely go for food
    snake_movements = {} #place and amount of snakes that can move to it
    food_spots = []

    for i in range(len(data['board']['food'])):
        food_spots.append((data['board']['food'][i]['x'], data['board']['food'][i]['y']))

    for i in range(len(head_list)):
        x = head_list[i][0]
        y = head_list[i][1]
        if (x > 0):
            add_to_dict(x - 1, y, snake_movements)
        if (x < data['board']['width'] - 1):
            add_to_dict(x + 1, y, snake_movements)
        if (y > 0):
            add_to_dict(x, y - 1, snake_movements)
        if (y < data['board']['height'] - 1):
            add_to_dict(x, y + 1, snake_movements)


    #find spaces that coincide with my movement     
    collision_spots = {}

    pos_x = data['you']['body'][0]['x']
    pos_y = data['you']['body'][0]['y']

    food_collision_modifier = 1

    for i in range(len(survival_directions)):
        if (survival_directions[i] == 'up' and (pos_x, pos_y + 1) in snake_movements):
            collision_spots['up'] = snake_movements[(pos_x, pos_y + 1)]
            if ((pos_x, pos_y + 1) in food_spots):
                collision_spots['up'] += food_collision_modifier

        elif (survival_directions[i] == 'down' and (pos_x, pos_y - 1) in snake_movements):
            collision_spots['down'] = snake_movements[(pos_x, pos_y - 1)]
            if ((pos_x, pos_y - 1) in food_spots):
                collision_spots['down'] += food_collision_modifier

        elif (survival_directions[i] == 'right' and (pos_x + 1, pos_y) in snake_movements):
            collision_spots['right'] = snake_movements[(pos_x + 1, pos_y)]
            if ((pos_x + 1, pos_y) in food_spots):
                collision_spots['right'] += food_collision_modifier

        elif (survival_directions[i] == 'left' and (pos_x - 1, pos_y) in snake_movements):
            collision_spots['left'] = snake_movements[(pos_x - 1, pos_y)]
            if ((pos_x - 1, pos_y) in food_spots):
                collision_spots['left'] += food_collision_modifier

    print("Collision directions: " + str(collision_spots))

    #for spaces i can move to that have collisions, 
    #avoid highest possible collisions first, than lower secend etc
    #leave directions with no collision
    #if all collision, choose area with best chance of getting out
    directions = survival_directions
    for i in range(len(survival_directions)):
        if collision_spots.has_key(survival_directions[i]):
            directions.remove(survival_directions[i])

    print("Collision directions after removing collisions: " + str(directions))

    #if no directions without collision, choose collision with least number
    if (len(directions) == 0):
        directions.append(min(collision_spots, key=collision_spots.get))
        print("Collision directions after adding min collision: " + str(directions))

    return directions

def add_to_dict(x, y, dict):
    if (not (x,y) in dict):
        dict[(x,y)] = 1
    else:
        dict[(x,y)] += 1
