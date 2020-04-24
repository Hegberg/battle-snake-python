import random

from app.survive import survival_choices
from app.survive import flood_fill
from app.survive import find_own_tail_path
from app.survive import find_other_snake_tail_path

from app.attack import attack_chase
from app.attack import attack_cutoff
from app.attack import attack_collide

from app.eat import consumption_choices
from app.eat import get_directions

from app.a_star import AStar
from app.a_star import init_astar

from app.common import directions1_in_directions2
from app.common import check_if_direction_in_between_walls
from app.common import check_if_path_in_between_walls
from app.common import DEBUG_LOGS

from app.collision_avoidance import avoid_death_collisions

def get_move(data):
 
    aStar, walls = init_astar(data)

    #directions = ["up", "down", "left", "right"]
    survival_directions = survival_choices(data, walls, aStar) #get bad options, remove them from contention

    growing = determine_if_growing(data)

    #check spacing
    spacing_directions, tail_directions, other_snake_tail_directions, can_follow_tail, can_follow_other_snake_tail  = get_spacing_directions(data, aStar, walls, survival_directions, growing)

    if (DEBUG_LOGS):
        print("Final spacing directions: " + str(spacing_directions))

    food_directions, nearest_food = consumption_choices(data, aStar, walls)

    consumption_directions = directions1_in_directions2(food_directions, survival_directions) 
    if (DEBUG_LOGS):
        print("Food move after survival direction clear: ", consumption_directions)

    #check to see if can attack snake
    attack_directions = get_attack_directions(data, aStar, walls, survival_directions)
    

    """priority, survive, avoid_collisions, space, attack, food
    all directions already filtered thorugh survival directions
    need to check if food fits in space,
    than space fits in avoid collisions
    than collision fits in survive

    Downward check in terms of prioity, make sure each less pressing thing fits in more pressing issue
    """

    #if viable path to tail, and a viable path to food, see if viable path from head -> food -> tail
    food_tail_directions = None
    if (can_follow_tail and consumption_directions != None and len(consumption_directions) > 0):
        food_tail_directions = head_to_food_to_tail_direction(data, aStar, walls, nearest_food, survival_directions)
        if (food_tail_directions != None):
            for direction in food_tail_directions:
                if (direction in survival_directions and not(direction in spacing_directions)):
                    spacing_directions.append(direction)
            if (DEBUG_LOGS):
                print("Own snake tail follow and spacing after survival direction clear: ", spacing_directions)

    #if viable path to opponent tail, and a viable path to food, see if viable path from head -> food -> opponent tail
    food_opponent_tail_directions = None
    if (can_follow_other_snake_tail and consumption_directions != None and len(consumption_directions) > 0):
        food_opponent_tail_directions = head_to_food_to_opponent_tail_direction(data, aStar, walls, nearest_food, survival_directions)
        if (food_opponent_tail_directions != None):
            for direction in food_opponent_tail_directions:
                if (direction in survival_directions and not(direction in spacing_directions)):
                    spacing_directions.append(direction)
            if (DEBUG_LOGS):
                print("Other snake tail follow and spacing after survival direction clear: ", spacing_directions)

    #temp until add collision avoidance
    no_head_collisions_directions = avoid_death_collisions(data, walls, survival_directions)

    #if can attack, set as preffered actions
    if (len(attack_directions) > 0):
        preferred_directions = attack_directions

    #if no viable attack, try to eat
    else:
        preferred_directions = get_directions_through_food_space_collision(consumption_directions, 
                                    spacing_directions, no_head_collisions_directions, survival_directions, food_tail_directions, food_opponent_tail_directions)

    final_directions = get_directions_with_space_and_collision_merge(preferred_directions, spacing_directions, no_head_collisions_directions, survival_directions)

    #no path availabe that won't kill us, so just return any response
    if (len(final_directions) <= 0 and len(survival_directions) > 0):
        final_directions = survival_directions
    elif(len(final_directions) <= 0):
        final_directions = ["up", "down", "left", "right"]

    if (DEBUG_LOGS):
        print("Final Directions before last reform: " + str(final_directions))

    #multiple good options
    if (len(final_directions) > 1):

        #follow tail if possible
        pos_tail_directions = directions1_in_directions2(tail_directions, final_directions)

        if (pos_tail_directions != None and len(pos_tail_directions) > 0):
            final_directions = pos_tail_directions
            if (DEBUG_LOGS):
                print("Final Directions after tail: " + str(final_directions))
            direction = random.choice(final_directions)
            return direction

        #follow opponent tail if possible
        pos_tail_directions = directions1_in_directions2(other_snake_tail_directions, final_directions)

        if (pos_tail_directions != None and len(pos_tail_directions) > 0):
            final_directions = pos_tail_directions
            if (DEBUG_LOGS):
                print("Final Directions after opponent tail: " + str(final_directions))
            direction = random.choice(final_directions)
            return direction

        #go straight if possible
        prev_directions =  get_directions(data['you']['body'][0]['x'], data['you']['body'][0]['y'], data['you']['body'][1]['x'], data['you']['body'][1]['y'])

        if (prev_directions != None):
            inverse_directions = []
            for direction in prev_directions:
                if (direction == "left"):
                    inverse_directions.append("right")
                elif (direction == "right"):
                    inverse_directions.append("left")
                elif (direction == "down"):
                    inverse_directions.append("up")
                elif (direction == "up"):
                    inverse_directions.append("down")

            forward_directions = directions1_in_directions2(inverse_directions, final_directions)

            if (forward_directions != None and len(forward_directions) > 0):
                final_directions = forward_directions
                if (DEBUG_LOGS):
                    print("Final Directions after straight: " + str(final_directions))
                direction = random.choice(final_directions)
                return direction

    direction = random.choice(final_directions)
    return direction
