#!/usr/bin/python3
"""Unittest for DBStorage"""
import unittest
from models import *
from models.state import State
from os import getenv


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', "not using db storage")
class TestDBStorage(unittest.TestCase):
    """
    Test the DBStorage class
    """

    def setUp(self):
        """
        Sets up the database connection and creates a new session
        """
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        """
        Closes the current session and drops all tables
        """
        self.db.close()
        self.db.__session.remove()
        self.db.__engine.dispose()
        self.db = None

    def test_all(self):
        """
        Test the all method
        """
        # create a new state and save it to the database
        new_state = State(name="California")
        new_state.save()

        # call the all method to get all states
        states = self.db.all(State)

        # check that the new state is in the dictionary
        self.assertIn(new_state, states.values())

    def test_new(self):
        """
        Test the new method
        """
        # create a new state and save it to the database
        new_state = State(name="California")
        self.db.new(new_state)
        self.db.save()

        # get the state from the database
        state = self.db.all(State).values()[0]

        # check that the new state was saved to the database
        self.assertEqual(new_state, state)

    def test_delete(self):
        """
        Test the delete method
        """
        # create a new state and save it to the database
        new_state = State(name="California")
        self.db.new(new_state)
        self.db.save()

        # delete the state from the database
        self.db.delete(new_state)
        self.db.save()

        # check that the state was deleted from the database
        states = self.db.all(State)
        self.assertNotIn(new_state, states.values())
