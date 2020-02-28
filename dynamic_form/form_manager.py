from expiringdict import ExpiringDict

from .interfaces import IDataStore, IFormParser
from .parser_json import JsonFlaskParser as JsonFormParser
from .errors import FormManagerException, FormParserException


class FormManager:
    """A controller which fetches form templates from a data store and converts them into Forms.

    The forms are cached in an expiring dict (default 60 seconds, 100 items). This reduces traffic to the data store.
    """

    def __init__(self, data_store=None, format_parser=JsonFormParser(), initial_load=True, max_age_seconds=60):
        """
        :param format_parser: A custom parsers to convert the database entry into a FlaskForm. Has to inherit from
        the ParserAdapterInterface class.
        :param data_store: A custom database adapter. Has to be an inherit from DbAdapterInterface
        :param initial_load: If all forms should be loaded
        :param max_age_seconds: Expiration time of cached forms

        """

        if not isinstance(data_store, IDataStore):
            raise FormManagerException(f"{data_store.__class__.__name__} has to be a subclass of"
                                       f"{IDataStore.__class__.__name__}")

        if not isinstance(format_parser, IFormParser):
            raise FormManagerException(f"{format_parser.__class__.__name__} has to be a subclass of f"
                                       f"{IFormParser.__name__}")

        self._data_store = data_store
        self._parser = format_parser

        self.form_cache = ExpiringDict(max_len=100, max_age_seconds=max_age_seconds)
        if initial_load:
            self._fetch_forms()

    def set_max_cache_age(self, seconds):
        """Change the expiration time of the form cache"""
        self.form_cache.max_age = seconds

    def get_form_by_name(self, form_name, use_cache=True):
        """Return form based on form_name

        First, local cache is examined for the form. If unsuccessful, it tries to locate the form in the database.

        :param str form_name: the name of the form
        :param use_cache: If false, always load from data store
        :raises: FormManagerException: If neither cache nor database contains form with passed name
        :returns: A form class as defined in the :class:FormParser
        """

        if use_cache and form_name in self.form_cache.keys():
            try:
                return self.form_cache[form_name]
            except KeyError:
                pass

        form_template = self._data_store.load_form_by_name(form_name)

        if not form_template:
            error_msg = f"Fail to load form. No form found with this name (name:{form_name})"
            raise FormManagerException(error_msg)

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
        """Add form to data store

        Before the form template is inserted into the data store, it is parsed into the form format. This ensures that
        only valid form templates are added to the data store. The parsed form is added to the cache.

        :param form_template:
        :raise FormParserException: If the form_template is not parsable
        :return: unique identifier of inserted form
        """
        try:
            form_name, form = self._parser.to_form(form_template)
        except Exception as e:
            raise FormParserException("Fail to parse from template to form.")

        self.form_cache[form_name] = form
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
