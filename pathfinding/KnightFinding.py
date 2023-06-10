from peterpath import Location
class KnightFinding:
    def __init__(self,startLoc,destination,width,height) -> None:
        self.startLoc = startLoc
        self.destination = destination
        self.width = width
        self.height = height
        self.data = []
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
        self.data.append(self.startLoc)
        print(self.getpossiblemoves(self.startLoc))
        


def basictest1():
    startLoc = Location(3,3)
    destination = Location(7,7)
    finder = KnightFinding(startLoc,destination,8,8)
    finder.findingpath()

if __name__ == "__main__":
    basictest1()