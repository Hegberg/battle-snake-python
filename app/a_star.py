import heapq


class Cell(object):
    def __init__(self, x, y, reachable):
        """Initialize new cell.
        @param reachable is cell reachable? not a wall?
        @param x cell x coordinate
        @param y cell y coordinate
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



class AStar(object):
    def __init__(self):
        # open list
        self.opened = []
        heapq.heapify(self.opened)
        # visited cells list
        self.closed = set()
        # grid cells
        self.cells = []
        self.grid_height = None
        self.grid_width = None

    def init_grid(self, width, height, walls, start, end):
        """Prepare grid cells, walls.
        @param width grid's width.
        @param height grid's height.
        @param walls list of wall x,y tuples.
        @param start grid starting point x,y tuple.
        @param end grid ending point x,y tuple.
        """
        self.grid_height = height
        self.grid_width = width
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                #print(str(x) + " " + str(y) + " " + str(reachable))
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(*start)
        self.end = self.get_cell(*end)

    def reset_grid(self, end):
        """Reset grid cells and set new goal"""
        for i in range(len(self.cells)):
            self.cells[i].g = 0
            self.cells[i].h = 0
            self.cells[i].f = 0
            self.cells[i].parent = None

        self.opened = []
        heapq.heapify(self.opened)
        
        self.closed = set()

        self.end = self.get_cell(*end)

    def set_ending_for_init_grid(self, end):
        """Only use for unsued grids setting a new goal"""
        self.end = self.get_cell(*end)

    def reset_grid_and_start(self, start, end):
        """Reset grid cells and set new goal and start location"""
        self.reset_grid(end)
        self.start = self.get_cell(*start)

    def reset_grid_and_remove_wall(self, start, end, wall):
        """Reset grid cells and set new goal and start location"""
        self.reset_grid(end)
        self.start = self.get_cell(*start)
        self.remove_wall(*wall)

    def add_wall(self, wall):
        self.add_wall_x_y(*wall)

    def get_heuristic(self, cell):
        """Compute the heuristic value H for a cell.
        Distance between this cell and the ending cell multiply by 10.
        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        """Returns a cell from the cells list.
        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_height + y]

    def add_wall_x_y(self, x, y):
        """Removes a cell reachable from the cells list.
        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        self.cells[x * self.grid_height + y].reachable = False

    def remove_wall(self, x, y):
        """Adds a cell reachable from the cells list.
        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        self.cells[x * self.grid_height + y].reachable = True

    def get_adjacent_cells(self, cell):
        """Returns adjacent cells to a cell.
        Clockwise starting from the one on the right.
        @param cell get adjacent cells for this cell
        @returns adjacent cells list.
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def get_path(self):
        cell = self.end
        path = [(cell.x, cell.y)]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        """Update adjacent cell.
        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def solve(self):
        """Solve maze, find path to ending cell.
        @returns path or None if not found.
        """
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, return found path
            if cell is self.end:
                return self.get_path()
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))


def init_astar(data, with_own_head_blocking = False, growing = False, snake_growing_index = -1):
    aStar = AStar()
    
    walls = []

    large_size_head_list = []

    start_point = 1
    if (with_own_head_blocking):
        start_point = 0

    for i in range(start_point, len(data['you']['body'])):
        #ignore own tail
        if (i == len(data['you']['body']) - 1):
            continue

        #ignore own grown tail if growing
        if (growing and i == len(data['you']['body']) - 2):
            continue

        walls.append((data['you']['body'][i]['x'], data['you']['body'][i]['y']))

    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == data['you']['id']):
            continue #skip self

        for j in range(len(data['board']['snakes'][i]['body'])):
            #if tail, don't count as wall
            if (j == len(data['board']['snakes'][i]['body']) - 1):
                continue

            #ignore snake grown tail
            if ((snake_growing_index == i) and j == len(data['board']['snakes'][i]['body']) - 2):
                #print("ignoring extra snake tial: " + str((data['board']['snakes'][i]['body'][j]['x'], data['board']['snakes'][i]['body'][j]['y'])))
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

def init_astar_with_custom_snake(data, self_new_body, snake_body_id, goal, extra_walls = [], growing = False, snake_growing_index = -1):
    aStar = AStar()
    
    walls = []

    start_point = 1

    for i in range(len(extra_walls)):
        walls.append((extra_walls[i][0], extra_walls[i][1]))

    #skip adding own head with start point
    for i in range(start_point, len(self_new_body)):
        #ignore own tail
        if (i == len(self_new_body) - 1):
            continue

        #ignore own grown tail if growing
        if (growing and i == len(self_new_body) - 2):
            continue

        walls.append((self_new_body[i]['x'], self_new_body[i]['y']))

    for i in range(len(data['board']['snakes'])):
        if (data['board']['snakes'][i]['id'] == snake_body_id):
            continue #skip self

        for j in range(len(data['board']['snakes'][i]['body'])):
            #if tail, don't count as wall
            if (j == len(data['board']['snakes'][i]['body']) - 1):
                continue

            #ignore snake grown tail
            if ((snake_growing_index == i) and j == len(data['board']['snakes'][i]['body']) - 2):
                continue

            walls.append((data['board']['snakes'][i]['body'][j]['x'], data['board']['snakes'][i]['body'][j]['y']))


    #print("Obstacles in board: " + str(walls))

    #init astar with new board, set end goal as temp value
    x = self_new_body[0]['x']
    y = self_new_body[0]['y']
    current_position = (x, y)
    aStar.init_grid(data['board']['width'], data['board']['height'], walls, current_position, goal)

    return aStar, walls