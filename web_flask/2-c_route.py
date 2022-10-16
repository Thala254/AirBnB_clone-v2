#!/usr/bin/python3
"""
This is module 2-c_route.
It starts a minimal Flask apllication.
Run it with python3 -m 2-c_route or ./2-c_route
"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """flask hello world"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """add a path to the url"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """make a simple variable rule"""
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
