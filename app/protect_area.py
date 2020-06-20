import copy
import math

from app.common import DEBUG_LOGS
from app.common import get_distance_between_points
from app.common import determine_if_snake_growing

from app.a_star import init_astar

class ProtectArea(object):
	"""docstring for ProtectArea"""
	def __init__(self, area_matrix, data, possible_directions, growing):
		#add current position to area, to see if it is located on the border or not
		area_matrix[(data['you']['body'][0]['x'], data['you']['body'][0]['y'])] = 0
		self.area_matrix = area_matrix
		self.data = copy.deepcopy(data)
		self.border_matrix = copy.deepcopy(area_matrix)
		self.possible_directions = possible_directions
		self.in_border = False
		self.growing = growing

	def get_border_matrix(self):
		for index in self.area_matrix:
			#x is on border
			if (index[0] == 0 or index[0] >= self.data['board']['width'] - 1):
				continue
			#y is on border
			if (index[1] == 0 or index[1] >= self.data['board']['height'] - 1):
				continue

			#if 8 spaces around are all in area matrix, not a border tile, remove
			if ((index[0] + 1, index[1]) in self.area_matrix and
				(index[0] - 1, index[1]) in self.area_matrix and
				(index[0] + 1, index[1] + 1) in self.area_matrix and
				(index[0] + 1, index[1] - 1) in self.area_matrix and
				(index[0] - 1, index[1] + 1) in self.area_matrix and
				(index[0] - 1, index[1] - 1) in self.area_matrix and
				(index[0], index[1] + 1) in self.area_matrix and
				(index[0], index[1] - 1) in self.area_matrix):

				if (index[0] == 4 and index[1] == 3):
					print("Removing head of snake from border list")

				#remove
				self.border_matrix.pop(index)

		if (DEBUG_LOGS):
			print("Refined border_matrix: " + str(self.border_matrix))

		#check if on border
		if ((self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y']) in self.border_matrix):
			if (DEBUG_LOGS):
				print("In border")
			self.in_border = True

		"""
		#go through and remove any border bordering own body
		for index in self.area_matrix:
			if index in self.border_matrix:
				#if border own body, and does not border other border, remove
		"""

	def get_direction_to_area_border(self):
		possible_tiles = []
		new_directions = []

		if ('up' in self.possible_directions):
			i = 1
			while (True):
				#hit edge of map
				if (self.data['you']['body'][0]['y'] - i == 0):
					print("up hit edge of map")
					break
				#if hit border, add it to possible tiles to move to
				elif ((self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y'] - i) in self.border_matrix):
					possible_tiles.append((self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y'] - i))
					new_directions.append('up')
					break

				i += 1

		if ('down' in self.possible_directions):
			i = 1
			while (True):
				#hit edge of map
				if (self.data['you']['body'][0]['y'] + i >= self.data['board']['height'] -1):
					print("down hit edge of map")
					break
				#if hit border, add it to possible tiles to move to
				elif ((self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y'] + i) in self.border_matrix):
					possible_tiles.append((self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y'] + i))
					new_directions.append('down')
					break

				i += 1

		if ('left' in self.possible_directions):
			i = 1
			while (True):
				#hit edge of map
				if ((self.data['you']['body'][0]['x'] - i) == 0):
					print("left hit edge of map")
					break
				#if hit border, add it to possible tiles to move to
				elif ((self.data['you']['body'][0]['x'] - i, self.data['you']['body'][0]['y']) in self.border_matrix):
					possible_tiles.append((self.data['you']['body'][0]['x'] - 1, self.data['you']['body'][0]['y']))
					new_directions.append('left')
					break

				i += 1

		if ('right' in self.possible_directions):
			i = 1
			while (True):
				#hit edge of map
				if ((self.data['you']['body'][0]['x'] + i) >= self.data['board']['width'] - 1):
					print("right hit edge of map")
					break
				#if hit border, add it to possible tiles to move to
				elif ((self.data['you']['body'][0]['x'] + i, self.data['you']['body'][0]['y']) in self.border_matrix):
					possible_tiles.append((self.data['you']['body'][0]['x'] + 1, self.data['you']['body'][0]['y']))
					new_directions.append('right')
					break

				i += 1

		if (DEBUG_LOGS):
			print("Current Pos: " + str((self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y'])))
			print("Possible Tiles: " + str(possible_tiles))
			print("Possible Directions: " + str(new_directions))

		if (len(new_directions) <= 1):
			return new_directions

		best_tile_choices, best_direction_choices = self.find_closest_tile_to_enemy(possible_tiles, new_directions)
		
		if (DEBUG_LOGS):
			print("Best to the border direction: " + str(best_direction_choices))

		return best_direction_choices

		"""
		smallest_distances = []
		smallest_tiles = []
		smallest_directions = []

		i = 0
		while (i < len(possible_tiles)):
			distance = get_distance_between_points(possible_tiles[i], (self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y']))

			if (len(smallest_distances) == 0 or distance < smallest_distances[0]):
				smallest_distances = []
				smallest_tiles = []
				smallest_directions = []

				smallest_distances.append(distance)
				smallest_tiles.append(possible_tiles[i])
				smallest_directions.append(new_directions[i])

			#favour tiles close to enemy heads
			elif (distance == smallest_distances[0]):

				

				smallest_distance_to_enemy = get_distance_between_points(possible_tiles[i], (self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y']))

				for j in range(len(best_tile_choices)):
					distance_to_enemy = get_distance_between_points(best_tile_choices[j], (self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y']))

					#if the new tile is closer than old tile, add it
					if (distance_to_enemy < smallest_distance_to_enemy):
						smallest_distances.append(distance)
						smallest_tiles.append(possible_tiles[i])
						smallest_directions.append(new_directions[i])

			i += 1

		if (DEBUG_LOGS):
			print("smallest_direction: " + str(smallest_directions))

		return smallest_directions
		"""

	def continue_on_border(self):
		possible_border_directions = []
		possible_border_tiles = []
		#check if adjacent tile is part of border paths, add to possible moves, take move that is further from edges
		if ('up' in self.possible_directions and
			((self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y'] - 1) in self.border_matrix)):
			possible_border_directions.append('up')
			possible_border_tiles.append((self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y'] - 1))

		if ('down' in self.possible_directions and 
			((self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y'] + 1) in self.border_matrix)):
			possible_border_directions.append('down')
			possible_border_tiles.append((self.data['you']['body'][0]['x'], self.data['you']['body'][0]['y'] + 1))

		if ('left' in self.possible_directions and
			((self.data['you']['body'][0]['x'] - 1, self.data['you']['body'][0]['y']) in self.border_matrix)):
			possible_border_directions.append('left')
			possible_border_tiles.append((self.data['you']['body'][0]['x'] - 1, self.data['you']['body'][0]['y']))

		if ('right' in self.possible_directions and
			((self.data['you']['body'][0]['x'] + 1, self.data['you']['body'][0]['y']) in self.border_matrix)):
			possible_border_directions.append('right')
			possible_border_tiles.append((self.data['you']['body'][0]['x'] + 1, self.data['you']['body'][0]['y']))

		if (DEBUG_LOGS):
			print("Possible border directions: " + str(possible_border_directions))

		if (len(possible_border_directions) <= 1):
			return possible_border_directions

		#favour tiles closer to other snakes heads, using direct distance not tile based distance

		best_tile_choices, best_direction_choices = self.find_closest_tile_to_enemy(possible_border_tiles, possible_border_directions)
		if (DEBUG_LOGS):
			print("Best border direction: " + str(best_direction_choices))

		return best_direction_choices

		"""
		smallest_distance = get_distance_between_points(possible_border_tiles[0], (self.data['board']['width'] // 2, self.data['board']['height'] // 2))
		smallest_tile = possible_border_tiles[0]
		smallest_direction = possible_border_directions[0]

		i = 1
		while (i < len(possible_border_tiles)):
			distance = get_distance_between_points(possible_border_tiles[i], (self.data['board']['width'] // 2, self.data['board']['height'] // 2))

			if (distance < smallest_distance):
				smallest_distance = distance
				smallest_tile = possible_border_tiles[i]
				smallest_direction = possible_border_directions[i]

			i += 1

		return smallest_direction
		"""


	def find_closest_tile_to_enemy(self, possible_tiles, possible_directions):
		closest_tiles = []
		smallest_distances = []
		closest_directions = []
		
		#determine closest opposing snake
		for i in range(len(self.data['board']['snakes'])):
			if (self.data['board']['snakes'][i]['id'] == self.data['you']['id']):
				continue #skip self

			temp_data = copy.deepcopy(self.data)

			lost_head = temp_data['board']['snakes'][i]['body'].pop(0)

			temp_data['board']['snakes'][i]['head'] = temp_data['board']['snakes'][i]['body'][0]

			aStar, walls = init_astar(temp_data, False, self.growing)

			print("Snake: " + str(self.data['board']['snakes'][i]['name']))
			j = 0
			while (j < len(possible_tiles)):

				path = None

				aStar.reset_grid_and_start((possible_tiles[j]), (self.data['board']['snakes'][i]['body'][0]['x'], self.data['board']['snakes'][i]['body'][0]['y']))
				path = aStar.solve()

				if (path == None):
					j += 1
					continue

				distance =  len(path)

				if (DEBUG_LOGS):
					print("Tile: " + str(possible_tiles[j]) + " distance: " + str(distance))

				if (len(smallest_distances) == 0 or distance < smallest_distances[0]):
					closest_tiles = []
					smallest_distances = []
					closest_directions = []

					smallest_distances.append(distance)
					closest_tiles.append(possible_tiles[j])
					closest_directions.append(possible_directions[j])

				elif(distance == smallest_distances[0]):

					direct_distance_old = math.sqrt(((closest_tiles[0][0] - self.data['board']['snakes'][i]['body'][0]['x']) ** 2) + ((closest_tiles[0][1] - self.data['board']['snakes'][i]['body'][0]['y']) ** 2))
					direct_distance_new = math.sqrt(((possible_tiles[j][0] - self.data['board']['snakes'][i]['body'][0]['x']) ** 2) + ((possible_tiles[j][1] - self.data['board']['snakes'][i]['body'][0]['y']) ** 2))
				
					if (DEBUG_LOGS):
						print("Tile: " + str(possible_tiles[j]) + " distance old: " + str(direct_distance_old) + " distance new: " + str(direct_distance_new))

					if (direct_distance_new < direct_distance_old):
						closest_tiles = []
						smallest_distances = []
						closest_directions = []

						smallest_distances.append(distance)
						closest_tiles.append(possible_tiles[j])
						closest_directions.append(possible_directions[j])


				j += 1

		return closest_tiles, closest_directions

	def return_as_list_item(self, direction):
		return_direction = []
		return_direction.append(direction)

		return return_direction

	def get_final_direction(self):
		self.get_border_matrix()

		#if not in border, find best path to border
		if (not self.in_border):
			to_border_directions = self.get_direction_to_area_border()
			return to_border_directions

		border_directions = self.continue_on_border()

		return border_directions


def get_direction_to_protect_area(area_matrix, data, possible_directions, growing):

	protected = ProtectArea(area_matrix, data, possible_directions, growing)

	area_protect_direction = protected.get_final_direction()

	return area_protect_direction
