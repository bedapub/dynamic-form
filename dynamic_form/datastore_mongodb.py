from pymongo import MongoClient

from dynamic_form.abstract_datastore import AbstractDataStore


class MongoDsAdapter(AbstractDataStore):
    """Datastore implementation for a Mongo database """

    def __init__(self, database, form_collection):
        super(MongoDsAdapter, self).__init__()

        if not isinstance(database.client, MongoClient):
            raise AttributeError("Client must be an instance of MongoClient")

        self.client = database.client
        self.db = database
        self.collection = self.db[form_collection]

    def load_all_forms(self):
        """Load all forms from database"""
        cursor = self.collection.find({})
        for form_template in cursor:
            yield form_template

    def load_form(self, identifier):
        """Load form based on unique identifier"""
        return self.collection.find_one({"_id": identifier})

    def load_form_by_name(self, form_name):
        """
       load form based on form_name
        """
        return self.collection.find_one({"form_name":form_name})

    def insert_form(self, form_template):
        """Push new form to the database"""
        result = self.collection.insert_one(form_template)
        return result

    def find_form(self, search_filter, *args, **kwargs):
        """Search query to find forms"""
        cursor = self.collection.find(search_filter, **kwargs)
        for form_template in cursor:
            yield form_template

    def deprecate_form(self, identifier):
        """Deprecate form (forms should not be deleted)"""
        raise NotImplementedError