"""
        #multiple options, only get here if don't have paths to follow, so just head towards mid preferred
        if ((int(data['board']['width']/2), int(data['board']['height']/2)) == (data['you']['body'][0]['x'], data['you']['body'][0]['y'])):
            print("Center map same as you snake head")
            path = None
        else:
            aStar.reset_grid_and_start((data['you']['body'][0]['x'], data['you']['body'][0]['y']), (int(data['board']['width']/2), int(data['board']['height']/2)))
            path = aStar.solve()

        #if path to mid exists
        if (path != None):
            center_directions = get_directions(data['you']['body'][0]['x'],data['you']['body'][0]['y'], path[1][0], path[1][1])
            center_final_directions = []
            for direction in center_directions:
                if direction in final_directions:
                    center_final_directions.append(direction)

            if (len(center_final_directions) > 0):
                print("Final Directions after centered: " + str(center_final_directions))
                direction = random.choice(center_final_directions)
                return direction
"""

#TODO
#change health check, to check for distance to nearest food, and if hunger left can get me there
#with a small amount to spare, go to food
#otherwise attack
#currently just check if health is above decent value

#TODO
#if multiple attack directions, choose one that will next turn keep me able to continue chasing the opponents head
def get_attack_directions(data, aStar, walls, survival_directions):
    attack_directions = []

    if (data['you']['health'] >= 25):
        attack_cutoff_directions = attack_cutoff(data, aStar, walls, survival_directions)

        #add cutoff directions
        for direction in attack_cutoff_directions:
            if (direction in survival_directions):
                attack_directions.append(direction)

        #if can cutoff opposing snake, do it
        if (len(attack_directions) > 0):
            return attack_directions

    #if largest snake by 2, and hunger > 50 (0-100)
    required_size_difference = 1

    snake_size_larger = True
    #for all snakes, if smaller than any, eat instead
    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self

        #if multiple snakes, be 1 sizes larger than required_size_difference before attacking
        if ((len(data['board']['snakes']) > 2) and 
            len(data['you']['body']) < len(data['board']['snakes'][i]['body']) + required_size_difference + 1):
            snake_size_larger = False

        if (len(data['you']['body']) < len(data['board']['snakes'][i]['body']) + required_size_difference):
            snake_size_larger = False

    if (snake_size_larger and data['you']['health'] >= 25):
        #if can collide opposing snake and large
        attack_collide_directions = attack_collide(data, walls, survival_directions)

        #add collide directions
        for direction in attack_collide_directions:
            if (direction in survival_directions):
                attack_directions.append(direction)

        #if can collide opposing snake, do it
        if (len(attack_directions) > 0):
            return attack_directions


    attack_chase_directions = []
    if (snake_size_larger and data['you']['health'] >= 25):
        #if can close distance to opponent head
        attack_chase_directions = attack_chase(data, aStar, walls, survival_directions)

    #add chase directions
    for direction in attack_chase_directions:
        if (direction in survival_directions):
            attack_directions.append(direction)

    return attack_directions

