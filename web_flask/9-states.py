#!/usr/bin/python3
"""Module for a script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Displays an HTML page that lists all State objects present in DBStorage sorted by name"""
    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Displays an HTML page that lists all City objects linked to the State with the given id"""
    state = storage.get(State, id)
    if state is None:
        return render_template('9-not_found.html')
    cities = sorted(state.cities, key=lambda x: x.name)
    return render_template('8-cities_by_states.html', state=state, cities=cities)


@app.teardown_appcontext
def teardown_db(error):
    """Removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
