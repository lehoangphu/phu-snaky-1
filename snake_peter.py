import random
import typing

def info_peter():
    return {
        "apiversion": "1",
        "author": "Peter",  # TODO: Your Battlesnake Username
        "color": "#142343",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move_peter(game_state: typing.Dict) -> typing.Dict:

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

    if (my_head['x'] == 0):
        is_move_safe["left"] = False
    if (my_head['x'] == board_width-1):
        is_move_safe["right"] = False
    if (my_head['y'] == 0):
        is_move_safe["down"] = False
    if (my_head['y'] == board_height-1):
        is_move_safe["up"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # Step 4 - Move towards food instead of random, to regain health and survive longer
    # TODO: Need to run to the nearest food
    food = game_state['board']['food']
    if (len(food) > 0):
        first_food = food[0]
        if (first_food['x'] < my_head["x"] and is_move_safe["left"]):
            return {"move": "left"}
        elif (first_food['x'] > my_head["x"] and is_move_safe["right"]):
            return {"move": "right"}
        elif (first_food['y'] < my_head["y"] and is_move_safe["down"]):
            return {"move": "down"}
        elif (first_food['y'] > my_head["y"] and is_move_safe["up"]):
            return {"move": "up"}
    

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}