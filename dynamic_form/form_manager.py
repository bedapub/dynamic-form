from .interfaces import IDataStore, IFormParser
from .parser_json import JsonFlaskParser as JsonFormParser
from .errors import FormManagerException


class FormManager:
    """A controller class which fetches forms from a data store and converts them into FlaskForms."""

    def __init__(self, data_store=None, format_parser=JsonFormParser(), initial_load=True):
        """
        :param format_parser: A custom parsers to convert the database entry into a FlaskForm. Has to inherit from
        the ParserAdapterInterface class.
        :param data_store: A custom database adapter. Has to be an inherit from DbAdapterInterface
        :param initial_load: If all forms should be loaded

        """

        if not isinstance(data_store, IDataStore):
            raise FormManagerException(f"{data_store.__class__.__name__} has to be a subclass of"
                                       f"{IDataStore.__class__.__name__}")

        if not isinstance(format_parser, IFormParser):
            raise FormManagerException(f"{format_parser.__class__.__name__} has to be a subclass of f"
                                         f"{IFormParser.__name__}")

        self._data_store = data_store
        self._parser = format_parser

        self.form_cache = {}
        if initial_load:
            self._fetch_forms()

    def get_form(self, form_name, use_cache=True):
        """Return form based on form_name

        First, local cache is examined for the form. If unsuccessful, it tries to locate the form in the database.

        :param str form_name: the name of the form
        :param boolean use_cache: If true, first tries to locate form in cache.
        :raises: FormManagerException: If neither cache nor database contains form with passed name
        :returns: A form class
        """

        if use_cache and form_name in self.form_cache.keys():
            return self.form_cache[form_name]
        else:
            form_template = self._data_store.load_form_by_name(form_name)

            form_name, form = self._parser.to_form(form_template)
            self.form_cache[form_name] = form
            return form

    def get_cached_form_names(self):
        """Return names of all form currently in the cache"""
        return self.form_cache.keys()

    def update_form_cache(self):
        """Update local cache with forms from database"""
        self._fetch_forms()

    def insert_form(self, form_template):
        """Add form to data store"""
        return self._data_store.insert_form(form_template)

    def _fetch_forms(self):
        """Fetches all forms from database and stores them in local cache.

        :raises
            DbException: If the collection contains documents with identical form_names
        """
        self.form_cache.clear()
        forms_templates = self._data_store.load_forms()

        for form_template in forms_templates:
            form_name, form = self._parser.to_form(form_template)

            # Prevent overwriting a form which is already in the cache.
            if form_name in self.form_cache.keys():
                raise FormManagerException("Collection contains duplicates with name: {}".format(form_name))

            self.form_cache[form_name] = form
