#!/usr/bin/python3
# City Module for HBNB project
from sqlalchemy import Column, String, ForeignKey

from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """This is the class for Review
    Attributes:
        place id: place id
        user id: user id
        text: review description
    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
