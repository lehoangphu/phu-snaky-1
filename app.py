# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import typing

from flask import Flask
from flask import request

from snake_phu import move_phu
from snake_peter import move_peter


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


app = Flask("Battlesnake")

@app.get("/daddy/")
def on_daddy_info():
    return {
        "apiversion": "1",
        "author": "Daddy",  # TODO: Your Battlesnake Username
        "color": "#733488",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }

@app.post("/daddy/start")
def on_daddy_start():
    game_state = request.get_json()
    start(game_state)
    return "ok"

@app.post("/daddy/move")
def on_daddy_move():
    game_state = request.get_json()
    return move_phu(game_state)

@app.post("/daddy/end")
def on_daddy_end():
    game_state = request.get_json()
    end(game_state)
    return "ok"

@app.get("/peter/")
def on_peter_info():
    return {
        "apiversion": "1",
        "author": "Peter",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }

@app.post("/peter/start")
def on_peter_start():
    game_state = request.get_json()
    start(game_state)
    return "ok"

@app.post("/peter/end")
def on_peter_end():
    game_state = request.get_json()
    end(game_state)
    return "ok"

@app.post("/peter/move")
def on_peter_move():
    game_state = request.get_json()
    return move_peter(game_state)


@app.after_request
def identify_server(response):
    response.headers.set(
        "server", "battlesnake/github/starter-snake-python"
    )
    return response

if __name__ == '__main__':
    app.run()
