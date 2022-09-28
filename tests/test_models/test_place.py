#!/usr/bin/python3
""" """
import unittest
import inspect
import pep8 as pycodestyle
from datetime import datetime
import models
from models import storage
from models.place import Place
from models.state import State
from models.user import User
from models.city import City


class TestPlaceDocs(unittest.TestCase):
    """ Tests for documentation and styling of Place Class"""

    @classmethod
    def setUpClass(self):
        """setup for docstring tests"""
        self.base_funcs = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test to confirm that models/place.py conform to pep8"""
        for file in ['models/place.py',
                     'tests/test_models/test_place.py']:
            with self.subTest(path=file):
                errors = pycodestyle.Checker(file).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for pressence of module docstring"""
        self.assertTrue(len(models.place.__doc__) >= 1,
                        "Place.py needs a docstring")

    def test_class_docstring(self):
        """Test for the presence of Place class docstring"""
        self.assertTrue(len(Place.__doc__) >= 1,
                        "Place class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Place methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertTrue(
                    len(func.__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestPlace(unittest.TestCase):
    """ Tests for Place class """

    @classmethod
    def setUpClass(cls):
        """create necessary dependent objects"""
        test_user = {'id': "001",
                     'email': "you@g.com",
                     'password': "1234",
                     'first_name': "TEST",
                     'last_name': "REVIEW"}
        cls.user = User(test_user)
        cls.user.save()
        test_state = {'id': "002",
                      'created_at': datetime(2022, 8, 12, 00, 31, 55, 331997),
                      'name': "TEST STATE FOR CITY"}
        cls.state = State(test_state)
        cls.state.save()
        test_city = {'id': "003",
                     'name': "CITY SET UP",
                     'state_id': "002"}
        cls.city = City(test_city)
        cls.city.save()

    @classmethod
    def tearDownClass(cls):
        storage.delete(cls.state)
        storage.delete(cls.user)

    def test_simple_initialization(self):
        """initialization without arguments"""
        model = Place()
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))

    def test_var_initialization(self):
        """Check default type"""
        test_place = {'id': "003",
                      'city_id': "003",
                      'user_id': "001",
                      'name': "TEST REVIEW",
                      'description': "blah blah",
                      'number_rooms': 4,
                      'number_bathrooms': 2,
                      'max_guest': 4,
                      'price_by_night': 23,
                      'latitude': 45.5,
                      'longitude': 23.4}
        model = Place(**test_place)
        self.assertEqual(model.id, test_place["id"])
        self.assertEqual(model.city_id, test_place["city_id"])
        self.assertEqual(model.user_id, test_place["user_id"])
        self.assertEqual(model.name, test_place["name"])
        self.assertEqual(model.description, test_place["description"])
        self.assertEqual(model.number_rooms, test_place["number_rooms"])
        self.assertEqual(model.number_bathrooms,
                         test_place["number_bathrooms"])
        self.assertEqual(model.max_guest, test_place["max_guest"])
        self.assertEqual(model.price_by_night, test_place["price_by_night"])
        self.assertEqual(model.latitude, test_place["latitude"])
        self.assertEqual(model.longitude, test_place["longitude"])

    def test_date_format(self):
        """test the date has the right type"""
        model = Place()
        self.assertIsInstance(model.created_at, datetime)

    def test_delete(self):
        """test the deletion of a city"""
        test_place = {'name': "test_1",
                      'city_id': "003",
                      'user_id': "001"
                      }
        model = Place(**test_place)
        model.save()
        self.assertIn(f"Place.{model.id}", storage.all("Place").keys())
        storage.delete(model)
        self.assertNotIn(f"Place.{model.id}", storage.all("Place").keys())

    def test_all_place(self):
        """test querying all places"""
        length = len(storage.all("Place"))
        test_place = {'city_id': "003",
                      'user_id': "001"
                      }
        a = Place(**test_place)
        a.name = "test_a"
        b = Place(**test_place)
        b.name = "test_b"
        a.save()
        b.save()
        all_cities = storage.all("Place")
        self.assertIn(f"Place.{a.id}", all_cities.keys())
        self.assertIn(f"Place.{b.id}", all_cities.keys())
        self.assertEqual(len(all_cities), length + 2)
        storage.delete(a)
        storage.delete(b)

    def test_save(self):
        """saving the object to storage"""
        test_args = {'id': "003",
                     'city_id': "003",
                     'user_id': "001",
                     'name': "TEST REVIEW",
                     'description': "blah blah",
                     'number_rooms': 4,
                     'number_bathrooms': 2,
                     'max_guest': 4,
                     'price_by_night': 23,
                     'latitude': 45.5,
                     'longitude': 23.4}
        place = Place(**test_args)
        place.save()
        all_places = storage.all("Place")
        self.assertIn(f"Place.{test_args['id']}", all_places.keys())
        storage.delete(place)

    # def __init__(self, *args, **kwargs):
    #     """ """
    #     super().__init__(*args, **kwargs)
    #     self.name = "Place"
    #     self.value = Place

    # def test_city_id(self):
    #     """ """
    #     new = self.value()
    #     new.save()
    #     self.assertEqual(type(new.city_id), str)

    # def test_user_id(self):
    #     """ """
    #     new = self.value()
    #     new.save()
    #     self.assertEqual(type(new.user_id), str)

    # def test_name(self):
    #     """ """
    #     new = self.value()
    #     new.save()
    #     self.assertEqual(type(new.name), str)

    # def test_description(self):
    #     """ """
    #     new = self.value()
    #     new.save()
    #     self.assertEqual(type(new.description), str)

    # def test_number_rooms(self):
    #     """ """
    #     new = self.value()
    #     new.save()
    #     self.assertEqual(type(new.number_rooms), int)

    # def test_number_bathrooms(self):
    #     """ """
    #     new = self.value()
    #     new.save()
    #     self.assertEqual(type(new.number_bathrooms), int)

    # def test_max_guest(self):
    #     """ """
    #     new = self.value()
    #     new.save()
    #     self.assertEqual(type(new.max_guest), int)

    # def test_price_by_night(self):
    #     """ """
    #     new = self.value()
    #     new.save()
    #     self.assertEqual(type(new.price_by_night), int)

    # def test_latitude(self):
    #     """ """
    #     new = self.value()
    #     new.save()
    #     self.assertEqual(type(new.latitude), float)

    # def test_longitude(self):
    #     """ """
    #     new = self.value()
    #     new.save()
    #     self.assertEqual(type(new.latitude), float)

    # def test_amenity_ids(self):
    #     """ """
    #     new = self.value()
    #     new.save()
    #     self.assertEqual(type(new.amenity_ids), list)
