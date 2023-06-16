# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# For more info see docs.battlesnake.com
from flask import Flask
from flask import request
from flask import render_template

app = Flask("Battlesnake")

@app.route("/")
def on_root():
    return render_template("index.html")

@app.get("/<username>")
@app.get("/<username>/")
def on_info(username):
    module_name = "snake_" + username
    function_name_short = "info"
    function_name_full = "info_" + username  
    module = __import__(module_name)
    try:
        func_to_run = getattr(module, function_name_short)
    except AttributeError:
        func_to_run = getattr(module, function_name_full)
        
    return func_to_run()

@app.post("/<username>/move")
def on_move(username):
    module_name = "snake_" + username
    function_name_short = "move"
    function_name_full = "move_" + username   
    module = __import__(module_name)
    try:
        func_to_run = getattr(module, function_name_short)
    except AttributeError:
        func_to_run = getattr(module, function_name_full)
    game_state = request.get_json()
    return func_to_run(game_state)

@app.post("/<username>/start")
def on_start(username):
    game_state = request.get_json()
    return "ok"

@app.post("/<username>/end")
def on_end(username):
    game_state = request.get_json()
    return "ok"

@app.after_request
def identify_server(response):
    response.headers.set(
        "server", "battlesnake/github/starter-snake-python"
    )
    return response

if __name__ == '__main__':
    app.run()
