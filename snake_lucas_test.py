import random
import typing
import json
from pathlib import Path

def info_lucastest():
    return {
        "apiversion": "1",
        "author": "lucastest",  # TODO: Your Battlesnake Username
        "color": "#ff0000",  # TODO: Choose color
        "head": "tongue",  # TODO: Choose head
        "tail": "hook",  # TODO: Choose tail
    }

def move_lucas(game_state: typing.Dict) -> typing.Dict:
    logFileName = "logs/turn_" + str(game_state["turn"]) + ".json"
    logFilePath = Path(__file__).parent / logFileName
    json_file = open(logFilePath, "w")
    json.dump(game_state, json_file, indent=4)
    json_file.close()

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

    if my_head["x"] >= board_width:
        is_move_safe["right"] = False

    if my_head["x"] <= 0:
        is_move_safe["left"] = False

    if my_head["y"] >= board_height:
        is_move_safe["down"] = False

    if my_head["y"] <= 0:
        is_move_safe["up"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
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

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
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

    # Are there any safe moves left?
    safe_moves = []
    for move, is_safe in is_move_safe.items():
        if is_safe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    foods = game_state['board']['food']
    if foods:
        # Calculate the distances to all food items
        distances = []
        for food in foods:
            distance = abs(food["x"] - my_head["x"]) + abs(food["y"] - my_head["y"])
            distances.append(distance)

        # Find the nearest food
        min_distance = min(distances)
        nearest_food_index = distances.index(min_distance)
        nearest_food = foods[nearest_food_index]

        # Determine the next move to get closer to the nearest food
        if nearest_food["x"] < my_head["x"]:
            is_move_safe["left"] = True
            is_move_safe["right"] = False
            is_move_safe["up"] = False
            is_move_safe["down"] = False
        elif nearest_food["x"] > my_head["x"]:
            is_move_safe["left"] = False
            is_move_safe["right"] = True
            is_move_safe["up"] = False
            is_move_safe["down"] = False
        elif nearest_food["y"] < my_head["y"]:
            is_move_safe["left"] = False
            is_move_safe["right"] = False
            is_move_safe["up"] = True
            is_move_safe["down"] = False
        elif nearest_food["y"] > my_head["y"]:
            is_move_safe["left"] = False
            is_move_safe["right"] = False
            is_move_safe["up"] = False
            is_move_safe["down"] = True

    # TODO: Step 5 - Trap Opponent
    for snake in opponents:
        if len(snake['body']) >= len(my_body):
            opponent_head = snake['body'][0]
            x_diff = opponent_head['x'] - my_head['x']
            y_diff = opponent_head['y'] - my_head['y']

            if abs(x_diff) < abs(y_diff):
                if y_diff > 0:
                    is_move_safe['up'] = False
                else:
                    is_move_safe['down'] = False
            else:
                if x_diff > 0:
                    is_move_safe['left'] = False
                else:
                    is_move_safe['right'] = False

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

if __name__ == "__main__":
    dataFilePath = Path(__file__).parent / "snake_lucas_test.json"
    rhandle = open(dataFilePath, "r")

    gamestate = json.load(rhandle)
    rhandle.close()
    print(move_lucastest(gamestate))
