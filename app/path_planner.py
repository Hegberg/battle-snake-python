
from queue import PriorityQueue

class State(object):
    def __init__(self, value, parent, start = 0, goal = 0):
        self.children = [] #list off all possabilities
        self.parent = parent #current parent
        self.value = value #current value
        self.dist = 0 #current distance, not actually set just placeholder, hence meant to be substate
        
        #check if parent is plucked in
        if parent:
            self.start = parent.start #store stare
            self.goal = parent.goal #store goal
            self.path = parent.path[:] #copy path

            self.path.append(value) #store all value into path
        
        #if no parent
        else:
            self.path = value #set a path with list of objects starting at current value
            self.start = start #store start
            self.goal = goal #store goal

    #two empty functions defined in sub class
    def get_distance(self):
        pass

    def create_children(self):
        pass

class State_String(State):
    def __init__(self, value, parent, start = 0, goal = 0):
        super(State_String, self).__init__(value, parent, start, goal) #create constructor

        self.dist = self.get_distance() #overwrite distace

    def get_distance(self):
        #check to see if reached goal, if so return 0
        if self.value = self.goal:
            return 0

        dist = 0

        #define loop to go through each letter of goal
        for i in range(len(self.goal)):
            letter = self.goal[i] #get current letter
            dist += abs(i - self.value.index(letter)) #find index of letter in current value
            
            #this will give distance of letter from current target

        return dist

    def create_children(self):
        #if no children then go and generate new children
        #extra precuation to not duplicate children

        if not self.children:
            for i in range(len(self.goal) - 1): #go through every possible arrangement of letter
                val = self.value
                
                #switching second letter and first letter of every pair
                #and we track on the beginning and track on the end and the we have a new arrangement of the letter
                val = val[:i] + val[i+1] + val[i] + val[i+2:]

                #create child and store the value of the child and pass self to store the parent
                child = State_String(val, self)
                self.children.append(child) #add this child to children list

class A_Star_Solver:
    def __init__(self, start, goal):
        self.path = [] #store final solution from start start to goal state
        self.visited_queue = [] #keeps track of all the children that are visited
        self.priority_queue = PriorityQueue()
        self.start = start #store start state
        self.goal = goal #store goal state

    def solve(self):
        start_state = State_String(self.start, 0, self.start, self.goal) #no current parent state

        count = 0

        #priority_queue.put() os used to add children, have to pass tuple inside it
        #tuple contain 0, count and start_state, 0 is priority number we want
        slef.priority_queue.put((0, count, start_state))

        #loop contains all the magic
        while(not self.path and self.priority_queue.qsize()):
            closest_child = self.priority_queue.get()[2] #get topmost value from queue

            closest_child.create_children()
            self.visited_queue.append(closest_child.value) #keep track of visited children
            
            for child in closest_child.children:
                if (child.value not in self.visited_queue):
                    count += 1
                    if not child.dist:
                        self.path = child.path
                        break

                    self.priority_queue.put((child.dist, count, child))

        if (not self.path):
            print("Goal not possible: " + self.goal)

        return self.path


def find_path(start, goal):
    a = A_Star_Solver(start, goal)
    a.solve()

    for i in range(len(a.path)):
        print("Path: " + a.path[i])

    return a.path

