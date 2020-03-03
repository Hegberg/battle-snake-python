import random

from app.survive import survival_choices
from app.survive import flood_fill
from app.survive import find_tail_path

from app.attack import attack_choices

from app.eat import consumption_choices
from app.eat import get_direction

from app.a_star import AStar

from app.common import directions1_in_directions2

from app.collision_avoidance import avoid_death_collisions

def get_move(data):
 
    aStar, walls = init_astar(data)

    #directions = ["up", "down", "left", "right"]
    survival_directions = survival_choices(data, walls, aStar) #get bad options, remove them from contention

    #check spacing
    spacing_directions, can_follow_tail = get_spacing_directions(data, aStar, walls, survival_directions)

    food_directions, nearest_food = consumption_choices(data, survival_directions, aStar)

    consumption_directions = directions1_in_directions2(food_directions, survival_directions) 
    print("Food move after survival direction clear: ", consumption_directions)

    #meme unitl do something with it, just returns 0
    attack_percentages = attack_choices(data, survival_directions)

    #if viable path to tail, and a viable path to food, see if viable path from head -> food -> tail
    food_tail_directions = None
    if (can_follow_tail and consumption_directions != None and len(consumption_directions) > 0):
        food_tail_directions = head_to_food_to_tail_direction(data, aStar, nearest_food, survival_directions)
    

    """priority, survive, avoid_collisions, space, food
    all directions already filtered thorugh survival directions
    need to check if food fits in space,
    than space fits in avoid collisions
    than collision fits in survive

    Downward check in terms of prioity, make sure each less pressing thing fits in more pressing issue
    """

    #temp until add collision avoidance
    no_head_collisions_directions = avoid_death_collisions(data, walls, survival_directions)

    final_directions = get_directions_through_food_space_collision(consumption_directions, 
                                    spacing_directions, no_head_collisions_directions, survival_directions, food_tail_directions)

    #no path availabe that won't kill us, so just return any response
    if (len(final_directions) <= 0 and len(survival_directions) > 0):
        final_directions = survival_directions
    elif(len(final_directions) <= 0):
        final_directions = ["up", "down", "left", "right"]

    direction = random.choice(final_directions)
    return direction

def get_spacing_directions(data, aStar, walls, survival_directions):
    flood_directions, can_follow_flood = flood_fill(data, walls, survival_directions)

    tail_directions = find_tail_path(aStar, data)

    can_follow_tail = False
    #viable path to tail found
    if (tail_directions != None):
        can_follow_tail = True

    spacing_directions = []
    #large enough area to go into, add direction to spacing directions
    if (can_follow_flood):
        for direction in flood_directions:
            if (direction in survival_directions):
                spacing_directions.append(direction)
    print("Area Flood after survival direction clear: ", spacing_directions)

    #can follow tail, add direction to spacing directions
    if (can_follow_tail):
        for direction in tail_directions:
            if (direction in survival_directions and not direction in spacing_directions):
                spacing_directions.append(direction)
    print("Head->Food->Tail and Flood after survival direction clear: ", spacing_directions)

    return spacing_directions, can_follow_tail

def get_directions_through_food_space_collision(consumption_directions, spacing_directions, no_head_collisions_directions, survival_directions, food_tail_directions):
    #just need to use blank state of directions, try to fill in with useful ones
    spacing_and_consumption_directions = []
    #if space and consumptions possibilities, try to mix
    if (len(spacing_directions) > 0 and len(consumption_directions) > 0):
        #get spacing and food mix, if not possible just returns space directions
        spacing_and_consumption_directions = get_spacing_and_consumption_directions(consumption_directions, spacing_directions, food_tail_directions)
    #else check if spacing options exist, and just use those
    elif(len(spacing_directions) > 0):
        spacing_and_consumption_directions = spacing_directions

    print("Directions after space and food merge: " + str(spacing_and_consumption_directions))

    no_head_collision_and_spacing_directions = []
    #spacing directions viable after taking into account collisions
    if (len(spacing_and_consumption_directions) > 0):
        no_head_collision_and_spacing_directions = directions1_in_directions2(spacing_and_consumption_directions, no_head_collisions_directions)
        print("Directions after collision and space merge 1 : " + str(no_head_collision_and_spacing_directions))
    
    #if no viable spaces that give good space and avoid head on collisions, avoid head collisions first
    if (len(no_head_collision_and_spacing_directions) == 0 and len(no_head_collisions_directions) > 0):
        no_head_collision_and_spacing_directions = no_head_collisions_directions
        print("Directions after collision and space merge 2 : " + str(no_head_collision_and_spacing_directions))
    #if no collision spaces available, just use survival spaces
    elif (len(no_head_collision_and_spacing_directions) == 0 and len(no_head_collisions_directions) == 0):
        no_head_collision_and_spacing_directions = survival_directions
    print("Directions after collision and space merge 3 : " + str(no_head_collision_and_spacing_directions))

    return no_head_collision_and_spacing_directions

