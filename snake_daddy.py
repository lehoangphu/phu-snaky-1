import random
import typing
from pathfinding.peterpath import Location
from pathfinding.peterpath import PathFinder
import json
from pathlib import Path

def info_daddy():
    return {
        "apiversion": "1",
        "author": "Daddy",  # TODO: Your Battlesnake Username
        "color": "#333333",  # TODO: Choose color
        "head": "tongue",  # TODO: Choose head
        "tail": "hook",  # TODO: Choose tail
    }

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move_daddy(game_state: typing.Dict) -> typing.Dict:
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    my_body = game_state['you']['body']
    opponents = game_state['board']['snakes']

    food = game_state['board']['food']
    if (len(food) > 0):
        first_food = food[0]


    startLoc = Location(my_head["x"],my_head["y"])
    destination = Location(first_food["x"],first_food["y"])
    obstacles = []
    for snake in opponents:
        for position in snake["body"]:
            obstacles.append(Location(position["x"],position["y"]))
    
    for part in my_body:
        obstacles.append(Location(part["x"], part["y"]))
    
    print("obstacles: ", obstacles)
    finder = PathFinder(startLoc, destination, obstacles, board_width, board_height)
    
    path = finder.findthepath()
    print("path: ", path)
    current = path[0]
    nextmove = path[1]
    if nextmove.x > current.x:
        return {"move":"right"}
    if nextmove.x < current.x:
        return {"move":"left"}
    if nextmove.y > current.y:
        return {"move":"up"}
    if nextmove.y < current.y:
        return {"move":"down"}

    return {"move": "down"}

if __name__ == "__main__":
    dataFilePath = Path(__file__).parent / "snake_peter.json"
    rhandle = open(dataFilePath, "r")

    gamestate = json.load(rhandle)
    rhandle.close()
    print(move_peter(gamestate))