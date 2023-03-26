#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel, Base
from models.place import place_amenity
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy import Table

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
        nullable=False)
)


class Amenity(BaseModel, Base):
    """ Amenity class """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship(
        "Place", secondary=place_amenity, back_populates="amenities")
