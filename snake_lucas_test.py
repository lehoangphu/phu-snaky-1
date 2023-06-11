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

    my_snake_id = game_state["you"]["id"]
    my_head = game_state["you"]["head"]
    my_body = game_state["you"]["body"]
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]
    food_locations = game_state["board"]["food"]
    snakes = game_state["board"]["snakes"]

    # Check if a move is safe or not
    def is_move_safe(x: int, y: int) -> bool:
        if x < 0 or x >= board_width or y < 0 or y >= board_height:
            return False
        for body_part in my_body[1:]:
            if body_part["x"] == x and body_part["y"] == y:
                return False
        for snake in snakes:
            if snake["id"] != my_snake_id:
                for body_part in snake["body"]:
                    if body_part["x"] == x and body_part["y"] == y:
                        return False
        return True

    # Calculate the Manhattan distance between two points
    def manhattan_distance(p1: typing.Dict, p2: typing.Dict) -> int:
        return abs(p1["x"] - p2["x"]) + abs(p1["y"] - p2["y"])

    # Find the nearest food and its distance
    def find_nearest_food() -> typing.Optional[typing.Dict]:
        nearest_food = None
        nearest_distance = float("inf")
        for food in food_locations:
            distance = manhattan_distance(my_head, food)
            if distance < nearest_distance:
                nearest_food = food
                nearest_distance = distance
        return nearest_food, nearest_distance

    # Find the head of the snake with the longest body
    def find_longest_snake_head() -> typing.Optional[typing.Dict]:
        longest_snake_head = None
        longest_snake_length = 0
        for snake in snakes:
            if snake["id"] != my_snake_id and len(snake["body"]) > longest_snake_length:
                longest_snake_head = snake["head"]
                longest_snake_length = len(snake["body"])
        return longest_snake_head

    # Step 1: Prevent your Battlesnake from moving out of bounds
    safe_moves = []
    for move in ["up", "down", "left", "right"]:
        next_x, next_y = get_next_position(my_head, move)
        if is_move_safe(next_x, next_y):
            safe_moves.append(move)

    if not safe_moves:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Step 2: Move towards the nearest food
    nearest_food, food_distance = find_nearest_food()
    if nearest_food:
        if nearest_food["x"] < my_head["x"]:
            safe_moves = [move for move in safe_moves if move != "right"]
        elif nearest_food["x"] > my_head["x"]:
            safe_moves = [move for move in safe_moves if move != "left"]
        if nearest_food["y"] < my_head["y"]:
            safe_moves = [move for move in safe_moves if move != "down"]
        elif nearest_food["y"] > my_head["y"]:
            safe_moves = [move for move in safe_moves if move != "up"]

    # Step 3: Trap the opponent with the longest body
    longest_snake_head = find_longest_snake_head()
    if longest_snake_head:
        if longest_snake_head["x"] < my_head["x"]:
            safe_moves = [move for move in safe_moves if move != "left"]
        elif longest_snake_head["x"] > my_head["x"]:
            safe_moves = [move for move in safe_moves if move != "right"]
        if longest_snake_head["y"] < my_head["y"]:
            safe_moves = [move for move in safe_moves if move != "up"]
        elif longest_snake_head["y"] > my_head["y"]:
            safe_moves = [move for move in safe_moves if move != "down"]

    # Step 4: Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


def get_next_position(position: typing.Dict, move: str) -> typing.Tuple[int, int]:
    x, y = position["x"], position["y"]
    if move == "up":
        return x, y - 1
    elif move == "down":
        return x, y + 1
    elif move == "left":
        return x - 1, y
    elif move == "right":
        return x + 1, y


if __name__ == "__main__":
    dataFilePath = Path(__file__).parent / "snake_lucas_test.json"
    rhandle = open(dataFilePath, "r")

    gamestate = json.load(rhandle)
    rhandle.close()
    print(move_lucastest(gamestate))
