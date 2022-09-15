#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import TestBasemodel
from models.state import State
import unittest
import inspect
import pep8 as pycodestyle
import models


class TestStateDocs(unittest.TestCase):
    """ Tests for documentation and styling of State Class"""

    @classmethod
    def setUpClass(self):
        """setup for docstring tests"""
        self.base_funcs = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test to confirm that models/state.py conform to pep8"""
        for file in ['models/state.py',
                     'tests/test_models/test_state.py']:
            with self.subTest(path=file):
                errors = pycodestyle.Checker(file).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for pressence of module docstring"""
        self.assertTrue(len(models.state.__doc__) >= 1,
                        "State.py needs a docstring")

    def test_class_docstring(self):
        """Test for the presence of State class docstring"""
        self.assertTrue(len(State.__doc__) >= 1,
                        "State class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in State methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertTrue(
                    len(func.__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class test_state(TestBasemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)