def determine_if_growing(data):
    if (len(data['you']['body']) > 2):
        t1_x = data['you']['body'][len(data['you']['body']) - 1]['x']
        t1_y = data['you']['body'][len(data['you']['body']) - 1]['y']
        t2_x = data['you']['body'][len(data['you']['body']) - 2]['x']
        t2_y = data['you']['body'][len(data['you']['body']) - 2]['y']
        if (t1_x == t2_x and t1_y == t2_y):
            return True
    return False

def get_spacing_directions(data, aStar, walls, survival_directions, growing):
    flood_directions_and_lane, can_follow_flood, tail_flood_directions = flood_fill(data, walls, survival_directions, aStar)
    lane_filter_flood_directions, single_lane_flood = single_lane_filter(flood_directions_and_lane)
    flood_directions = lane_filter_flood_directions

    tail_directions_and_lane = find_own_tail_path(aStar, walls, data, growing)
    lane_filter_tail_directions, single_lane_tail = single_lane_filter(tail_directions_and_lane)
    tail_directions = lane_filter_tail_directions

    other_snake_tail_directions_and_lane = find_other_snake_tail_path(data, aStar, walls)
    lane_filter_other_snake_tail_directions, single_lane_other_tail = single_lane_filter(other_snake_tail_directions_and_lane)
    other_snake_tail_directions = lane_filter_other_snake_tail_directions

    if (DEBUG_LOGS):
        print("Flood: " + str(flood_directions))
        print("My Tail: " + str(tail_directions))
        print("Other snake tail: " + str(other_snake_tail_directions))

    can_follow_tail = False
    can_follow_other_snake_tail = False

    #viable path to tail found
    if (tail_directions != None and len(tail_directions) > 0):
        can_follow_tail = True

    #viable path to other snake tail found
    if (other_snake_tail_directions != None and len(other_snake_tail_directions) > 0):
        can_follow_other_snake_tail = True

    spacing_directions = []
    #large enough area to go into, add direction to spacing directions
    if (can_follow_flood):
        for direction in flood_directions:
            if (direction in survival_directions):
                spacing_directions.append((direction, single_lane_flood))
        if (DEBUG_LOGS):
            print("Area Flood after survival direction clear: ", spacing_directions)

    #can follow tail, add direction to spacing directions
    if (can_follow_tail):
        for direction in tail_directions:
            if (direction in survival_directions and not((direction, single_lane_tail) in spacing_directions)):
                spacing_directions.append((direction, single_lane_tail))
        if (DEBUG_LOGS):
            print("Head->Food->Tail and Flood after survival direction clear: ", spacing_directions)
    
    #if can follow opponent tail, add direction to spacing directions
    if (can_follow_other_snake_tail):
        for direction in other_snake_tail_directions:
            if (direction in survival_directions and not((direction, single_lane_other_tail) in spacing_directions)):
                spacing_directions.append((direction, single_lane_other_tail))
        if (DEBUG_LOGS):
            print("Other snake tail follow and spacing after survival direction clear: ", spacing_directions)

    #if can't follow tail, and no area large enough, and can't follow opponent tail, go with largest area
    if (not can_follow_flood and not can_follow_tail and not can_follow_other_snake_tail):
        for direction in flood_directions:
            if (direction in survival_directions):
                spacing_directions.append((direction, single_lane_flood))
        if (DEBUG_LOGS):
            print("Area Flood after normal flood and tail follow fail: ", spacing_directions)



    #if multiple spacing options
    #check if any spacing directions go through single path, if they do remove that option

    spacing_directions, spacing_single_filter = single_lane_filter(spacing_directions)

    if (DEBUG_LOGS):
        print("spacing direstions after merge and single lane filter: " + str(spacing_directions))
        print("spacing filter: " + str(spacing_single_filter))

    if (len(spacing_directions) > 1):
        space_directions_before_single_lane = spacing_directions[:]
        for direction in spacing_directions: #use spacing directions as in check so don't remove elemts while iterating through and missing some
            if (check_if_direction_in_between_walls(data, aStar, walls, direction)):
                space_directions_before_single_lane.remove(direction)

        #if directions still exist that are not of single path use new directions, 
        #otherwise use directions before check
        if (DEBUG_LOGS):
            print("Spaces not part of single lane: " + str(space_directions_before_single_lane))
        if (len(space_directions_before_single_lane) > 0):
            spacing_directions = space_directions_before_single_lane
            if (DEBUG_LOGS):
                print("Spacing directions after single lane filter: " + str(spacing_directions))

    #add all tail paths together
    if (len(tail_flood_directions) > 0):
        for direction in tail_flood_directions:
            if (not direction in tail_directions):
                tail_directions.append(direction)

    return spacing_directions, tail_directions, other_snake_tail_directions, can_follow_tail, can_follow_other_snake_tail

