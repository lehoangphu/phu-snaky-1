import json
from crow import SimpleApp
from gameinfo import GameInfo, Point, Path

# Constants
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
FOOD = "food"
BUFFER = "buffer"
WALL = "wall"

# Moves List
moveslist = [NORTH, EAST, SOUTH, WEST]

def findFallbackMove(game):
    print("FALL BACK MOVE")
    head = game.snake.getHead()
    posmoves = []
    freevec = []
    
    for m in moveslist:
        p = head.addMove(m)
        
        if p.compare(game.snake.getTail()) and len(game.snake.coords) > 3:
            return m
        
        free = game.getFreeSquares(head, 7)
        
        if game.isValid(p):
            posmoves.append(m)
            freevec.append(free)
    
    if not posmoves:
        print("BUFFER")
        for m in moveslist:
            p = head.addMove(m)
            if game.board.getCoord(p) == BUFFER:
                posmoves.append(m)
    
    if not posmoves:
        print("WALL")
        for m in moveslist:
            p = head.addMove(m)
            if game.board.getCoord(p) == WALL:
                posmoves.append(m)
    
    if not posmoves:
        return 0
    
    max_free = max(freevec)
    max_free_index = freevec.index(max_free)
    return posmoves[max_free_index]


def eat(game, path):
    if len(path.path) > 1:
        return path.getStepDir(0)
    return findFallbackMove(game)


def orbit(game):
    head = game.snake.getHead()
    target = game.getOrbitTarget()
    path = game.astarGraphSearch(head, target)
    if len(path.path) > 1 and len(game.snake.coords) > 3:
        return path.getStepDir(0)
    return findFallbackMove(game)


def findPathToNearestFood(game):
    head = game.snake.getHead()
    path = game.breadthFirstSearch(head, [FOOD], False)
    return path


def moveResponse(dir):
    move = {}
    if dir == NORTH:
        move["move"] = "up"
        move["taunt"] = "THE NORTH REMEMBERS"
    elif dir == EAST:
        move["move"] = "right"
        move["taunt"] = "TO THE EAST"
    elif dir == SOUTH:
        move["move"] = "down"
        move["taunt"] = "SOUTH WHERE ITS WARM"
    elif dir == WEST:
        move["move"] = "left"
        move["taunt"] = "WEST IS BEST"
    
    return json.dumps(move)


def checkFreeSquares(game):
    head = game.snake.getHead()
    print("Free Moves")
    for m in moveslist:
        p = head.addMove(m)
        free = 0
        
        if game.isValid(p):
            free = game.getFreeSquares(p, 10)
        
        print(free, end=" ")
    
    print()


def isClose(game, point, psize, radius):
    for snake in game.snakes:
        if snake.id != game.snake.id:
            if snake.getHead().manDist(point) <= radius:
                return True
    return False


def decideExcecute(game):
    checkFreeSquares(game)
    
    foodpath = findPathToNearestFood(game)
    fsize = len(foodpath.path)
    ssize = len(game.snake.coords)
    
    buffer = 10
    if ssize > 12:
        buffer = 35
    
    if isClose(game, foodpath.getLast(), fsize, 5):
        print("IS CLOSE EAT")
        return eat(game, foodpath)
    
    if len(game.snake.coords) < 10:
        return eat(game, foodpath)
    
    if game.snake.health < (fsize + buffer):
        return eat(game, foodpath)
    
    if fsize > ssize:
        return eat(game, foodpath)
    
    return orbit(game)


def SnakeInfo():
    info = {}
    info["color"] = "#000F00"
    info["head_url"] = "http://pets.wilco.org/Portals/7/Containers/Pets2011/images/star.png"
    info["taunt"] = "C++ is a superior language"
    info["name"] = "leks"
    return json.dumps(info)


def initSnakeApp():
    app = SimpleApp()
    
    # INFO
    @app.route("/")
    def info():
        return SnakeInfo()
    
    # START
    @app.route("/start", methods=["POST"])
    def start():
        return SnakeInfo()
    
    # MOVE
    @app.route("/move", methods=["POST"])
    def move():
        game = GameInfo(request.body)
        move = decideExcecute(game)
        return moveResponse(move)
    
    return app


if __name__ == "__main__":
    import sys
    
    port = 7000
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    
    app = initSnakeApp()
    app.port(port).multithreaded().run()
