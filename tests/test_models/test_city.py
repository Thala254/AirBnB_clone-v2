#!/usr/bin/python3
""" """
from models.city import City
from models.state import State
import unittest
import inspect
import pep8 as pycodestyle
from datetime import datetime
import models
from models import storage


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


class TestCity(unittest.TestCase):
    """ City Class Tests """

    @classmethod
    def setUpClass(cls):
        """Create a State object to test City"""
        test_state = {'updated_at': datetime(2022, 8, 12, 00, 31, 50, 331997),
                      'id': "001",
                      'created_at': datetime(2022, 8, 12, 00, 31, 55, 331997),
                      'name': "TEST STATE FOR CITY"}
        cls.state = State(**test_state)
        cls.state.save()

    @classmethod
    def tearDownClass(cls):
        storage.delete(cls.state)

    def test_save(self):
        """Set up the variables before the test"""
        test_args = {'updated_at': datetime(2022, 8, 12, 00, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4900',
                     'created_at': datetime(2022, 8, 12, 00, 31, 53, 331900),
                     'name': "CITY SET UP",
                     'state_id': "001"}
        model = City(**test_args)
        model.save()
        all_cities = storage.all("City")
        self.assertIn(f"City.{test_args['id']}", all_cities.keys())
        storage.delete(model)

    def test_var_initialization(self):
        """test simple initialization"""
        test_args = {'updated_at': datetime(2022, 8, 12, 00, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4900',
                     'created_at': datetime(2022, 8, 12, 00, 31, 53, 331900),
                     'name': "CITY SET UP",
                     'state_id': "001"}
        model = City(**test_args)
        self.assertEqual(model.name, test_args['name'])
        self.assertEqual(model.id, test_args['id'])

    def test_initialization_no_arg(self):
        """test initialization without arguments"""
        new = City()
        self.assertTrue(hasattr(new, "state_id"))
        self.assertTrue(hasattr(new, "created_at"))

    def test_date_format(self):
        """test the date has the right type"""
        model = City()
        self.assertIsInstance(model.created_at, datetime)

    def test_delete(self):
        """test the deletion of a city"""
        model = City(name="test_city_delete", state_id="001")
        model.save()
        self.assertIn(f"City.{model.id}", storage.all("City").keys())
        storage.delete(model)
        self.assertNotIn(f"City.{model.id}", storage.all("City").keys())

    def test_all_city(self):
        """test querying all cities"""
        length = len(storage.all("City"))
        a = City(name="amenity1", id="id1", state_id="001")
        b = City(name="amenity2", id="id2", state_id="001")
        a.save()
        b.save()
        all_cities = storage.all("City")
        self.assertIn(f"City.{a.id}", all_cities.keys())
        self.assertIn(f"City.{b.id}", all_cities.keys())
        # self.assertEqual(len(all_cities), length + 2)
        storage.delete(a)
        storage.delete(b)
