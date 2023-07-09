import time
import logging
from enum import Enum

def find_astar_path(startSnake, endLoc, obstacles):
    finder = AStarFinder(startSnake, endLoc, obstacles, 11, 11, 2)
    return finder.findthepath()
        
class PathEntry:
    def __init__(self, snake) -> None:
        self.snake = snake
        self.history = []
        self.cost = 0

class AStarFinder:
    class PathMode(Enum):
        SIMPLE = 1
        MAX = 2
        FLEXIBLE = 3 
        
    def __init__(self, snake, destination, obstacles, width, height, max_repeat) -> None:
        self.data = []
        self.snake = snake
        self.destination = destination
        self.obstacles = obstacles
        self.width = width
        self.height = height
        self.visited = {}
        self.max_repeat = max_repeat

    def get_new_snake(self, snake, direction):
        new_snake = snake.copy()
        new_snake.pop(len(new_snake)-1)
        if direction == "up":
            new_snake.insert(0, Location(snake[0].x, snake[0].y+1))
        elif direction == "down":
            new_snake.insert(0, Location(snake[0].x, snake[0].y-1))
        elif direction == "left":
            new_snake.insert(0, Location(snake[0].x-1, snake[0].y))
        elif direction == "right":
            new_snake.insert(0, Location(snake[0].x+1, snake[0].y))
        return new_snake
    
    def addPathData(self, oldEntry, new_snake):
        if (self.isValidLocation(new_snake)):
            newEntry = PathEntry(new_snake)
            newEntry.history = oldEntry.history.copy()
            newEntry.history.append(oldEntry.snake[0])
            newEntry.cost = len(newEntry.history) + new_snake[0].get_distance(self.destination)
            self.data.append(newEntry)

    def get_smallest_data_index(self):
        smallest = 0
        for i in range(len(self.data)):
            if self.data[i].cost < self.data[smallest].cost:
                smallest = i
        return smallest

    def findthepath(self):
        path = None
        startEntry = PathEntry(self.snake)
        self.data.append(startEntry)
        pop_counter = 0
        while len(self.data) > 0:
            pop_counter += 1
            current = self.data.pop(self.get_smallest_data_index())
            logging.debug("current cost: %d", current.cost)
            if current.snake[0] == self.destination:
                current.history.append(self.destination)
                path = current.history
                break
            
            process_current = False
            if current.snake[0] in self.visited:
                self.visited[current.snake[0]] += 1
            else:
                self.visited[current.snake[0]] = 1

            if self.visited[current.snake[0]] <= self.max_repeat:
                process_current = True
            
            if process_current:
                self.addPathData(current, self.get_new_snake(current.snake, "up"))
                self.addPathData(current, self.get_new_snake(current.snake, "down"))
                self.addPathData(current, self.get_new_snake(current.snake, "left"))
                self.addPathData(current, self.get_new_snake(current.snake, "right"))
        logging.info("Pop counter: %d", pop_counter)
        if path:
            logging.info("Path length: %d", len(path))
        return path

    def isValidLocation(self, snake):
        if snake[0].x < 0 or snake[0].x > self.width-1:
            return False
        if snake[0].y < 0 or snake[0].y > self.height-1:
            return False
        for obstacles in self.obstacles:
            if obstacles == snake[0]:
                return False
        for i in range(1, len(snake)):
            if snake[0] == snake[i]:
                return False
        return True
    
    def isVisited(self, newlocation):
        for location in self.visited:
            if location == newlocation:
                return True
        return False

def basicTest1():
    start_time = time.time()
    snake = [
        Location(2,8),
        Location(2,9),
        Location(2,10),
        Location(3,10),
        Location(3,9),
        Location(3,8),
        Location(3,7),
        Location(3,6),
        Location(3,5),
        Location(3,4),
        Location(3,3),
        Location(3,2),
        Location(3,1),
        Location(3,0)]

    destination = Location(9,9)
    obstacles = [
    ]
    
    path = find_astar_path(snake, destination, obstacles)
    logging.info(path)
    logging.info("elapsed time: %d", (time.time() - start_time)*1000)

def circleSnake1():
    start_time = time.time()
    snake = [
        Location(3,2),
        Location(3,1),
        Location(3,0),
        Location(2,0),
        Location(1,0),
        Location(0,0),
        Location(0,1),
        Location(0,2),
        Location(0,3),
        Location(0,4),
        Location(1,4),
        Location(2,4),
        Location(3,4),
        Location(4,4),
        Location(4,3),
        Location(4,2),
        Location(4,1),
        Location(4,0)]

    destination = Location(9,9)
    obstacles = [
    ]
    finder = AStarFinder(snake, destination, obstacles, 11, 11, 2)
    
    path = finder.findthepath()
    logging.info(path)
    logging.info("elapsed time: %d", (time.time() - start_time)*1000)

if __name__ == "__main__":
    # peterpath.py is being run directly
    from location import Location

    # run tests
    logging.basicConfig(level=logging.INFO)
    circleSnake1()
else:
    # peterpath.py is being imported into another script
    from .location import Location