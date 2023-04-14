#!/usr/bin/python3
"""
Starts a Flask web application.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Remove the current SQLAlchemy Session after each request.
    """
    storage.close()


@app.route('/states', strict_slashes=False)
def states_list():
    """
    List all State objects present in DBStorage sorted by name (A->Z)
    """
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html',
                           states=states_sorted)


@app.route('/states/<id>', strict_slashes=False)
def states_cities(id):
    """
    List all City objects linked to a State sorted by name (A->Z)
    """
    state = storage.get(State, id)
    if state is None:
        return render_template('9-states.html', state=None)

    cities_sorted = sorted(state.cities, key=lambda city: city.name)
    return render_template('9-states.html',
                           state=state, cities=cities_sorted)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
