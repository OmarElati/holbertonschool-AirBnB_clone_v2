#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models


class State(BaseModel, Base):
    """
    State class for storing state data.
    """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if models.storage_type == 'db':
        cities = relationship("City", cascade="all, delete", backref="state")
    else:
        @property
        def cities(self):
            """
            Getter attribute that returns the list of City instances with state_id
            equals to the current State.id.
            """
            cities = models.storage.all('City')
            return [city for city in cities.values() if city.state_id == self.id]