def single_lane_filter(directions_and_single_lane):
    single_lane_directions = []
    multi_lane_directions = []
    #go through entire list, seperate into single and non single lane
    for i in range(len(directions_and_single_lane)):
        #make sure direction not None
        if (directions_and_single_lane[i][0] == None):
            continue

        #true means single lane, false means multi
        if (directions_and_single_lane[i][1]):
            single_lane_directions.append(directions_and_single_lane[i][0])
        else:
            multi_lane_directions.append(directions_and_single_lane[i][0])

    if (len(multi_lane_directions) > 0):
        return multi_lane_directions, False
    else:
        return single_lane_directions, True

def get_directions_through_food_space_collision(consumption_directions, spacing_directions, no_head_collisions_directions, survival_directions, food_tail_directions, food_opponent_tail_directions):
    #just need to use blank state of directions, try to fill in with useful ones
    spacing_and_consumption_directions = []
    #if space and consumptions possibilities, try to mix
    if (spacing_directions != None and len(spacing_directions) > 0 and consumption_directions != None and len(consumption_directions) > 0):
        #get spacing and food mix, if not possible just returns space directions
        spacing_and_consumption_directions = get_spacing_and_consumption_directions(consumption_directions, spacing_directions, food_tail_directions, food_opponent_tail_directions)
    #else check if spacing options exist, and just use those
    elif(spacing_directions != None and len(spacing_directions) > 0):
        spacing_and_consumption_directions = spacing_directions

    if (DEBUG_LOGS):
        print("Directions after space and food merge: " + str(spacing_and_consumption_directions))

    return spacing_and_consumption_directions

