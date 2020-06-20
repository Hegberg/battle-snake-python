import copy

class Cell(object):
	def __init__(self, x, y, snake_index = -1, snake_head = 0):
		"""Initialize new cell.
		@param x cell x coordinate
		@param y cell y coordinate
		@param snake_index is index of snake in data list, - 1 for no snake
		@param snake_head, 1 = snake_head, 2 = snake_body, 0 = blank_space

		@param g cost to move from the starting cell to this cell.
		@param h estimation of the cost to move from this cell
				 to the ending cell.
		@param f f = g + h
		"""
		self.reachable = reachable
		self.x = x
		self.y = y
		self.parent = None
		self.g = 0
		self.h = 0
		self.f = 0

	def __lt__(self, other):
		if (self.f < other.f):
			return True

		return False

	def __le__(self, other):
		if (self.f <= other.f):
			return True

		return False

class MovingPathPlanning(object):
	"""docstring for MovingPathPlanning"""
	def __init__(self, data, matrix, walls, aStar, tile_order_queue):
		self.visited = []
		self.data = copy.deepcopy(data)
		self.matrix = matrix
		self.walls = walls
		self.aStar = aStar
		self.tile_order_queue = tile_order_queue

	def flood_fill_recursive():
		while (len(tile_order_queue) > 0):
			matrix = flood_fill_tile_check()

		return matrix

	def flood_fill_tile_check():
		x = self.tile_order_queue[0][0]
		y = self.tile_order_queue[0][1]

		#if item in queue has unique number grab it, otherwise assume default
		if (len(self.tile_order_queue[0]) > 2):
			number_fill = self.tile_order_queue[0][2]
		else:
			number_fill = 2

		self.tile_order_queue.pop(0)

		if (self.matrix[x][y] == 0):
			if (number_fill == 2):
				between_walls = check_if_location_in_between_walls(self.data, self.aStar, self.walls, (x,y))
				#if between walls, check if opposing snake is close enough to cut off from that point, if so, remove option from floodfill
				if(between_walls):
					return self.matrix

			self.matrix[x][y] = number_fill

			if (x > 0):
				self.tile_order_queue.append((x-1, y, number_fill))
			if (x < len(matrix[y]) - 1):
				self.tile_order_queue.append((x+1, y, number_fill))
			if (y > 0):
				self.tile_order_queue.append((x, y-1, number_fill))
			if (y < len(matrix) - 1):
				self.tile_order_queue.append((x, y+1, number_fill))

			return self.matrix
		return self.matrix