import random
import typing
import json
from pathlib import Path

def info_lucastest():
    return {
        "apiversion": "1",
        "author": "lucastest",
        "color": "#ff0000",
        "head": "tongue",
        "tail": "hook",
    }

def move_lucas(game_state: typing.Dict) -> typing.Dict:
    logFileName = "logs/turn_" + str(game_state["turn"]) + ".json"
    logFilePath = Path(__file__).parent / logFileName
    json_file = open(logFilePath, "w")
    json.dump(game_state, json_file, indent=4)
    json_file.close()

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    my_head = game_state["you"]["body"][0]
    my_neck = game_state["you"]["body"][1]

    if my_neck["x"] < my_head["x"]:
        is_move_safe["left"] = False
    elif my_neck["x"] > my_head["x"]:
        is_move_safe["right"] = False
    elif my_neck["y"] < my_head["y"]:
        is_move_safe["down"] = False
    elif my_neck["y"] > my_head["y"]:
        is_move_safe["up"] = False

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] >= board_width - 1:
        is_move_safe["right"] = False
    if my_head["x"] <= 0:
        is_move_safe["left"] = False
    if my_head["y"] >= board_height - 1:
        is_move_safe["down"] = False
    if my_head["y"] <= 0:
        is_move_safe["up"] = False

    my_body = game_state['you']['body']
    for body_part in my_body[1:]:
        if my_head["y"] - 1 == body_part["y"] and my_head["x"] == body_part["x"]:
            is_move_safe["up"] = False
        elif my_head["y"] + 1 == body_part["y"] and my_head["x"] == body_part["x"]:
            is_move_safe["down"] = False
        elif my_head["x"] - 1 == body_part["x"] and my_head["y"] == body_part["y"]:
            is_move_safe["left"] = False
        elif my_head["x"] + 1 == body_part["x"] and my_head["y"] == body_part["y"]:
            is_move_safe["right"] = False

    opponents = game_state['board']['snakes']
    for snake in opponents:
        for body_part in snake['body']:
            if my_head["y"] - 1 == body_part["y"] and my_head["x"] == body_part["x"]:
                is_move_safe["up"] = False
            elif my_head["y"] + 1 == body_part["y"] and my_head["x"] == body_part["x"]:
                is_move_safe["down"] = False
            elif my_head["x"] - 1 == body_part["x"] and my_head["y"] == body_part["y"]:
                is_move_safe["left"] = False
            elif my_head["x"] + 1 == body_part["x"] and my_head["y"] == body_part["y"]:
                is_move_safe["right"] = False

    safe_moves = [move for move, is_safe in is_move_safe.items() if is_safe]

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Prioritize food over avoiding walls and snakes
    foods = game_state['board']['food']
    if foods:
        distances = []
        for food in foods:
            distance = abs(food["x"] - my_head["x"]) + abs(food["y"] - my_head["y"])
            distances.append(distance)

        min_distance = min(distances)
        nearest_food_index = distances.index(min_distance)
        nearest_food = foods[nearest_food_index]

        if nearest_food["x"] < my_head["x"]:
            safe_moves.remove("right")
        elif nearest_food["x"] > my_head["x"]:
            safe_moves.remove("left")
        elif nearest_food["y"] < my_head["y"]:
            safe_moves.remove("down")
        elif nearest_food["y"] > my_head["y"]:
            safe_moves.remove("up")

    next_move = random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

if __name__ == "__main__":
    dataFilePath = Path(__file__).parent / "snake_lucas_test.json"
    rhandle = open(dataFilePath, "r")

    gamestate = json.load(rhandle)
    rhandle.close()
    print(move_lucastest(gamestate))
