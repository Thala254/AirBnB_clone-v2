#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
import models

if getenv('HBNB_TYPE_STORAGE') == "db":
    Base = declarative_base()
else:
    class Base:
        """useless class"""
        pass


class BaseModel:
    """A base class for all hbnb models"""
    if getenv('HBNB_TYPE_STORAGE') == "db":
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow(),
                            nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow(),
                            nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            if 'id' not in kwargs:
                kwargs['id'] = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                kwargs['created_at'] = datetime.now()
            elif not isinstance(kwargs['created_at'], datetime):
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                         "%Y-%m-%d %H:%M:%S.%f"
                                                         )
            if 'updated_at' not in kwargs:
                kwargs['updated_at'] = datetime.now()
            elif not isinstance(kwargs['updated_at'], datetime):
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                         "%Y-%m-%d %H:%M:%S.%f"
                                                         )
            if getenv('HBNB_TYPE_STORAGE') != "db":
                kwargs.pop('__class__', None)
            for k, v in kwargs.items():
                setattr(self, k, v)

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{}] ({}) {}'.format(type(self).__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""

        """
        dictionary = self.__dict__.copy()
        if '_sa_instance_state' in dictionary:
            dictionary.pop('_sa_instance_state', None)
        dictionary["created_at"] = dictionary["created_at"].isoformat()
        dictionary["updated_at"] = dictionary["updated_at"].isoformat()
        dictionary["__class__"] = type(self).__name__
        return dictionary
        """
        dictionary = {
            k: str(v) for k, v in self.__dict__.items()
        }
        dictionary.pop('_sa_instance_state', None)
        dictionary.update({
            '__class__': self.__class__.__name__
        })
        return dictionary

    def delete(self):
        models.storage.delete(self)
