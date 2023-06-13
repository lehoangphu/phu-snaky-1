from peterpath import Location
class KnightEntry:
    def __init__(self,location,history)-> None:
        self.location = location
        self.history = history
        
class KnightFinding:
    def __init__(self,startLoc,destination,width,height) -> None:
        self.startLoc = startLoc
        self.destination = destination
        self.width = width
        self.height = height
        self.KnightEntryList = []
        self.visited = []
    def getpossiblemoves(self,position):
        moves = [
            Location(position.x+1, position.y+2),
            Location(position.x-1, position.y+2),
            Location(position.x-2, position.y+1),
            Location(position.x-2, position.y-1),
            Location(position.x-1, position.y-2),
            Location(position.x+1, position.y-2),
            Location(position.x+2, position.y-1),
            Location(position.x+2, position.y+1)
        ]
        validMoves = []
        for spot in moves:
            if self.isValidLocation(spot):
                validMoves.append(spot)
        return validMoves
    
    def isValidLocation(self,position):
        if position.x < 0 or position.x > self.width-1:
            return False
        elif position.y < 0 or position.y > self.height-1:
            return False
        else:
            return True
    
    def findingpath(self):
        self.KnightEntryList.append(KnightEntry(self.startLoc,[]))
        while len(self.KnightEntryList) > 0:
            current = self.KnightEntryList.pop(0)
            if current.location ==  self.destination:
                current.history.append(self.destination)
                return current.history
            if not self.isVisited(current.location):
                self.visited.append(current.location)
            possiblemoves = self.getpossiblemoves(current.location)
            for move in possiblemoves:
                newentry = KnightEntry(move,current.history.copy())
                newentry.history.append(current.location)
                self.KnightEntryList.append(newentry)

    def isVisited(self,newlocation):
        for location in self.visited:
            if location == newlocation:
                return True
        return False

def basictest1():
    startLoc = Location(0,0)
    destination = Location(7,7)
    finder = KnightFinding(startLoc,destination,8,8)
    print(finder.findingpath())

if __name__ == "__main__":
    basictest1()