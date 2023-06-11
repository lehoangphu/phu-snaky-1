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

    my_head = game_state["you"]["body"][0]
    my_body = set((part["x"], part["y"]) for part in game_state["you"]["body"][1:])
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]
    food_positions = set((food["x"], food["y"]) for food in game_state["board"]["food"])

    # Define all possible moves
    moves = ["up", "down", "left", "right"]

    # Check for immediate moves that lead to certain death
    immediate_deaths = []
    for move in moves:
        next_position = get_next_position(my_head, move)
        if (
            is_out_of_bounds(next_position, board_width, board_height)
            or is_collision(next_position, my_body, game_state["board"]["snakes"])
        ):
            immediate_deaths.append(move)

    # If there are immediate deaths, remove them from the list of possible moves
    if immediate_deaths:
        moves = [move for move in moves if move not in immediate_deaths]

    # If there are no possible moves, return a random safe move
    if not moves:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Calculate the distances to all food items
    distances = []
    for food in food_positions:
        distance = manhattan_distance(my_head, food)
        distances.append(distance)

    # Find the nearest food
    min_distance = min(distances)
    nearest_food_index = distances.index(min_distance)
    nearest_food = list(food_positions)[nearest_food_index]

    # Determine the best move towards the nearest food
    best_move = None
    if nearest_food[0] < my_head["x"] and "left" in moves:
        best_move = "left"
    elif nearest_food[0] > my_head["x"] and "right" in moves:
        best_move = "right"
    elif nearest_food[1] < my_head["y"] and "up" in moves:
        best_move = "up"
    elif nearest_food[1] > my_head["y"] and "down" in moves:
        best_move = "down"

    # If there is a best move, return it
    if best_move:
        print(f"MOVE {game_state['turn']}: {best_move}")
        return {"move": best_move}

    # If no best move is found, choose a random safe move
    next_move = random.choice(moves)
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def get_next_position(position: dict, move: str) -> dict:
    x, y = position["x"], position["y"]
    if move == "up":
        return {"x": x, "y": y + 1}
    elif move == "down":
        return {"x": x, "y": y - 1}
    elif move == "left":
        return {"x": x - 1, "y": y}
    elif move == "right":
        return {"x": x + 1, "y": y}

def is_out_of_bounds(position: dict, width: int, height: int) -> bool:
    x, y = position["x"], position["y"]
    return x < 0 or x >= width or y < 0 or y >= height

def is_collision(position: dict, body: set, snakes: list) -> bool:
    x, y = position["x"], position["y"]
    if (x, y) in body:
        return True
    for snake in snakes:
        if (x, y) in set((part["x"], part["y"]) for part in snake["body"]):
            return True
    return False

def manhattan_distance(pos1: dict, pos2: dict) -> int:
    return abs(pos1["x"] - pos2[0]) + abs(pos1["y"] - pos2[1])

if __name__ == "__main__":
    dataFilePath = Path(__file__).parent / "snake_lucas_test.json"
    rhandle = open(dataFilePath, "r")
    gamestate = json.load(rhandle)
    rhandle.close()
    print(move_lucastest(gamestate))
