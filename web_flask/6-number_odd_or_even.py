#!/usr/bin/python3
"""
This is module 6-number_odd_or_even.
It starts a minimal Flask application.
Run it with python3 -m 6-number_odd_or_even or ./6-number_odd_or_even
"""
from flask import Flask
from flask import render_template
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


@app.route('/python/', defaults={'text': "is cool"}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """give a rule a default value"""
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """make a rule only take a number"""
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:number>', strict_slashes=False)
def number_template(number):
    """create an html page with a rule"""
    return render_template('5-number.html', number=number)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Create a template with 2 variables"""
    odd_even = "even" if (n % 2 == 0) else "odd"
    return render_template("6-number_odd_or_even.html",
                           number=n, odd_even=odd_even)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
