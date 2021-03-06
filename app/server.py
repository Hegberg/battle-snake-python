import json
import os
import random

import bottle
from bottle import HTTPResponse

from app.move_snake import get_move


@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    #print("START:", json.dumps(data))

    response = {"color": "#800000", "headType": "bwc-ski", "tailType": "bolt"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/move")
def move():

    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json
    #print("MOVE:", json.dumps(data))

    # Choose a random direction to move in
    #directions = ["up", "down", "left", "right"]
    #move = random.choicie(directions)
    move = get_move(data)

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    #shout = "I am a python snake!"
    shout = "I like em big... I like em Chunky! I like em round... I like em Bumpy!"

    response = {"move": move, "shout": shout}
    #print("MOVE RESPONSE:", response)
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )



@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    #print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "192.168.1.65"),
        #host=os.getenv("IP", "127.0.0.1"),
        #host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
