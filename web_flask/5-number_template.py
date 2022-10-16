#!/usr/bin/python3
"""
script that starts a Flask web application
Run it with python3 -m 5-number_template or ./5-number_template
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """function that handles / route"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """function that handles /hbnb route"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """function that handles /c/<text> route"""
    return f"C {text.replace('_', ' ')}"


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    """function that handles /python/(<text>) route"""
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """function that handles /number/<n> route"""
    return f"{n:d} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """function that handles /number_template/<n> route"""
    return render_template('5-number.html', number=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
