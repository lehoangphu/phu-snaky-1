import random
import typing
from pathfinding.location import Location
from pathfinding.findapath import find_a_path
import json
from pathlib import Path
import time
import os


def info_peter():
    return {
        "apiversion": "1",
        "author": "Peter",  # TODO: Your Battlesnake Username
        "color": "#000000",  # TODO: Choose color
        "head": "all-seeing",  # TODO: Choose head
        "tail": "flytrap",  # TODO: Choose tail
    }

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move_peter(game_state: typing.Dict) -> typing.Dict:
    # informational only: start the timer
    start_time = time.time()
    print("Turn: ", game_state["turn"])

    # informational only: Log the turn to a file
    deployment_mode = os.environ.get("deployment_mode")
    if deployment_mode != "production":
        logFileName = "logs/peterturn_" + str(game_state["turn"]) + ".json"
        logFilePath = Path(__file__).parent / logFileName
        json_file = open(logFilePath, "w")
        json.dump(game_state, json_file, indent=4)
        json_file.close()
    
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    my_body = game_state['you']['body']
    my_tail = game_state['you']['body'][len(my_body)-1]
    opponents = game_state['board']['snakes']

    foods = game_state['board']['food']
    


    startLoc = Location(my_head["x"],my_head["y"])
    tailLoc = Location(my_tail["x"], my_tail["y"])

    obstacles = []
    for snake in opponents:
        for position in snake["body"]:
            obstacles.append(Location(position["x"],position["y"]))
    
    for part in my_body:
        obstacles.append(Location(part["x"], part["y"]))
    
    print("obstacles: ", obstacles)

    foodpath = None
    for food in foods:
        foodLoc = Location(food["x"], food["y"])
        foodpath = find_a_path(startLoc, foodLoc, obstacles)
        if foodpath != None:
            break
    
    tailpath = None
    if foodpath == None:
        tailpath = find_a_path(startLoc,tailLoc, obstacles)
    if foodpath != None:
        current = foodpath[0]
        nextmove = foodpath[1]
    elif tailpath != None:
        current = tailpath[0]
        nextmove = foodpath[1]

    print("elapsed time: ", (time.time() - start_time) * 1000)
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