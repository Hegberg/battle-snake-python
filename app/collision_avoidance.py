from app.common import add_to_dict

#TODO
#add, prefer collisions with snakes same size vs snakes of smaller size
def avoid_death_collisions(data, walls, survival_directions):
    #get list of heads of other snakes that are equal or larger to me in size
    same_size_head_list = []
    large_size_head_list = []
    self_len = len(data['you']['body'])

    food_collision_modifier = 1
    large_snake_collision_modifier = 3

    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self

        #if larger or equal size, add to list
        if (len(data['board']['snakes'][i]['body']) == self_len):
            same_size_head_list.append((data['board']['snakes'][i]['body'][0]['x'], data['board']['snakes'][i]['body'][0]['y']))
        
        elif (len(data['board']['snakes'][i]['body']) >= self_len):
            large_size_head_list.append((data['board']['snakes'][i]['body'][0]['x'], data['board']['snakes'][i]['body'][0]['y']))

    #get spaces they can move to that is not walls, and if tile has food
    #if there is food, try to choose any move but that one, since they will most likely go for food
    snake_movements = {} #place and amount of snakes that can move to it
    food_spots = []

    for i in range(len(data['board']['food'])):
        food_spots.append((data['board']['food'][i]['x'], data['board']['food'][i]['y']))

    for i in range(len(same_size_head_list)):
        x = same_size_head_list[i][0]
        y = same_size_head_list[i][1]
        if (x > 0):
            add_to_dict(x - 1, y, snake_movements)
        if (x < data['board']['width'] - 1):
            add_to_dict(x + 1, y, snake_movements)
        if (y > 0):
            add_to_dict(x, y - 1, snake_movements)
        if (y < data['board']['height'] - 1):
            add_to_dict(x, y + 1, snake_movements)

    for i in range(len(large_size_head_list)):
        x = large_size_head_list[i][0]
        y = large_size_head_list[i][1]
        if (x > 0):
            add_to_dict(x - 1, y, snake_movements, large_snake_collision_modifier)
        if (x < data['board']['width'] - 1):
            add_to_dict(x + 1, y, snake_movements, large_snake_collision_modifier)
        if (y > 0):
            add_to_dict(x, y - 1, snake_movements, large_snake_collision_modifier)
        if (y < data['board']['height'] - 1):
            add_to_dict(x, y + 1, snake_movements, large_snake_collision_modifier)


    #find spaces that coincide with my movement     
    collision_spots = {}

    pos_x = data['you']['body'][0]['x']
    pos_y = data['you']['body'][0]['y']

    for i in range(len(survival_directions)):
        #need to move down to go up in y terms
        if (survival_directions[i] == 'down' and (pos_x, pos_y + 1) in snake_movements):
            collision_spots['down'] = snake_movements[(pos_x, pos_y + 1)]
            if ((pos_x, pos_y + 1) in food_spots):
                collision_spots['down'] += food_collision_modifier

        #need to move up to go down in y terms
        elif (survival_directions[i] == 'up' and (pos_x, pos_y - 1) in snake_movements):
            collision_spots['up'] = snake_movements[(pos_x, pos_y - 1)]
            if ((pos_x, pos_y - 1) in food_spots):
                collision_spots['up'] += food_collision_modifier

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
    survival_directions_copy = survival_directions[:]
    directions = survival_directions_copy
    for i in range(len(directions)):
        for j in range(len(survival_directions_copy)):
            if survival_directions_copy[j] in collision_spots:
                directions.remove(survival_directions_copy[j])
                break

    print("Collision directions after removing collisions: " + str(directions))

    #if no directions without collision, choose collision with least number
    if (len(directions) == 0 and len(collision_spots) > 0):
        lowest_value = 100 #arbitary max number
        directions = []
        for key in collision_spots.keys():
            if (collision_spots[key] < lowest_value):
                directions = []
                lowest_value = collision_spots[key]
                directions.append(key)
            elif (collision_spots[key] == lowest_value):
                directions.append(key)

        #min_value = min(collision_spots.keys(), key=(lambda k: collision_spots[k]))
        #directions.append(min_value)
        print("Collision directions after adding min collisions: " + str(directions))

    return directions
