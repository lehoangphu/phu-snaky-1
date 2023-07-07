class Location:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    def __repr__(self) -> str:
        retString = "(" + str(self.x) + ", " + str(self.y) + ")"
        return retString
    def __eq__(self, object) -> bool:
        if self.x == object.x and self.y == object.y:
            return True
        else:
            return False
    def get_distance(self, location):
        return abs(self.x - location.x) + abs(self.y - location.y)

        
class PathEntry:
    def __init__(self, snake, history) -> None:
        self.snake = snake 
        self.history = history
    def get_cost(self, destination):
        return self.snake[0].get_distance(destination) + len(self.history)

class PathFinder:
    def __init__(self, snake, destination, obstacles, width, height) -> None:
        self.data = []
        self.snake = snake
        self.destination = destination
        self.obstacles = obstacles
        self.width = width
        self.height = height
    
    def addPathData(self, oldEntry, newlocation):
        if (self.isValidLocation(newlocation)):
            visited = False
            for oldLoc in oldEntry.history:
                if newlocation == oldLoc:
                    visited = True
            if not visited:
                newSnake = oldEntry.snake.copy()
                newSnake.insert(0, newlocation)
                newSnake.pop(len(newSnake)-1)
                newHistory = oldEntry.history.copy()
                newHistory.append(oldEntry.snake[0])
                newEntry = PathEntry(newSnake, newHistory)
                self.data.append(newEntry)

    def findthepath(self):
        startEntry = PathEntry(self.snake, [])
        self.data.append(startEntry)

        while len(self.data) > 0:
            current = self.data.pop(0)
            if current.snake[0] == self.destination:
                current.history.append(self.destination)
                # print("Found a path")
                return current.history
                break
        
            uplocation = Location(current.snake[0].x, current.snake[0].y+1)
            downlocation = Location(current.snake[0].x, current.snake[0].y-1)
            leftlocation = Location(current.snake[0].x-1, current.snake[0].y)
            rightlocation = Location(current.snake[0].x+1, current.snake[0].y)

            self.addPathData(current, uplocation)
            self.addPathData(current, downlocation)
            self.addPathData(current, leftlocation)
            self.addPathData(current, rightlocation)

    def isValidLocation(self, location):
        if location.x < 0 or location.x > self.width-1:
            return False
        if location.y < 0 or location.y > self.height-1:
            return False
        for obstacles in self.obstacles:
            if obstacles == location:
                return False
        for i in range(len(self.snake)-1):
            if self.snake[i] == location:
                return False
        return True
    def isVisited(self, newlocation):
        for location in self.visited:
            if location == newlocation:
                return True
        return False

def basicTest1():
    snake = [
        Location(0,0),
        Location(1,0),
        Location(2,0),
        Location(3,0)
    ]
    destination = Location(8,8)
    obstacles = [
        Location(4, 0),
        Location(4, 1),
        Location(4, 2),
        Location(4, 3),
        Location(4, 4),
        Location(4, 5),
        Location(4, 6),
        Location(4, 7),
        Location(4, 8),
        Location(4, 9)
    ]
    finder = PathFinder(snake, destination, obstacles, 11, 11)
    
    print(finder.findthepath())

if __name__ == "__main__":
    basicTest1()
