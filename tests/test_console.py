#!/usr/bin/python3
"""
Contains the class TestConsoleDocs
"""

from datetime import datetime
from contextlib import contextmanager
import inspect
import pep8
import unittest
import io
import sys
import os
import console
from console import HBNBCommand
from models.amenity import Amenity


@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestHBNBCommandDocs(unittest.TestCase):
    """Tests to check the documentation and style of HBNBCommand class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.all_funcs = inspect.getmembers(HBNBCommand, inspect.isfunction)

    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Test tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_console_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")

    def test_cls_funcs_docstrings(self):
        """Test for the presence of docstrings in HBNBCommand methods"""
        for func in self.all_funcs:
            if "_HBNBCommand_" in func[0]:
                self.assertTrue(len(func[1].__doc__) >= 1)


class TestHBNBCommand(unittest.TestCase):
    """ tests on HBNBCommand Class """
    @classmethod
    def setUpClass(self):
        self.cli = HBNBCommand()
        test_args = {'updated_at': datetime(2017, 2, 11, 23, 48, 34, 339879),
                     'id': 'd3da85f2-499c-43cb-b33d-3d7935bc808c',
                     'created_at': datetime(2017, 2, 11, 23, 48, 34, 339743),
                     'name': 'SELF.MODEL'}
        self.model = Amenity(**test_args)
        self.model.save()

    @classmethod
    def tearDownClass(self):
        self.cli.do_destroy("Amenity d3da85f2-499c-43cb-b33d-3d7935bc808c")

    def test_quit(self):
        with self.assertRaises(SystemExit):
            self.cli.do_quit(self.cli)

    # one test for db without time zone, one for file
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db', "db")
    def test_show_correct(self):
        with captured_output() as (out, err):
            self.cli.do_show("Amenity d3da85f2-499c-43cb-b33d-3d7935bc808c")
        output = out.getvalue().strip()
        self.assertFalse(datetime(2017, 2, 11, 23, 48, 26, 45784) in output)
        self.assertTrue(datetime(2017, 2, 11, 23, 48, 34, 339743) in output)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') == 'db', "db")
    def test_show_correct(self):
        with captured_output() as (out, err):
            self.cli.do_show("Amenity d3da85f2-499c-43cb-b33d-3d7935bc808c")
        output = out.getvalue().strip()
        self.assertFalse(
                         "datetime.datetime(2017, 2, 11, 23, 48, 26, 339743)"
                         in output)
        self.assertTrue(
                         "datetime.datetime(2017, 2, 11, 23, 48, 34, 339743)"
                         in output)

    def test_show_error_no_args(self):
        with captured_output() as (out, err):
            self.cli.do_show('')
        output = out.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    def test_show_error_missing_arg(self):
        with captured_output() as (out, err):
            self.cli.do_show("Amenity")
        output = out.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

    def test_show_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_show("Human 1234-5678-9101")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_show_error_class_missing(self):
        with captured_output() as (out, err):
            self.cli.do_show("d3da85f2-499c-43cb-b33d-3d7935bc808c")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_create_no_arg(self):
        with captured_output() as (out, err):
            self.cli.do_create('')
        output = out.getvalue().strip()
        self.assertEqual(output, "** class name missing **")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') == 'db', "db")
    def test_create_with_FS(self):
        with captured_output() as (out, err):
            self.cli.do_create("Amenity")
        output = out.getvalue().strip()

        with captured_output() as (out, err):
            self.cli.do_show("Amenity {}".format(output))
        output2 = out.getvalue().strip()
        self.assertTrue(output in output2)

    def test_destroy_correct(self):
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4901',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': "TEST_DESTROY"}
        testmodel = Amenity(**test_args)
        testmodel.save()
        self.cli.do_destroy("Amenity f519fb40-1f5c-458b-945c-2ee8eaaf4901")

        with captured_output() as (out, err):
            self.cli.do_show("Amenity f519fb40-1f5c-458b-945c-2ee8eaaf4901")
        output = out.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_destroy_error_missing_id(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("Amenity")
        output = out.getvalue().strip()
        self.assertEqual(output, "** instance id missing **")

    def test_destroy_error_class_missing(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("d3da85f2-499c-43cb-b33d-3d7935bc808c")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_destroy_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("Human d3da85f2-499c-43cb-b33d-3d7935bc808c")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_destroy_error_invalid_id(self):
        with captured_output() as (out, err):
            self.cli.do_destroy("Amenity " +
                                "f519fb40-1f5c-AAA-945c-2ee8eaaf4900")
        output = out.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_all_correct(self):
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': 'f519fb40-1f5c-458b-945c-2ee8eaaf4900',
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': "TEST_ALL_CORRECT"}
        testmodel = Amenity(**test_args)
        testmodel.save()
        with captured_output() as (out, err):
            self.cli.do_all("")
        output = out.getvalue().strip()
        self.assertTrue("d3da85f2-499c-43cb-b33d-3d7935bc808c" in output)
        self.assertTrue("f519fb40-1f5c-458b-945c-2ee8eaaf4900" in output)
        self.assertFalse("123-456-abc" in output)

    def test_all_correct_with_class(self):
        with captured_output() as (out, err):
            self.cli.do_all("Amenity")
        output = out.getvalue().strip()
        self.assertTrue(len(output) > 0)
        self.assertTrue("d3da85f2-499c-43cb-b33d-3d7935bc808c" in output)

    def test_all_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_all("Human")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_update_correct(self):
        with captured_output() as (out, err):
            self.cli.do_update("Amenity " +
                               "d3da85f2-499c-43cb-b33d-3d7935bc808c name Bay")
        output = out.getvalue().strip()
        self.assertEqual(output, '')

        with captured_output() as (out, err):
            self.cli.do_show("Amenity d3da85f2-499c-43cb-b33d-3d7935bc808c")
        output = out.getvalue().strip()
        self.assertTrue("Bay" in output)
        self.assertFalse("Ace" in output)

    def test_update_error_invalid_id(self):
        with captured_output() as (out, err):
            self.cli.do_update("Amenity 123-456-abc name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_update_error_no_id(self):
        with captured_output() as (out, err):
            self.cli.do_update("Amenity name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_update_error_invalid_class(self):
        with captured_output() as (out, err):
            self.cli.do_update("Human " +
                               "d3da85f2-499c-43cb-b33d-3d7935bc808c name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_update_error_no_class(self):
        with captured_output() as (out, err):
            self.cli.do_update("d3da85f2-499c-43cb-b33d-3d7935bc808c name Cat")
        output = out.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_update_error_missing_value(self):
        with captured_output() as (out, err):
            self.cli.do_update("Amenity " +
                               "d3da85f2-499c-43cb-b33d-3d7935bc808c name")
        output = out.getvalue().strip()
        self.assertEqual(output, "** value missing **")

    def test_state_argument(self):
        with captured_output() as (out, err):
            self.cli.do_create('State name="WEIRD"')
        with captured_output() as (out, err):
            self.cli.do_all("State")
        output = out.getvalue().strip()
        self.assertTrue("WEIRD" in output)

    def test_city_2_arguments(self):
        with captured_output() as (out, err):
            self.cli.do_create('State name="Arizona"')
        output = out.getvalue().strip()
        with captured_output() as (out, err):
            self.cli.do_create('City state_id="{}" name="Fremont"'.format(
                output))

    def test_city_2_arguments_space(self):
        with captured_output() as (out, err):
            self.cli.do_create('State name="Arizona"')
        output = out.getvalue().strip()
        with captured_output() as (out, err):
            self.cli.do_create('City state_id="{}" name="Alpha_Beta"'.format(
                output))
        output = out.getvalue().strip()
        with captured_output() as (out, err):
            self.cli.do_show('City {}'.format(output))
        output = out.getvalue().strip()
        self.assertTrue("Alpha Beta" in output)

    def test_place(self):
        with captured_output() as (out, err):
            self.cli.do_create('State name="Another_State"')
        state_id = out.getvalue().strip()
        with captured_output() as (out, err):
            self.cli.do_create('City state_id="{}" name="Alpha_Beta"'.format(
                state_id))
        city_id = out.getvalue().strip()
        with captured_output() as (out, err):
            self.cli.do_create('User email="m@a.com" password="1234" '
                               'first_name="John" last_name="Doe"')
        user_id = out.getvalue().strip()
        with captured_output() as (out, err):
            self.cli.do_create('Place city_id="{}" user_id="{}"'
                               ' name="My_house"'
                               ' description="no_description_yet"'
                               ' number_rooms=4 number_bathrooms=1 max_guest=3'
                               ' price_by_night=100 latitude=120.12'
                               ' longitude=101.4'.format(city_id, user_id))
        output = out.getvalue().strip()
        with captured_output() as (out, err):
            self.cli.do_show('Place {}'.format(output))
        output = out.getvalue().strip()
        self.assertTrue("My house" in output)
        self.assertTrue("100" in output)
        self.assertTrue("120.12" in output)


if __name__ == "__main__":
    unittest.main()
