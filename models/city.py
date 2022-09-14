#!/usr/bin/python3
""" City Module for HBNB project """

import models
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
# from models import HBNB_TYPE_STORAGE


class City(BaseModel, Base):
    """City class"""
    if models.HBNB_TYPE_STORAGE == "db":
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    else:
        """ The city class, contains state ID and name """
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
