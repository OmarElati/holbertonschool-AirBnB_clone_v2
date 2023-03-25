#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
import models
from models import *
from models.amenity import Amenity



# Define the place_amenity table
place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


# Define the Place table
class Place(Base):
    __tablename__ = 'places'
    id = Column(String(60), primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)


# Define the Amenity table
class Amenity(Base):
    __tablename__ = 'amenities'
    id = Column(String(60), primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
storage_type = "string"


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    if storage_type == 'db':
        amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)
    else:
        @property
        def amenities(self):
            amenities_list = []
            for amenity_id in self.amenity_ids:
                amenity = models.storage.get(Amenity, amenity_id)
                if amenity is not None:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, obj):
            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship("Review", backref="place", cascade="all, delete-orphan")
    else:
        @property
        def reviews(self):
            """getter method for reviews"""
            reviews = models.storage.all(Review)
            place_reviews = [review for review in reviews.values() if review.place_id == self.id]
            return place_reviews

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
