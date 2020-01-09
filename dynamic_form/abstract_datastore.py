from abc import ABC, abstractmethod


class AbstractDataStore(ABC):
    """An interface to load forms from a data store."""

    def __init__(self):
        pass

    @abstractmethod
    def load_form(self, identifier):
        """Load form based on unique identifier"""
        raise NotImplementedError

    @abstractmethod
    def load_form_by_name(self, name):
        """Load form based on form_name"""
        raise NotImplementedError

    @abstractmethod
    def load_all_forms(self):
        """Load all forms from database"""
        raise NotImplementedError

    @abstractmethod
    def insert_form(self, form_template):
        """Push new form to the database"""
        raise NotImplementedError

    @abstractmethod
    def find_form(self, *args, **kwargs):
        """Search query to find forms"""
        raise NotImplementedError

    @abstractmethod
    def deprecate_form(self, identifier):
        """Deprecate form (forms should not be deleted)"""
        raise NotImplementedError
