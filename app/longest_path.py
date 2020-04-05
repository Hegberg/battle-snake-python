

class LongestPath(object):
	def __init__(self, data, first_space, traversable_area):
		self.data = data
		self.first_space = first_space
		self.traversable_area = traversable_area #dictionary of useable spaces
		self.closest_tail = self.find_closest_tail()

	def get_longest_path(self):

		longest_path = self.depth_first_search(self.traversable_area, self.first_space)

		print("Longest Path from location: " + str(self.first_space))
		print("Longest Path: " + str(longest_path))

		return longest_path

	def find_closest_tail(self):
		closest_tail = None
		closest_distance = None
		print("first_space: " + str(self.first_space))
		for i in range(len(self.data['board']['snakes'])):
			tail = self.data['board']['snakes'][i]['body'][len(self.data['board']['snakes'][i]['body']) - 1]
			print("Tail: " + str(tail))
			distance = self.get_distance_between_points((tail['x'], tail['y']), self.first_space)
			if (closest_tail == None):
				closest_tail = (tail['x'], tail['y'])
				closest_distance = distance

			elif (closest_distance > distance):
				closest_tail = (tail['x'], tail['y'])
				closest_distance = distance

			#if distances, are the same, and one is own tail, choose own tail
			elif (closest_distance == distance):
				if (tail == self.data['you']['body'][len(self.data['you']['body']) - 1]):
					closest_distance = distance
					closest_tail = (tail['x'], tail['y'])

		return closest_tail


	#find longest path, if tie, choose path closest to tail
	def depth_first_search(self, matrix, location):

		#if already visited or does not exist, return no path
		if (not (location[0],location[1]) in matrix):
			return []
		if (matrix[location[0]][location[1]] != 0):
			return []

		matrix[location[0]][location[1]] = 1
		longest_path_addition = []

		#get longest path from among neighbours
		self.check_new_point(matrix, (location[0] + 1, location[1]), longest_path_addition)
		self.check_new_point(matrix, (location[0] - 1, location[1]), longest_path_addition)
		self.check_new_point(matrix, (location[0], location[1] + 1), longest_path_addition)
		self.check_new_point(matrix, (location[0], location[1] - 1), longest_path_addition)

		#attach current location onto front of path, return
		longest_path_addition.insert(0, location)
		return longest_path_addition


	def get_distance_between_points(self, point_1, point_2):
		return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])


	def check_new_point(self, matrix, location, longest_path_addition):

		if ((location[0], location[1]) in matrix and matrix[location[0]][location[1]] == 0):
			new_matrix = matrix.copy()
			path_addition = self.depth_first_search(new_matrix, (location[0], location[1]))

			if (len(path_addition) > len(longest_path_addition)):
				longest_path_addition = path_addition
			#if same distance, find path with closer ending to closest tail
			elif(len(path_addition) > 0 and (len(path_addition) == len(longest_path_addition))):
				if (self.get_distance_between_points(path_addition[len(path_addition) - 1], self.closest_tail) > 
					self.get_distance_between_points(longest_path_addition[len(longest_path_addition) - 1], self.closest_tail)):
					longest_path_addition = path_addition



def find_longest_path(data, first_space, traversable_area):
	long_path = LongestPath(data, first_space, traversable_area)

	return long_path.get_longest_path()