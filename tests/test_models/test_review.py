#!/usr/bin/python3
""" """
import unittest
import inspect
import pep8 as pycodestyle
from datetime import datetime
import models
from models import storage
from models.review import Review
from models.place import Place
from models.state import State
from models.user import User
from models.city import City


class TestReviewDocs(unittest.TestCase):
    """ Tests for documentation and styling of Review Class"""

    @classmethod
    def setUpClass(self):
        """setup for docstring tests"""
        self.base_funcs = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test to confirm that models/review.py conform to pep8"""
        for file in ['models/review.py',
                     'tests/test_models/test_review.py']:
            with self.subTest(path=file):
                errors = pycodestyle.Checker(file).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for pressence of module docstring"""
        self.assertTrue(len(models.review.__doc__) >= 1,
                        "Review.py needs a docstring")

    def test_class_docstring(self):
        """Test for the presence of Review class docstring"""
        self.assertTrue(len(Review.__doc__) >= 1,
                        "Review class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Review methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertTrue(
                    len(func.__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestReview(unittest.TestCase):
    """ Tests for Review Class """
    def test_initialization_no_arg(self):
        """test simple initialization with no arguments"""
        model = Review()
        self.assertTrue(hasattr(model, "place_id"))
        self.assertTrue(hasattr(model, "user_id"))
        self.assertTrue(hasattr(model, "text"))
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))

    def test_var_initialization(self):
        """Check default type"""
        model = Review()
        self.assertIsInstance(model.created_at, datetime)

    def test_save(self):
        """saving the object to storage"""
        test_user = {'id': "004",
                     'email': "you@g.com",
                     'password': "1234",
                     'first_name': "TEST",
                     'last_name': "REVIEW"}
        user = User(**test_user)
        test_state = {'id': "004",
                      'created_at': datetime(2022, 8, 12, 00, 31, 55, 331997),
                      'name': "TEST STATE FOR CITY"}
        state = State(**test_state)
        test_city = {'id': "007",
                     'name': "CITY SET UP",
                     'state_id': "004"}
        city = City(**test_city)
        test_place = {'id': "005",
                      'city_id': "007",
                      'user_id': "004",
                      'name': "TEST REVIEW",
                      'description': "blah blah",
                      'number_rooms': 4,
                      'number_bathrooms': 2,
                      'max_guest': 4,
                      'price_by_night': 23,
                      'latitude': 45.5,
                      'longitude': 23.4}
        place = Place(**test_place)
        test_review = {'text': "a text",
                       'place_id': "005",
                       'user_id': "004"}
        review = Review(**test_review)
        user.save()
        state.save()
        city.save()
        place.save()
        review.save()
        all_reviews = storage.all("Review")
        self.assertIn(f"Review.{review.id}", all_reviews.keys())
        storage.delete(review)
        storage.delete(place)
        storage.delete(user)
        storage.delete(state)
