import bottle
import json
import random
from queue import Queue

@bottle.route('/')
def index():
    return "Your BattleSnake is alive!"

@bottle.post('/ping')
def ping():
    return json.dumps({"ping": "pong"})

@bottle.post('/move')
def move():
    data = bottle.request.json

    # Extract information from the request
    board = data['board']
    board_width = board['width']
    board_height = board['height']
    head = data['you']['head']
    body = data['you']['body']
    snakes = data['board']['snakes']

    # Choose the best move based on the strategy
    move = choose_move(head, body, board_width, board_height, snakes)

    response = {
        'move': move,
        'taunt': 'I am the smartest BattleSnake!'
    }

    return json.dumps(response)

def choose_move(head, body, board_width, board_height, snakes):
    valid_moves = ['up', 'down', 'left', 'right']
    safe_moves = get_safe_moves(head, body, board_width, board_height)

    # Prioritize food if available
    food_moves = get_food_moves(head, valid_moves, board_width, board_height, snakes)
    if food_moves:
        return random.choice(food_moves)

    # Avoid colliding with other snakes
    avoid_snakes_moves = get_avoid_snakes_moves(head, safe_moves, board_width, board_height, snakes)
    if avoid_snakes_moves:
        return random.choice(avoid_snakes_moves)

    # Choose a safe move if no food or snake avoidance is necessary
    if safe_moves:
        return random.choice(safe_moves)

    # If no safe moves, choose any valid move
    return random.choice(valid_moves)

def get_safe_moves(head, body, board_width, board_height):
    safe_moves = []
    for move in ['up', 'down', 'left', 'right']:
        x, y = get_new_position(head['x'], head['y'], move)
        if is_valid_move(x, y, board_width, board_height, body):
            safe_moves.append(move)
    return safe_moves

def get_food_moves(head, valid_moves, board_width, board_height, snakes):
    food_moves = []
    for move in valid_moves:
        x, y = get_new_position(head['x'], head['y'], move)
        if is_valid_move(x, y, board_width, board_height, []):
            if is_food_location(x, y, snakes):
                food_moves.append(move)
    return food_moves

def get_avoid_snakes_moves(head, valid_moves, board_width, board_height, snakes):
    avoid_moves = []
    for move in valid_moves:
        x, y = get_new_position(head['x'], head['y'], move)
        if is_valid_move(x, y, board_width, board_height, []):
            if not is_snake_location(x, y, snakes):
                avoid_moves.append(move)
    return avoid_moves

def get_new_position(x, y, direction):
    if direction == 'up':
        return x, y - 1
    elif direction == 'down':
        return x, y + 1
    elif direction == 'left':
        return x - 1, y
    elif direction == 'right':
        return x + 1, y

def is_valid_move(x, y, width, height, body):
    if x < 0 or x >= width:
        return False
    if y < 0 or y >= height:
        return False
    if (x, y) in body:
        return False
    return True

def is_food_location(x, y, snakes):
    for snake in snakes:
        for part in snake['body']:
            if part['x'] == x and part['y'] == y:
                return True
    return False

def is_snake_location(x, y, snakes):
    for snake in snakes:
        for part in snake['body']:
            if part['x'] == x and part['y'] == y:
                return True
    return False

if __name__ == '__main__':
    bottle.run(
        application=bottle.app(),
        server='gunicorn',
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080))
    )
