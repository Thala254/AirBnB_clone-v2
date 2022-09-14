#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String, Table
import models
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """amenity class"""
    if models.HBNB_TYPE_STORAGE == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""
