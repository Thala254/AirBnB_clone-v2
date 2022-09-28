#!/usr/bin/python3
""" """
import unittest
import inspect
import pep8 as pycodestyle
from datetime import datetime
import models
from models import storage
from models.state import State


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


class TestState(unittest.TestCase):
    """ Tests for State class """
    def test_minimal_creation(self):
        """creating an object with no arguments"""
        model = State()
        self.assertTrue(hasattr(model, "name"))
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))

    def test_var_initialization(self):
        """Check default type"""
        model = State()
        self.assertIsInstance(model.created_at, datetime)

    def test_save(self):
        """Try to save the object to storage"""
        test_state = {'id': "009",
                      'created_at': datetime(2017, 2, 12, 00, 31, 55, 331997),
                      'name': "TEST STATE FOR STATE"}
        state = State(**test_state)
        state.save()
        all_states = storage.all("State")
        self.assertIn(f"State.{test_state['id']}", all_states.keys())
        storage.delete(state)
