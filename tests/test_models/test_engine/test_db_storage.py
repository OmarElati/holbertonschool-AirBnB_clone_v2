#!/usr/bin/python3
"""Unittest for DBStorage"""
import unittest
from models import storage
from models.state import State
from models.engine.db_storage import DBStorage
from datetime import datetime


class TestDBStorage(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        storage.reload()

    def test_all(self):
        """
        Test the all() method of DBStorage.
        """
        storage = DBStorage()
        storage.reload()
        state = State(name="California", created_at=datetime.now(),
                    updated_at=datetime.now())
        state.save()
        state_key = state.__class__.__name__ + "." + state.id
        all_objs = storage.all(State)
        self.assertIn(state_key, all_objs.keys())
        storage.close()

    def tearDown(self):
        """Tear down the test environment."""
        storage.close()


if __name__ == '__main__':
    unittest.main()
