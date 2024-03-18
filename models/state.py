#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String

from models.base_model import BaseModel, Base


class State(BaseModel):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
