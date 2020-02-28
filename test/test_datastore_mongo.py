import unittest
from pymongo import MongoClient

from dynamic_form.errors import DataStoreException
from dynamic_form.datastore_mongodb import MongoDataStore

from test import test_utils


class TestMongoDataStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        client = MongoClient(host="127.0.0.1")
        db = client["test"]
        cls.collection = db["test_form"]

    @classmethod
    def tearDownClass(cls) -> None:
        cls.collection.drop()

    def setUp(self) -> None:
        self.collection.drop()
        self.data_store = MongoDataStore(self.collection)

    def test_wrong_collection_cls(self):

        class NotMongoDataStore:
            pass

        with self.assertRaises(DataStoreException):
            MongoDataStore(db_collection=NotMongoDataStore())

    def test_load_forms_empty(self):
        form_template = self.data_store.load_forms()
        form_list = list(form_template)
        self.assertEqual(len(form_list), 0)


class TestMongoDataStoreWithEntry(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        client = MongoClient(host="127.0.0.1")
        db = client["test"]
        cls.collection = db["test_form"]
        cls.data_store = MongoDataStore(cls.collection)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.collection.drop

    def setUp(self) -> None:
        self.collection.drop()
        self.data_store = MongoDataStore(self.collection)
        form = test_utils.get_login_form()
        self.res = self.data_store.insert_form(form.to_dict())

    def test_load_forms(self):
        form_template = self.data_store.load_forms()
        self.assertEqual(len(list(form_template)), 1)

    def test_load_login_form_by_id(self):
        identifier = self.res
        form = self.data_store.load_form(identifier)
        self.assertEqual(len(form.keys()), 5)

    def test_load_login_form_by_name(self):
        form = self.data_store.load_form_by_name("user_login")
        self.assertEqual(len(form.keys()), 5)

    def test_load_nonexisting_login_form_by_name(self):
        form = self.data_store.load_form_by_name("nonexisting")
        self.assertIsNone(form)

    def test_search_form(self):
        res = self.data_store.find_form(search_filter={"name": "user_login"})

        self.assertEqual(len(list(res)), 1)

    def test_deprecate_form(self):
        identifier = self.res
        self.data_store.deprecate_form(identifier)

        form = self.data_store.load_form(identifier)
        self.assertEqual(form["deprecated"], True)
