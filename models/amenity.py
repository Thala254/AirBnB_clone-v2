#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String, Table
from os import getenv
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """amenity class"""
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""