def get_directions_with_space_and_collision_merge(preferred_directions, spacing_directions, no_head_collisions_directions, survival_directions):
#survival, spacing, avoid_head_on, preffered
    if (DEBUG_LOGS):
        print("Prefferred directions: " + str(preferred_directions))
        print("Spacing directions: " + str(spacing_directions))
        print("No Head Collision directions: " + str(no_head_collisions_directions))
        print("Survival directions: " + str(survival_directions))

    preffered_and_spacing_directions = []
    #prefered directions viable after taking into account collisions
    if (len(preferred_directions) > 0 and len(spacing_directions) > 0):
        preffered_and_spacing_directions = directions1_in_directions2(preferred_directions, spacing_directions)
        if (DEBUG_LOGS):
            print("Directions after space and prefferred direction merge 1: " + str(preffered_and_spacing_directions))
    elif (len(spacing_directions) > 0):
        preffered_and_spacing_directions = spacing_directions
        if (DEBUG_LOGS):
            print("Directions after space and prefferred direction merge 2: " + str(preffered_and_spacing_directions))
    else:
        preffered_and_spacing_directions = preferred_directions
        if (DEBUG_LOGS):
            print("Directions after space and prefferred direction merge 3: " + str(preffered_and_spacing_directions))

    #if no valid merge between the collision and preffered, and collision has options, use that as collision and preffered directions
    if (len(preffered_and_spacing_directions) == 0 and len(spacing_directions) > 0):
        preffered_and_spacing_directions = spacing_directions
        if (DEBUG_LOGS):
            print("Directions after no collision and prefferred direction merge 4: " + str(spacing_directions))

    no_head_collision_and_preffered_directions = []
    #(head on and preffered) taking into account spacing
    #merge preffered and spacing with no head on collision
    no_head_collision_and_preffered_directions = spacing_and_no_head_collision_merge(no_head_collisions_directions, preffered_and_spacing_directions)

    #if no valid merge between the preferred_spacing and collision, and spacing has options, use that as spacing and collision directions
    if (len(no_head_collision_and_preffered_directions) == 0 and len(spacing_directions) > 0):
        preffered_and_spacing_directions = spacing_directions
        if (DEBUG_LOGS):
            print("Directions after no collision and prefferred direction merge 8: " + str(preffered_and_spacing_directions))

        #preform spacing and no_head_collision_merge, again, but now with just spacing instead of preferred spacing
        no_head_collision_and_preffered_directions = spacing_and_no_head_collision_merge(no_head_collisions_directions, preffered_and_spacing_directions)
    
    #if no valid merge between the spacing and collision, and spacing has options, use that as spacing and collision directions
    if (len(no_head_collision_and_preffered_directions) == 0 and len(no_head_collisions_directions) > 0):
        no_head_collision_and_preffered_directions = no_head_collisions_directions
        if (DEBUG_LOGS):
            print("Directions after no collision and prefferred direction merge 9: " + str(no_head_collision_and_preffered_directions))


    survival_and_spacing_directions = []
    #if no viable spaces that give good space and avoid head on collisions, try to get to open space first
    if (len(no_head_collision_and_preffered_directions) > 0 and len(survival_directions) > 0):
        survival_and_spacing_directions = directions1_in_directions2(no_head_collision_and_preffered_directions, survival_directions)
        if (DEBUG_LOGS):
            print("Directions after space and survival direction merge 10: " + str(survival_and_spacing_directions))
    
    #no valid merge between spacing and survival, use survival
    if (len(survival_and_spacing_directions) == 0):
        survival_and_spacing_directions = survival_directions
        if (DEBUG_LOGS):
            print("Directions after space and survival direction merge 11: " + str(survival_and_spacing_directions))

    return survival_and_spacing_directions

def spacing_and_no_head_collision_merge(no_head_collisions_directions, preffered_and_spacing_directions):
    if ((len(no_head_collisions_directions) > 0) and len(preffered_and_spacing_directions) > 0):
        no_head_collision_and_preffered_directions = directions1_in_directions2(no_head_collisions_directions, preffered_and_spacing_directions)
        if (DEBUG_LOGS):
            print("Directions after no collision and prefferred direction merge 5: " + str(no_head_collision_and_preffered_directions))
    elif (len(no_head_collisions_directions) > 0):
        no_head_collision_and_preffered_directions = no_head_collisions_directions
        if (DEBUG_LOGS):
            print("Directions after no collision and prefferred direction merge 6: " + str(no_head_collision_and_preffered_directions))
    else:
        no_head_collision_and_preffered_directions = preffered_and_spacing_directions
        if (DEBUG_LOGS):
            print("Directions after no collision and prefferred direction merge 7: " + str(no_head_collision_and_preffered_directions))
    return no_head_collision_and_preffered_directions

#returns directions that give space and food, if no overlap, gives space directions back
def get_spacing_and_consumption_directions(consumption_directions, spacing_directions, food_tail_directions, food_opponent_tail_directions):
    #food directions viable after spacing taken into account
    spacing_and_consumption_directions = directions1_in_directions2(consumption_directions, spacing_directions)
    if (DEBUG_LOGS):
        print("Food move after spacing merge: ", spacing_and_consumption_directions)

    #if spacing and food not compatible, try head->food->tail if viable path exists for that
    if (len(spacing_and_consumption_directions) == 0 and food_tail_directions != None):
        spacing_and_consumption_directions = food_tail_directions
        if (DEBUG_LOGS):
            print("Food move after food_tail merge: ", spacing_and_consumption_directions)

    #if head->food->tail not compatible, try head->food->opponent_tail if viable path exists for that
    if (len(spacing_and_consumption_directions) == 0 and food_opponent_tail_directions != None):
        spacing_and_consumption_directions = food_opponent_tail_directions
        if (DEBUG_LOGS):
            print("Food move after opponent_food_tail merge: ", spacing_and_consumption_directions)

    #if spacing and consumption directions have no entries, can't eat so ignore food
    if (len(spacing_and_consumption_directions) == 0):
        spacing_and_consumption_directions = spacing_directions
        if (DEBUG_LOGS):
            print("Spacing after failed to merge with food: ", spacing_and_consumption_directions)

    return spacing_and_consumption_directions

