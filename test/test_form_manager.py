import unittest
from pymongo import MongoClient

from dynamic_form import FormManager, MongoDataStore
from dynamic_form.errors import FormManagerException
from test import test_utils


class TestFormManagerInit(unittest.TestCase):

    def test_init_wrong_data_store(self):

        class DataStore:
            pass

        with self.assertRaises(FormManagerException):
            FormManager(data_store=DataStore)

    def test_init_wrong_parser(self):

        class UselessParser:
            pass

        with self.assertRaises(FormManagerException):
            client = MongoClient()
            FormManager(data_store=MongoDataStore(client["test_db"]["test_collection"]), format_parser=UselessParser())


class TestFormManager(unittest.TestCase):

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
    def setUp(self) -> None:
        self.collection.drop()

    def test_init_without_initial_load(self):
        FormManager(self.data_store, initial_load=False)

    def test_insert_form(self):
        from_template = test_utils.get_login_form()
        self.form_manager.insert_form(from_template.to_dict())

    def test_load_forms(self):
        from_template = test_utils.get_login_form()
        self.form_manager.insert_form(from_template.to_dict())
        form = self.form_manager.get_form(form_name="user_login", use_cache=False)

    def test_update_cache(self):
        from_template = test_utils.get_login_form()
        self.form_manager.insert_form(from_template.to_dict())
        self.form_manager.update_form_cache()

        self.assertEqual(len(self.form_manager.form_cache.keys()), 1)



class TestFormManagerCache(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        from_template = test_utils.get_login_form()

        client = MongoClient()
        cls.collection = client["test"]["form_test"]

        cls.data_store = MongoDataStore(cls.collection)
        cls.data_store.insert_form(form_template=from_template.to_dict())
        cls.form_manager = FormManager(data_store=cls.data_store)

    def test_load_form_from_cache(self):
        form = self.form_manager.get_form("user_login", use_cache=True)

    def test_get_form_names(self):
        names = self.form_manager.get_cached_form_names()

        self.assertEqual(len(names), 1)