#returns directions that give space and food, if no overlap, gives space directions back
def get_spacing_and_consumption_directions(consumption_directions, spacing_directions, food_tail_directions):
    #food directions viable after spacing taken into account
    spacing_and_consumption_directions = directions1_in_directions2(consumption_directions, spacing_directions)
    print("Food move after spacing merge: ", spacing_and_consumption_directions)

    #if spacing and food not compatible, try head->food->tail if viable path exists for that
    if (len(spacing_and_consumption_directions) == 0 and food_tail_directions != None):
        spacing_and_consumption_directions = food_tail_directions
        print("Food move after food_tail merge: ", spacing_and_consumption_directions)

    #if spacing and consumption directions have no entries, can't eat so ignore food
    if (len(spacing_and_consumption_directions) == 0):
        spacing_and_consumption_directions = spacing_directions
        print("Spacing after failed to merge with food: ", spacing_and_consumption_directions)

    return spacing_and_consumption_directions


def head_to_food_to_tail_direction(data, aStar, nearest_food, survival_directions):
    
    you_x = data['you']['body'][0]['x']
    you_y = data['you']['body'][0]['y']
    aStar.reset_grid_and_start((you_x, you_y), (nearest_food[0], nearest_food[1]))

    to_food_path = aStar.solve()

    #can get to food
    if (to_food_path != None):
        tail_x = data['you']['body'][len(data['you']['body']) - 1]['x']
        tail_y = data['you']['body'][len(data['you']['body']) - 1]['y']

        head_blocking_aStar, new_walls = init_astar(data, True)

        head_blocking_aStar.reset_grid_and_start((nearest_food[0], nearest_food[1]), (tail_x, tail_y))

        to_tail_path = head_blocking_aStar.solve()

        if (to_tail_path != None):
            path_directions = get_direction(you_x, you_y, to_food_path[1][0], to_food_path[1][1])
            
            #if direction of food not in viable direction, remove option
            revised_path_directions = []
            for direction in path_directions:
                if (direction in survival_directions):
                    revised_path_directions.append(direction)

            print("To Food to Tail direction : ", revised_path_directions)
            if (len(revised_path_directions) > 0):
                return revised_path_directions

    return None

def init_astar(data, with_own_head_blocking = False):
    aStar = AStar()
    
    walls = []

    start_point = 1
    if (with_own_head_blocking):
        start_point = 0

    for i in range(start_point, len(data['you']['body'])):
        #ignore own tail
        if (i == len(data['you']['body']) - 1):
            continue

        walls.append((data['you']['body'][i]['x'], data['you']['body'][i]['y']))

    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self

        for j in range(len(data['board']['snakes'][i]['body'])):
            #if tail, don't count as wall
            if (j == len(data['board']['snakes'][i]['body']) - 1):
                continue

            walls.append((data['board']['snakes'][i]['body'][j]['x'], data['board']['snakes'][i]['body'][j]['y']))

    #print("Obstacles in board: " + str(walls))

    #init astar with new board, set end goal as temp value
    x = data['you']['body'][0]['x']
    y = data['you']['body'][0]['y']
    current_position = (x, y)
    goal = (0,0)
    aStar.init_grid(data['board']['width'], data['board']['height'], walls, current_position, goal)

    return aStar, walls