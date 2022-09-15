#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import TestBasemodel
from models.city import City
import unittest
import inspect
import pep8 as pycodestyle
import models


class TestCityDocs(unittest.TestCase):
    """ Tests for documentation and styling of City Class"""

    @classmethod
    def setUpClass(self):
        """setup for docstring tests"""
        self.base_funcs = inspect.getmembers(City, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test to confirm that models/city.py conform to pep8"""
        for file in ['models/city.py',
                     'tests/test_models/test_city.py']:
            with self.subTest(path=file):
                errors = pycodestyle.Checker(file).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for pressence of module docstring"""
        self.assertTrue(len(models.city.__doc__) >= 1,
                        "City.py needs a docstring")

    def test_class_docstring(self):
        """Test for the presence of City class docstring"""
        self.assertTrue(len(City.__doc__) >= 1,
                        "City class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in City methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertTrue(
                    len(func.__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class test_City(TestBasemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)
