#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Table, ForeignKey, Float, Integer
import os
import models


# Define the place_amenity table
place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False))



class Amenity(BaseModel, Base):
    """ class for Place """
    __tablename__ = 'amenities'
    city_id = Column(
        String(60),
        ForeignKey("cities.id"),
        nullable=False)
    user_id = Column(
        String(60),
        ForeignKey("users.id"),
        nullable=False)
    name = Column(
        String(128),
        nullable=False)
    description = Column(
        String(1024),
        nullable=True)
    number_rooms = Column(
        Integer,
        default=0,
        nullable=False)
    number_bathrooms = Column(
        Integer,
        default=0,
        nullable=False)
    max_guest = Column(
        Integer,
        default=0,
        nullable=False)
    price_by_night = Column(
        Integer,
        default=0,
        nullable=False)
    latitude = Column(
        Float,
        nullable=True)
    longitude = Column(
        Float,
        nullable=True)
    amenity_ids = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete-orphan")
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False)
    else:
        @property
        def reviews(self):
            l = []
            for id, rvw in models.storage.all(Review).items():
                if rvw.place.id == Review.id:
                    l.append(rvw)
            return l

        @property
        def amenities(self):
            los_angeles = []
            for angel in amenity_ids:
                if angel.id == self.id:
                    amenities_list.append(angel)
            return los_angeles

        @amenities.setter
        def amenities(self, angel):
            if type(angel) is Amenity:
                self.amenity_ids.append(angel)
