from pymongo.collection import Collection

from .interfaces import IDataStore
from .errors import DataStoreException


class MongoDataStore(IDataStore):
    """Data store implementation for Mongo database """

    def __init__(self, db_collection):
        super(MongoDataStore, self).__init__()

        if db_collection and not isinstance(db_collection, Collection):
            raise DataStoreException(f"db_collection has to be a subclass of {Collection.__class__.__name__}")

        self.collection = db_collection

    def __repr__(self):
        return f"MongoDataStore(collection: {self.collection.full_name})"

    def load_forms(self):
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
        return self.collection.find_one({"name": form_name})

    def insert_form(self, form_template):
        """Push new form to the database"""
        result = self.collection.insert_one(form_template)
        identifier = result.inserted_id
        return identifier

    def find_form(self, search_filter, *args, **kwargs):
        """Search query to find forms"""
        cursor = self.collection.find(search_filter, **kwargs)
        for form_template in cursor:
            yield form_template

    def deprecate_form(self, identifier):
        """Deprecate form (forms should not be deleted)"""
        self.collection.update_one({"_id": identifier}, {"$set": {"deprecated": True}})
