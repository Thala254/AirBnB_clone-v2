#!/usr/bin/python3
"""
script that starts a Flask web application
Run this script from AirBnB_v2 directory for imports
"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def handle_teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """function to handle request to /states_list route"""
    states = storage.all("State").values()
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
