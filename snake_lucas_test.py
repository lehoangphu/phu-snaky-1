def move(data):
    # Extract relevant information from the game data
    you = data["you"]
    head = you["head"]
    board = data["board"]
    food = board["food"]

    # Find the closest food item
    closest_food = find_closest_food(head, food)

    # Determine the next move based on the direction towards the closest food
    next_move = get_direction(head, closest_food)

    return {
        "move": next_move,
        "shout": "I'm hungry!",
    }

def find_closest_food(head, food):
    # Calculate the distance from the snake's head to each food item
    distances = [distance(head, food_item) for food_item in food]

    # Find the index of the closest food item
    closest_food_index = distances.index(min(distances))

    # Return the coordinates of the closest food item
    return food[closest_food_index]

def get_direction(head, target):
    # Determine the direction (up, down, left, right) towards the target
    if head["x"] < target["x"]:
        return "right"
    elif head["x"] > target["x"]:
        return "left"
    elif head["y"] < target["y"]:
        return "up"
    else:
        return "down"

def distance(point1, point2):
    # Calculate the Manhattan distance between two points
    return abs(point1["x"] - point2["x"]) + abs(point1["y"] - point2["y"])
