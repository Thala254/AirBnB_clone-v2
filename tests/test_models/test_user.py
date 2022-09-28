#!/usr/bin/python3
""" """
import unittest
import inspect
import pep8 as pycodestyle
from datetime import datetime
import models
from models import storage
from models.user import User


class TestUserDocs(unittest.TestCase):
    """ Tests for documentation and styling of User Class"""

    @classmethod
    def setUpClass(self):
        """setup for docstring tests"""
        self.base_funcs = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test to confirm that models/user.py conform to pep8"""
        for file in ['models/user.py',
                     'tests/test_models/test_user.py']:
            with self.subTest(path=file):
                errors = pycodestyle.Checker(file).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for pressence of module docstring"""
        self.assertTrue(len(models.user.__doc__) >= 1,
                        "User.py needs a docstring")

    def test_class_docstring(self):
        """Test for the presence of User class docstring"""
        self.assertTrue(len(User.__doc__) >= 1,
                        "User class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertTrue(
                    len(func.__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestUser(unittest.TestCase):
    """ Tests for User class """
    def test_var_initialization(self):
        """Check default type"""
        test_user = {'id': "001",
                     'email': "you@g.com",
                     'password': "1234",
                     'first_name': "TEST",
                     'last_name': "REVIEW"}
        model = User(**test_user)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.email, str)
        self.assertIsInstance(model.password, str)
        self.assertIsInstance(model.first_name, str)
        self.assertIsInstance(model.last_name, str)

    def test_no_arguments(self):
        """test initialization without arguments"""
        model = User()
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))
        self.assertTrue(hasattr(model, "email"))
        self.assertTrue(hasattr(model, "password"))
        self.assertTrue(hasattr(model, "first_name"))
        self.assertTrue(hasattr(model, "last_name"))

    def test_save(self):
        """saving the object to storage"""
        test_user = {'id': "001",
                     'email': "you@g.com",
                     'password': "1234",
                     'first_name': "TEST",
                     'last_name': "REVIEW"}
        user = User(**test_user)
        user.save()
        all_users = storage.all('User')
        self.assertIn(f"User.{test_user['id']}", all_users.keys())
        storage.delete(user)
