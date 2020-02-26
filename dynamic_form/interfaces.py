from abc import ABC, abstractmethod


class IFormParser(ABC):
    """Interface for form parser"""

    @abstractmethod
    def to_form(self, template_form):
        """Convert from data store format to form format"""
        raise NotImplementedError

    @abstractmethod
    def to_template(self, form, **kwargs):
        """Convert from form format to data store format"""
        raise NotImplementedError


class IDataStore(ABC):
    """interface to load form from data store."""

    @abstractmethod
    def load_form(self, identifier):
        """Load form from data store based on unique identifier"""
        raise NotImplementedError

    @abstractmethod
    def insert_form(self, form_template):
        """Insert form into data store"""
        raise NotImplementedError

    @abstractmethod
    def load_form_by_name(self, name):
        """Load form from data store based on name"""
        raise NotImplementedError

    @abstractmethod
    def load_forms(self):
        """Load all forms from data store"""
        raise NotImplementedError

    @abstractmethod
    def find_form(self, *args, **kwargs):
        """Find form in data store based on search query"""
        raise NotImplementedError

    @abstractmethod
    def deprecate_form(self, identifier):
        """Deprecate form in data store"""
        raise NotImplementedError
