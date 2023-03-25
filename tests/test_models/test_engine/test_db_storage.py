#!/usr/bin/python3
"""Unittest for DBStorage"""
import os
import unittest
from models import storage
from models.engine.db_storage import DBStorage
from models.state import State


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'db not active')
class TestDBStorage(unittest.TestCase):
    """Tests for the DBStorage class"""

    def setUp(self):
        """Set up testing environment"""
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        """Tear down testing environment"""
        self.db.close()

    def test_all(self):
        """Test all method"""
        objs = self.db.all()
        self.assertIsNotNone(objs)

    def test_new(self):
        """Test new method"""
        new_obj = State(name="California")
        self.db.new(new_obj)
        self.assertIn(new_obj, self.db.all().values())

    def test_save(self):
        """Test save method"""
        new_obj = State(name="California")
        self.db.new(new_obj)
        self.db.save()
        self.assertTrue(os.path.isfile('file.json'))

    def test_delete(self):
        """Test delete method"""
        new_obj = State(name="California")
        self.db.new(new_obj)
        self.db.save()
        self.db.delete(new_obj)
        self.assertNotIn(new_obj, self.db.all().values())

    def test_reload(self):
        """Test reload method"""
        self.assertTrue(isinstance(self.db._DBStorage__engine, object))
        self.assertTrue(isinstance(self.db._DBStorage__session, object))


if __name__ == '__main__':
    unittest.main()
