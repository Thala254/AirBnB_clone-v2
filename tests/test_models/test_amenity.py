#!/usr/bin/python3
""" """
import unittest
import inspect
import os
import pep8 as pycodestyle
from datetime import datetime
import models
from models import storage
from models.amenity import Amenity


class TestAmenityDocs(unittest.TestCase):
    """ Tests for documentation and styling of Amenity Class"""

    @classmethod
    def setUpClass(self):
        """setup for docstring tests"""
        self.base_funcs = inspect.getmembers(Amenity, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test to confirm that models/base_model.py conform to pep8"""
        for file in ['models/amenity.py',
                     'tests/test_models/test_amenity.py']:
            with self.subTest(path=file):
                errors = pycodestyle.Checker(file).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for pressence of module docstring"""
        self.assertTrue(len(models.amenity.__doc__) >= 1,
                        "amenity.py needs a docstring")

    def test_class_docstring(self):
        """Test for the presence of Amenity class docstring"""
        self.assertTrue(len(Amenity.__doc__) >= 1,
                        "Amenity class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Amenity methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertTrue(
                    len(func.__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestAmenity(unittest.TestCase):
    """ Tests for Amenity class """
    def test_save(self):
        """test saving and retrieving an amenity"""
        test_args = {'updated_at': datetime(2022, 8, 12, 00, 31, 53, 331997),
                     'id': '054',
                     'created_at': datetime(2022, 8, 12, 00, 31, 53, 331900),
                     'name': "AMENITY SET UP"}
        model = Amenity(**test_args)
        model.save()
        all_amenities = storage.all("Amenity")
        self.assertIn(f"Amenity.{test_args['id']}", all_amenities.keys())
        storage.delete(model)

    def test_var_initialization(self):
        """test the creation of the model went right"""
        test_args = {'updated_at': datetime(2022, 8, 12, 00, 31, 53, 331997),
                     'id': '055',
                     'created_at': datetime(2022, 8, 12, 00, 31, 53, 331900),
                     'name': "AMENITY SET UP"}
        model = Amenity(**test_args)
        self.assertEqual(model.name, test_args['name'])
        self.assertEqual(model.id, test_args['id'])

    def test_missing_arg(self):
        """test creating an Amenity with no argument"""
        new = Amenity()
        self.assertTrue(hasattr(new, "id"))
        self.assertTrue(hasattr(new, "created_at"))

    def test_date_format(self):
        """test the date has the right type"""
        model = Amenity()
        self.assertIsInstance(model.created_at, datetime)

    def test_delete(self):
        """test the deletion of an amenity"""
        model = Amenity(name="test_amenity_delete")
        model.save()
        self.assertIn(f"Amenity.{model.id}", storage.all("Amenity").keys())
        storage.delete(model)
        self.assertNotIn(f"Amenity.{model.id}", storage.all("Amenity").keys())

    def test_all_amenity(self):
        """test querying all amenities"""
        length = len(storage.all("Amenity"))
        a = Amenity(name="amenity1", id="id1")
        b = Amenity(name="amenity2", id="id2")
        a.save()
        b.save()
        all_amenities = storage.all("Amenity")
        self.assertIn(f"Amenity.{a.id}", all_amenities.keys())
        self.assertIn(f"Amenity.{b.id}", all_amenities.keys())
        # self.assertEqual(len(all_amenities), length + 2)
        storage.delete(a)
        storage.delete(b)
