#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """handles the /hbnb route"""
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    places_tmp = storage.all("Place").values()
    owners = storage.all("User")
    places = []
    for k, v in owners.items():
        for place in places_tmp:
            if k.split('.')[1] == place.user_id:
                places.append([f'{v.first_name} {v.last_name}', place])
    places.sort(key=lambda x: x[1].name)
    return render_template('100-hbnb.html', states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
