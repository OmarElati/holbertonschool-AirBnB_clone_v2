#!/usr/bin/python3
"""Module for a script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Displays an HTML page with a list of States and Cities"""
    states = storage.all(State).values()
    cities = list()
    for state in states:
        for city in state.cities:
            cities.append(city)

    return render_template('8-cities_by_states.html',
                           states=states, state_cities=cities)


@app.route('/states', strict_slashes=False)
def states():
    """Displays an HTML page that lists all State objects present in DBStorage sorted by name"""
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Displays an HTML page that lists all City objects linked to the State with the given id"""
    states = storage.all(State).values()
    for state in states:
        if id == state.id:
            return render_template('9-states.html',
                                    state=state, state_cities=state.cities)

    return render_template('9-states.html', not_found=True)


@app.teardown_appcontext
def teardown_db(error):
    """Removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