#TODO
#if tail <- food <- food <- head, don't eat food and follow tail since will die
def head_to_food_to_tail_direction(data, aStar, walls, nearest_food, survival_directions):
    
    you_x = data['you']['body'][0]['x']
    you_y = data['you']['body'][0]['y']
    aStar.reset_grid_and_start((you_x, you_y), (nearest_food[0], nearest_food[1]))

    to_food_path = aStar.solve()

    single_lane = check_if_path_in_between_walls(data, aStar, to_food_path, walls)
    if (single_lane):
        #print("Attack Path is between walls, ignore it: " + str(path))
        to_food_path = None
        return None

    #can get to food
    if (to_food_path != None):
        tail_x = data['you']['body'][len(data['you']['body']) - 1]['x']
        tail_y = data['you']['body'][len(data['you']['body']) - 1]['y']

        head_blocking_aStar, new_walls = init_astar(data, True)

        head_blocking_aStar.reset_grid_and_start((nearest_food[0], nearest_food[1]), (tail_x, tail_y))

        to_tail_path = head_blocking_aStar.solve()

        if (to_tail_path != None):

            single_lane = check_if_path_in_between_walls(data, head_blocking_aStar, to_tail_path, new_walls)
            if (single_lane):
                #print("Attack Path is between walls, ignore it: " + str(path))
                to_tail_path = None
                return None

            path_directions = get_directions(you_x, you_y, to_food_path[1][0], to_food_path[1][1])
            
            #if direction of food not in viable direction, remove option
            revised_path_directions = []
            for direction in path_directions:
                if (direction in survival_directions):
                    revised_path_directions.append(direction)

            if (DEBUG_LOGS):
                print("To Food to Tail direction : ", revised_path_directions)
            if (len(revised_path_directions) > 0):
                return revised_path_directions

    return None

def head_to_food_to_opponent_tail_direction(data, aStar, walls, nearest_food, survival_directions):
    
    you_x = data['you']['body'][0]['x']
    you_y = data['you']['body'][0]['y']
    aStar.reset_grid_and_start((you_x, you_y), (nearest_food[0], nearest_food[1]))

    to_food_path = aStar.solve()

    single_lane = check_if_path_in_between_walls(data, aStar, to_food_path, walls)
    if (single_lane):
        #print("Attack Path is between walls, ignore it: " + str(path))
        to_food_path = None
        return None

    #can get to food
    if (to_food_path != None):

        revised_path_directions = []

        for i in range(len(data['board']['snakes'])):
            if (data['board']['snakes'][i]['id'] == data['you']['id']):
                continue #skip self

            tail_x = data['board']['snakes'][i]['body'][len(data['board']['snakes'][i]['body']) - 1]['x']
            tail_y = data['board']['snakes'][i]['body'][len(data['board']['snakes'][i]['body']) - 1]['y']

            head_blocking_aStar, new_walls = init_astar(data, True)

            head_blocking_aStar.reset_grid_and_start((nearest_food[0], nearest_food[1]), (tail_x, tail_y))

            to_tail_path = head_blocking_aStar.solve()

            if (to_tail_path != None):

                single_lane = check_if_path_in_between_walls(data, head_blocking_aStar, to_tail_path, new_walls)
                if (single_lane):
                    #print("Attack Path is between walls, ignore it: " + str(path))
                    to_tail_path = None
                    continue

                path_directions = get_directions(you_x, you_y, to_food_path[1][0], to_food_path[1][1])
                
                #if direction of food not in viable direction, remove option
                for direction in path_directions:
                    if (direction in survival_directions):
                        revised_path_directions.append(direction)

        if (DEBUG_LOGS):
            print("To Food to Opponent Tail direction : ", revised_path_directions)
        if (len(revised_path_directions) > 0):
            return revised_path_directions

    return None