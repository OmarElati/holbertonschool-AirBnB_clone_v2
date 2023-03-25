#!/usr/bin/python3
""" Module for testing db_storage"""
import unittest
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models import storage


class TestDBStorage(unittest.TestCase):
    def setUp(self):
        self.db = storage.DBStorage()

    def tearDown(self):
        self.db.close()

    def test_all(self):
        # Test all() method with no arguments
        all_objs = self.db.all()
        self.assertIsInstance(all_objs, dict)
        self.assertIn('State', all_objs)
        self.assertIn('City', all_objs)
        self.assertIn('User', all_objs)
        self.assertIn('Place', all_objs)
        self.assertIn('Review', all_objs)
        self.assertIn('Amenity', all_objs)

        # Test all() method with one class argument
        all_states = self.db.all(State)
        self.assertIsInstance(all_states, dict)
        self.assertIn('State', all_states)
        self.assertNotIn('City', all_states)

    def test_new(self):
        # Test that a new object is added to the session
        new_state = State(name="California")
        self.db.new(new_state)
        self.assertIn(new_state, self.db.__session.new)

    def test_save(self):
        # Test that changes to objects are saved to the database
        new_state = State(name="Nevada")
        self.db.new(new_state)
        self.db.save()
        self.assertIn(new_state, self.db.all(State).values())

    def test_delete(self):
        # Test that an object can be deleted from the session and database
        new_state = State(name="Texas")
        self.db.new(new_state)
        self.db.save()
        self.assertIn(new_state, self.db.all(State).values())

        self.db.delete(new_state)
        self.assertNotIn(new_state, self.db.all(State).values())

    def test_reload(self):
        # Test that tables are created and session is reloaded
        self.db.reload()
        self.assertIsNotNone(self.db.__engine)
        self.assertIsNotNone(self.db.__session)
        self.assertIsInstance(self.db.__session(), self.db.session_factory)


if __name__ == '__main__':
    unittest.main()
