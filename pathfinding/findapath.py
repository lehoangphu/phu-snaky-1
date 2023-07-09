def find_a_path(startLoc, endLoc, obstacles):
    finder = PathFinder(startLoc, endLoc, obstacles, 11, 11)
    return finder.findthepath()
     
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
    start = {"x": 0, "y": 0}
    end = {"x": 8, "y": 8}
    snakes = [
        {
          "id": "snake-508e96ac-94ad-11ea-bb37",
          "name": "My Snake",
          "health": 54,
          "body": [
            {"x": 0, "y": 0}, 
            {"x": 1, "y": 0}, 
            {"x": 2, "y": 0}
          ],
          "latency": "111",
          "head": {"x": 0, "y": 0},
          "length": 3,
          "shout": "why are we shouting??",
          "customizations":{
            "color":"#FF0000",
            "head":"pixel",
            "tail":"pixel"
          }
        }, 
        {
          "id": "snake-b67f4906-94ae-11ea-bb37",
          "name": "Another Snake",
          "health": 16,
          "body": [
            {"x": 5, "y": 4}, 
            {"x": 5, "y": 3}, 
            {"x": 6, "y": 3},
            {"x": 6, "y": 2}
          ],
          "latency": "222",
          "head": {"x": 5, "y": 4},
          "length": 4,
          "shout": "I'm not really sure...",
          "customizations":{
            "color":"#26CF04",
            "head":"silly",
            "tail":"curled"
          }
        }
      ]
    
    obstacles = []
    for snake in snakes:
        for position in snake["body"]:
            obstacles.append(Location(position["x"],position["y"]))
    startLoc = Location(start["x"], start["y"])
    endLoc = Location(end["x"], end["y"])

    print(find_a_path(startLoc, endLoc, obstacles))


if __name__ == "__main__":
    # peterpath.py is being run directly
    from location import Location

    # run tests
    basicTest1()
else:
    # peterpath.py is being imported into another script
    from .location import Location