#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
from datetime import datetime
import json
import os
import inspect
import pep8 as pycodestyle
import models


class TestBaseModelDocs(unittest.TestCase):
    """ Tests for documentation and styling of BaseModel Class"""

    @classmethod
    def setUpClass(self):
        """setup for docstring tests"""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test to confirm that models/base_model.py conform to pep8"""
        for file in ['models/base_model.py',
                     'tests/test_models/test_base_model.py']:
            with self.subTest(path=file):
                errors = pycodestyle.Checker(file).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for pressence of module docstring"""
        self.assertTrue(len(models.base_model.__doc__) >= 1,
                        "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test for the presence of BaseModel class docstring"""
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertTrue(
                    len(func.__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBasemodel(unittest.TestCase):
    """ BaseModel Class tests """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_default(self):
        """ """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)
        self.assertEqual(i.id, new.id)
        self.assertEqual(i.created_at, new.created_at)
        self.assertNotEqual(i.updated_at, new.updated_at)

    def test_kwargs_int(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ test that the str method has the correct output """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ Test conversion of object attributes to dictionary for json """
        i = self.value()
        i.name = "School"
        i.number = 10
        d = i.to_dict()
        expected_attributes = ['id', 'created_at', 'updated_at',
                               'name', 'number', '__class__']
        self.assertCountEqual(d.keys(), expected_attributes)
        self.assertEqual(d['__class__'], self.name)
        self.assertEqual(d['name'], 'School')
        self.assertEqual(d['number'], 10)
        self.assertEqual(d['created_at'], i.created_at.isoformat())
        self.assertEqual(d['updated_at'], i.updated_at.isoformat())

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ """
        n = {'Name': 'test'}
        new = self.value(**n)
        self.assertEqual(n['Name'], new.Name)

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """ Test that save method updates `updated_at` and calls
        storage.save """
        new_a = self.value()
        self.assertEqual(type(new_a.updated_at), datetime)
        old_updated_at = new_a.updated_at
        new_a.save()
        new_updated_at = new_a.updated_at
        self.assertFalse(old_updated_at == new_updated_at)
