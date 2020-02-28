import unittest
import time

from bson import ObjectId
from pymongo import MongoClient
import wtforms

from dynamic_form import FormManager, MongoDataStore
from dynamic_form.errors import FormManagerException
from test import test_utils


class TestFormManagerInit(unittest.TestCase):
    """Test Initialization of Form Manager"""

    def test_init_wrong_data_store(self):
        class DataStore:
            pass

        with self.assertRaises(FormManagerException):
            FormManager(data_store=DataStore)

    def test_init_wrong_form_parser(self):
        class UselessParser:
            pass

        with self.assertRaises(FormManagerException):
            client = MongoClient()
            FormManager(data_store=MongoDataStore(client["test_db"]["test_collection"]), format_parser=UselessParser())


class TestFormManagerInsert(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        client = MongoClient()

        cls.collection = client["test"]["form_test"]

        cls.data_store = MongoDataStore(cls.collection)
        cls.form_manager = FormManager(data_store=cls.data_store)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.collection.drop()

    @classmethod
    def setUp(cls) -> None:
        cls.collection.drop()

    def test_init_without_initial_load(self):
        form_manager = FormManager(self.data_store, initial_load=False)
        self.assertEqual(len(form_manager.get_cached_form_names()), 0)

    def test_insert_form(self):
        from_template = test_utils.get_login_form()
        res = self.form_manager.insert_form(from_template.to_dict())
        self.assertIsInstance(res, ObjectId)


class TestFromFormManagerFetch(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        form_template = test_utils.get_login_form()

        client = MongoClient()
        cls.collection = client["test"]["form_test"]
        cls.collection.drop()

        cls.data_store = MongoDataStore(cls.collection)
        cls.data_store.insert_form(form_template=form_template.to_dict())

    def setUp(self) -> None:
        self.form_manager = FormManager(data_store=self.data_store)

    def test_load_form_by_name_from_cache(self):
        LoginForm = self.form_manager.get_form_by_name("user_login")
        self.assertTrue(issubclass(LoginForm, wtforms.Form))

    def test_load_form_by_name_expired_cache(self):
        """Manually reduce expiration time"""
        self.form_manager.set_max_cache_age(0.01)
        time.sleep(0.02)
        LoginForm = self.form_manager.get_form_by_name("user_login")
        self.assertTrue(issubclass(LoginForm, wtforms.Form))

    def test_load_form_by_nonexisting_name(self):
        with self.assertRaises(FormManagerException):
            self.form_manager.get_form_by_name("nonexisting")

    def test_cached_form_names(self):
        names = self.form_manager.get_cached_form_names()
        self.assertListEqual(list(names), ["user_login"])

    def test_update_form_cache(self):
        self.form_manager.form_cache.clear()
        self.assertEqual(len(self.form_manager.get_cached_form_names()), 0)
        self.form_manager.update_form_cache()
        self.assertEqual(len(self.form_manager.get_cached_form_names()), 1)

class TestFormManagerManyForms(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        client = MongoClient()
        cls.collection = client["test"]["form_test"]
        cls.collection.drop()

        cls.data_store = MongoDataStore(cls.collection)

    def setUp(self) -> None:
        from_templates = test_utils.get_many_login_forms(num=5)

        self.form_manager = FormManager(data_store=self.data_store)
        self.form_manager.form_cache.max_len = 3
        for form_template in from_templates:
            self.form_manager.insert_form(form_template=form_template.to_dict())

    def test_many_forms(self):
        names = self.form_manager.get_cached_form_names()
        self.assertEqual(len(names), 3)

        LoginForm_0 = self.form_manager.get_form_by_name("user_login_0")
        self.assertTrue(issubclass(LoginForm_0, wtforms.Form))




