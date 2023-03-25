#!/usr/bin/python3
"""Unit tests for FileStorage class"""
import unittest
import os
from models import storage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """Test suite for FileStorage class"""

    def setUp(self):
        """Set up test environment"""
        self.test_model = BaseModel()
        self.test_model.save()
        self.storage = storage

    def tearDown(self):
        """Tear down test environment"""
        os.remove('file.json')

    def test_all(self):
        """Test all method"""
        objects = self.storage.all()
        self.assertIsInstance(objects, dict)
        self.assertIn('BaseModel.' + self.test_model.id, objects)

    def test_save_reload(self):
        """Test save and reload methods"""
        new_model = BaseModel()
        new_model.save()
        self.storage.reload()
        self.assertIn('BaseModel.' + new_model.id, self.storage.all())

    def test_file_path(self):
        """Test file_path attribute"""
        self.assertIsInstance(self.storage._FileStorage__file_path, str)

    def test_objects(self):
        """Test objects attribute"""
        self.assertIsInstance(self.storage._FileStorage__objects, dict)
