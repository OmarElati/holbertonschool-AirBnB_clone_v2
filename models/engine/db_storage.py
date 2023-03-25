#!/usr/bin/python3
"""
This module defines the DBStorage class
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """
    This class stores data to the MySQL database.
    """
    __engine = None
    __session = None
    classes = {
        'State': State,
        'City': City,
        'User': User,
        'Place': Place,
        'Review': Review,
        'Amenity': Amenity
    }

    def __init__(self):
        """Create the engine and links it to the MySQL database and user."""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(os.getenv('HBNB_MYSQL_USER'),
                    os.getenv('HBNB_MYSQL_PWD'),
                    os.getenv('HBNB_MYSQL_HOST'),
                    os.getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of instances/objects.
        """
        if cls is not None:
            if cls in self.classes:
                objs = self.__session.query(self.classes[cls]).all()
                return {obj.__class__.__name__ + '.' + obj.
                        id: obj for obj in objs}
            else:
                return {}
        else:
            obj_dict = {}
            for cls in self.classes.values():
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    obj_dict[key] = obj
            return obj_dict

    def new(self, obj):
        """
        Add the object to the current database session.
        """
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete obj from the current database session.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database and
        create the current database session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """
        Close the current database session.
        """
        self.__session.close()
