#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""


    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())


    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel."""
        if not kwargs.get('id'):
            self.id = str(uuid.uuid4())
        if not kwargs.get('created_at'):
            self.created_at = datetime.utcnow()
        if not kwargs.get('updated_at'):
            self.updated_at = datetime.utcnow()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.
                                     id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = dict(self.__dict__)
        dictionary.pop('_sa_instance_state', None)
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary['__class__'] = type(self).__name__
        return dictionary

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)
