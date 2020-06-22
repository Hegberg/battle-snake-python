from app.common import DEBUG_LOGS

class LongestPath(object):
	def __init__(self, data, first_space, traversable_area):
		self.data = data
		self.first_space = first_space
		self.traversable_area = traversable_area.copy() #dictionary of useable spaces
		self.closest_tail, self.tail_owner_index = self.find_closest_tail()

	def get_longest_path(self):

		#if first place is right beside tail, use
		if (self.check_if_beside_tail([self.first_space], 1)):
			return [self.first_space]

		longest_path = self.depth_first_search(self.traversable_area, self.first_space, 1)

		return longest_path

	def find_closest_tail(self):
		closest_tail = None
		closest_distance = None
		tail_owner_index = None
		for i in range(len(self.data['board']['snakes'])):
			#grab tail from where it will be once area is traversed

			#no valid space to search
			if (len(self.traversable_area) == 0):
				tail = self.data['board']['snakes'][i]['body'][len(self.data['board']['snakes'][i]['body']) - 1]
			elif (len(self.data['board']['snakes'][i]['body']) > len(self.traversable_area)):
				tail = self.data['board']['snakes'][i]['body'][len(self.data['board']['snakes'][i]['body']) - len(self.traversable_area)]
			else:
				#path is longer than snake, so use it's head as future tail position
				tail = self.data['board']['snakes'][i]['body'][0]

			distance = self.get_distance_between_points((tail['x'], tail['y']), self.first_space)
			if (closest_tail == None):
				closest_tail = (tail['x'], tail['y'])
				closest_distance = distance
				tail_owner_index = i

			elif (closest_distance > distance):
				closest_tail = (tail['x'], tail['y'])
				closest_distance = distance
				tail_owner_index = i

			#if distances, are the same, and one is own tail, choose own tail
			elif (closest_distance == distance):
				if (tail == self.data['you']['body'][len(self.data['you']['body']) - 1]):
					closest_distance = distance
					closest_tail = (tail['x'], tail['y'])
					tail_owner_index = i


		#print(closest_tail)

		return closest_tail, tail_owner_index


	#find longest path, if tie, choose path closest to tail
	def depth_first_search(self, matrix, location, depth):
		#print("Traversable matrix: " + str(matrix))
		#print("location: " + str(location))

		#if already visited or does not exist, return no path
		if (not (location[0],location[1]) in matrix):
			return []
		if (matrix[(location[0],location[1])] != 0):
			return []

		matrix[(location[0],location[1])] = 1
		longest_path_addition = []

		#print("Location: " + str(location) + " depth: " + str(depth))

		#get longest path from among neighbours
		#new_matrix = matrix.copy()
		path_addition = self.depth_first_search(matrix, (location[0] + 1, location[1]), depth + 1)
		#print("Location after right: " + str(location) + " depth: " + str(depth))
		longest_path_addition = self.check_new_path(path_addition, longest_path_addition, depth)

		#new_matrix = matrix.copy()
		path_addition = self.depth_first_search(matrix, (location[0] - 1, location[1]), depth + 1)
		#print("Location after left: " + str(location) + " depth: " + str(depth))
		longest_path_addition = self.check_new_path(path_addition, longest_path_addition, depth)

		#new_matrix = matrix.copy()
		path_addition = self.depth_first_search(matrix, (location[0], location[1] + 1), depth + 1)
		#print("Location after up: " + str(location) + " depth: " + str(depth))
		longest_path_addition = self.check_new_path(path_addition, longest_path_addition, depth)

		#new_matrix = matrix.copy()
		path_addition = self.depth_first_search(matrix, (location[0], location[1] - 1), depth + 1)
		#print("Location after down: " + str(location) + " depth: " + str(depth))
		longest_path_addition = self.check_new_path(path_addition, longest_path_addition, depth)

		#attach current location onto front of path, return
		longest_path_addition.insert(0, location)
		#print("Longest path addition: " + str(longest_path_addition) + " for location: " + str(location))
		return longest_path_addition


	def get_distance_between_points(self, point_1, point_2):
		return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])


	def check_new_path(self, path_addition, longest_path_addition, depth):
		#if adjacent to a tail, count as valid path and return
		if (self.check_if_beside_tail(path_addition, depth)):
			return path_addition

		if (len(path_addition) > len(longest_path_addition)):
			longest_path_addition = path_addition
		#if same distance, find path with closer ending to closest tail
		elif(len(path_addition) > 0 and (len(path_addition) == len(longest_path_addition))):
			if (self.get_distance_between_points(path_addition[len(path_addition) - 1], self.closest_tail) > 
				self.get_distance_between_points(longest_path_addition[len(longest_path_addition) - 1], self.closest_tail)):
				longest_path_addition = path_addition

		#print("new longest path: " + str(longest_path_addition))
		return longest_path_addition
		
	def check_if_beside_tail(self, path_addition, depth):
		if (len(path_addition) == 0):
			return False 
		for i in range(len(self.data['board']['snakes'])):
			if (len(self.data['board']['snakes'][i]['body']) - 1 - depth >= 0):
				tail_instance = self.data['board']['snakes'][i]['body'][len(self.data['board']['snakes'][i]['body']) - 1 - depth]
			else:
				tail_instance = self.data['board']['snakes'][i]['body'][0]
			#if new path addition is beside tail, return true
			if (self.get_distance_between_points(path_addition[0], (tail_instance['x'], tail_instance['y'])) == 1):
				self.closest_tail = (tail_instance['x'], tail_instance['y'])
				self.tail_owner_index = i
				return True
		return False


def find_longest_path(data, first_space, traversable_area):
	long_path = LongestPath(data, first_space, traversable_area)

	return long_path.get_longest_path(), long_path.closest_tail, long_path.tail_owner_index