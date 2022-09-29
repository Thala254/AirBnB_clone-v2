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
from models import storage


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
    def setUp(self):
        """ """
        self.model1 = BaseModel()

        test_args = {'created_at': datetime(2022, 8, 10, 2, 6, 55, 258849),
                     'updated_at': datetime(2022, 8, 10, 2, 6, 55, 258966),
                     'id': '46458416-e5d5-4985-aa48-a2b369d03d2a',
                     'name': 'model1'}
        self.model2 = BaseModel(**test_args)
        self.model2.save()

    def tearDown(self):
        try:
            storage.delete(self.model2)
            storage.delete(self.model1)
            os.remove('file.json')
        except Exception:
            pass

    def test_instantiation(self):
        self.assertIsInstance(self.model1, BaseModel)
        self.assertTrue(hasattr(self.model1, "created_at"))
        self.assertTrue(hasattr(self.model1, "id"))
        self.assertTrue(hasattr(self.model1, "updated_at"))

    def test_reinstantiation(self):
        self.assertIsInstance(self.model2, BaseModel)
        self.assertEqual(self.model2.id,
                         '46458416-e5d5-4985-aa48-a2b369d03d2a')

    def test_save(self):
        self.model1.save()
        self.assertTrue(hasattr(self.model1, "updated_at"))
        old_time = self.model2.updated_at
        self.model2.save()
        self.assertNotEqual(old_time, self.model2.updated_at)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not testing db storage")
    def test_save(self):
        """ Testing save """
        self.model1.save()
        key = self.model1.__class__.__name__ + "." + self.model1.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], self.model1.to_dict())

    def test_to_dict(self):
        jsonified = self.model2.to_dict()
        self.assertNotEqual(self.model2.__dict__, jsonified)
        self.assertNotIsInstance(jsonified["created_at"], datetime)
        self.assertNotIsInstance(jsonified["updated_at"], datetime)
        self.assertTrue(hasattr(jsonified, "__class__"))
        self.assertEqual(jsonified["__class__"], "BaseModel")

    def test_kwargs(self):
        """ """
        self.assertEqual(self.model2.id,
                         '46458416-e5d5-4985-aa48-a2b369d03d2a')
        # self.assertEqual(self.model2.created_at,
        #                  datetime(2022, 8, 10, 2, 6, 55, 258849))

    def test_kwargs_int(self):
        """ """
        copy = self.model2.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_str(self):
        """ test that the str method has the correct output """
        self.assertEqual(str(self.model1), '[{}] ({}) {}'
                         .format(self.model1.__class__.__name__,
                                 self.model1.id, self.model1.__dict__))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not testing db storage")
    def test_todict(self):
        """ Test conversion of object attributes to dictionary for json """
        self.model1.name = "School"
        self.model1.number = 10
        d = self.model1.to_dict()
        expected_attributes = ['id', 'created_at', 'updated_at',
                               'name', 'number', '__class__']
        self.assertCountEqual(d.keys(), expected_attributes)
        self.assertEqual(d['__class__'], self.model1.__class__.__name__)
        self.assertEqual(d['name'], 'School')
        self.assertEqual(d['number'], '10')
        # self.assertEqual(d['created_at'], self.model1.created_at.isoformat())
        # self.assertEqual(d['updated_at'], self.model1.updated_at.isoformat())

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = BaseModel(**n)

    def test_kwargs_one(self):
        """ """
        n = {'Name': 'test'}
        new = BaseModel(**n)
        self.assertEqual(n['Name'], new.Name)

    def test_updated_at(self):
        """ Test that save method updates `updated_at` and calls
        storage.save """
        self.assertEqual(type(self.model1.updated_at), datetime)
        old_updated_at = self.model1.updated_at
        self.model1.save()
        new_updated_at = self.model1.updated_at
        self.assertFalse(old_updated_at == new_updated_at)
        storage.delete(self.model1)
