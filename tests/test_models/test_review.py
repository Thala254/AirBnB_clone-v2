#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import TestBasemodel
from models.review import Review
import unittest
import inspect
import pep8 as pycodestyle
import models


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


class test_review(TestBasemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.place_id), str)

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_text(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.text), str)
