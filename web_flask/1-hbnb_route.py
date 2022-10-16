#!/usr/bin/python3
"""
script that starts a Flask web application
Run it with python3 -m 1-hbnb_route or ./1-hbnb_route
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """function that handles / route"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """function that handles /hbnb route"""
    return 'HBNB'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
