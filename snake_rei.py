import random
import typing
import json
from pathlib import Path
import os
import time

author_name = "Rei"

def info():
    return {
        "apiversion": "1",
        "author": author_name,  # TODO: Your Battlesnake Username
        "color": "#cc66ff",  # TODO: Choose color
        "head": "dead",  # TODO: Choose head
        "tail": "present",  # TODO: Choose tail
    }

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    # informational only: start the timer
    start_time = time.time()
    print("Turn: ", game_state["turn"])

    # informational only: Log the turn to a file
    deployment_mode = os.environ.get("deployment_mode")
    if deployment_mode != "production":
        logFileName = "logs/" + author_name + "turn_" + str(game_state["turn"]) + ".json"
        logFilePath = Path(__file__).parent / logFileName
        json_file = open(logFilePath, "w")
        json.dump(game_state, json_file, indent=4)
        json_file.close()

    # snake's logic starts here
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width-1:
        is_move_safe["right"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    if my_head["y"] == board_height-1:
        is_move_safe["up"]

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    for part in my_body:
        if my_head["x"]+1 == part["x"] and my_head["y"] == part["y"]:
            is_move_safe["right"] = False
        if my_head["x"]-1 == part["x"] and my_head["y"] == part["y"]:
            is_move_safe["left"] = False
        if my_head["y"]+1 == part["y"] and my_head["x"] == part["x"]:
            is_move_safe["up"] = False
        if my_head["y"]-1 == part["y"] and my_head["x"] == part["x"]:
            is_move_safe["down"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # Are there any safe moves left?
    safe_moves = []
    for move, is_safe in is_move_safe.items():
        if is_safe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # Step 4 - Move towards food instead of random, to regain health and survive longer
    

    print(f"MOVE {game_state['turn']}: {next_move}")
    print("elapsed time: ", (time.time() - start_time) * 1000)
    return {"move": next_move}

if __name__ == "__main__":
    dataFileName = "snake_"+author_name+".json"
    dataFilePath = Path(__file__).parent / dataFileName
    rhandle = open(dataFilePath, "r")

    gamestate = json.load(rhandle)
    rhandle.close()
    print(move(gamestate))