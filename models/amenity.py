#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Table, ForeignKey


# Define the place_amenity table
place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Amenity(BaseModel, Base):
     __tablename__ = 'amenities'
     id = Column(String(60), primary_key=True, nullable=False)
     name = Column(String(128), nullable=False)
     places = relationship("Place", secondary=place_amenity, back_populates="amenities")
