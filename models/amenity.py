#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String

from models.base_model import BaseModel


class Amenity(BaseModel):
    """This is the class for Amenity
    Attributes:
        name: The name of the Amenity
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
