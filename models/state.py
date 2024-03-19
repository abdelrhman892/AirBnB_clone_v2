#!/usr/bin/python3
""" State Module for HBNB project """
import shlex

from sqlalchemy import Column, String
from sqlalchemy.orm import Relationship

import models
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = Relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        var = models.storage.all()
        ls = []
        result = []
        for key in var:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if city[0] == 'City':
                ls.append(var[key])
        for element in ls:
            if element.state_id == self.id:
                result.append(element)
        return result
