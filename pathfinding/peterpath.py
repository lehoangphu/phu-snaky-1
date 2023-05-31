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
    def __init__(self, location) -> None:
        self.location = location
        self.history = []
        self.cost = 0

class PathFinder:
    def __init__(self, startLoc, destination, obstacles, width, height) -> None:
        self.data = []
        self.startLoc = startLoc
        self.destination = destination
        self.obstacles = obstacles
        self.width = width
        self.height = height
        self.visited = []
    
    def addPathData(self, oldEntry, newlocation):
        if (self.isValidLocation(newlocation)):
            newEntry = PathEntry(newlocation)
            newEntry.history = oldEntry.history.copy()
            newEntry.history.append(oldEntry.location)
            self.data.append(newEntry)

    def findthepath(self):
        startEntry = PathEntry(self.startLoc)
        self.data.append(startEntry)

        while len(self.data) > 0:
            current = self.data.pop(0)
            if current.location == self.destination:
                current.history.append(self.destination)
                # print("Found a path")
                return current.history
                break
            if not self.isVisited(current.location):
                self.visited.append(current.location)
                uplocation = Location(current.location.x, current.location.y+1)
                downlocation = Location(current.location.x, current.location.y-1)
                leftlocation = Location(current.location.x-1, current.location.y)
                rightlocation = Location(current.location.x+1, current.location.y)

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
        return True
    def isVisited(self, newlocation):
        for location in self.visited:
            if location == newlocation:
                return True
        return False

def basicTest1():
    startLoc = Location(0,0)
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
    finder = PathFinder(startLoc, destination, obstacles, 11, 11)
    
    finder.findthepath()

if __name__ == "__main__":
    basicTest1()
