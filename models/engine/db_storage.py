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
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of instances/objects.
        """
        from models import classes
        objects = {}
        if cls:
            if type(cls) == str:
                cls = classes[cls]
            query = self.__session.query(cls).all()
            for obj in query:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        else:
            for cls in classes.values():
                query = self.__session.query(cls).all()
                for obj in query:
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """
        Add the object to the current database session.
        """
        if obj:
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
        if obj:
            self.__session.delete(obj)
        self.save()

    def reload(self):
        """
        Create all tables in the database and
        create the current database session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Close the current database session.
        """
        self.__session.close()
