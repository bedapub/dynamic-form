import warnings

from dynamic_form.abstract_datastore import AbstractDataStore
from dynamic_form.abstract_parser import AbstractParserAdapter as AbstractParserAdapter
from dynamic_form.parser_json import JsonFlaskParser as JsonFormParser

class FormManagerException(Exception):
    pass


class FormManager:
    """
    A controller class which fetches forms from a database and converts them into FlaskForms.

    """

    def __init__(self, ds_adapter=None, input_parser=JsonFormParser()):
        """
        :param input_parser: A custom parsers to convert the database entry into a FlaskForm. Has to inherit from
        the ParserAdapterInterface class.
        :param ds_adapter: A custom database adapter. Has to be an inherit from DbAdapterInterface
        """

        if ds_adapter and not isinstance(ds_adapter, AbstractDataStore):
            raise AttributeError(f"{ds_adapter.__name__} has to be a subclass of f{AbstractDataStore.__name__}")

        if not isinstance(input_parser, AbstractParserAdapter):
            raise AttributeError(f"{input_parser.__class__.__name__} has to be a subclass of f"
                                 f"{AbstractParserAdapter.__name__}")

        self.ds_adapter = ds_adapter
        self.parser = input_parser

        # Local cache for all forms
        self.form_cache = {}
        self._fetch_forms()

    def get_form(self, form_name, use_cache=True):
        """Return form based on form_name.

        First, local cache is examined for the form. If unsuccessful, it tries to locate the form in the database.

        :param
        str form_name: the name of the form
        boolean use_cache: If true, first tries to loccate form in cache.
        :raises:
            FormManagerException: If neither cache nor database contains form with passed name
        :returns: A form class
        :rtype: wtforms.FlaskForm
        """

        if use_cache and form_name in self.form_cache.keys():
            return self.form_cache[form_name]
        else:
            form_template = self.ds_adapter.load_form_by_name(form_name)

            # Rise exception if form not found in database
            # try:
            #     next(form_template)
            # except StopIteration as e:
            #     raise FormManagerException("Could not find form with name: {}".format(form_name))

            form_name, form = self.parser.parse_to_form(form_template)
            self.form_cache[form_name] = form
            return form

    def get_form_names(self):
        """Return names of all form currently in the cache
        """
        return self.form_cache.keys()

    def update_form_cache(self):
        """Update local cache with forms from database
        """
        self.form_cache = {}
        self._fetch_forms()

    def new_form(self, form, **kwargs):
        return self.parser.to_template(form, **kwargs)

    def insert_form(self, form_template):
        return self.ds_adapter.insert_form(form_template)

    def _fetch_forms(self):
        """
        Fetches all forms from database and stores them in local cache.

        :raises
            DbException: If the collection contains documents with identical form_names
        """
        forms_template = self.ds_adapter.load_all_forms()

        for form_template in forms_template:
            print(f"Print {form_template.get('name')}")
            form_name, form = self.parser.to_form(form_template)

            # Prevent overwriting a form which is already in the cache.
            if form_name in self.form_cache.keys():
                raise FormManagerException("Collection contains duplicates with name: {}".format(form_name))

            self.form_cache[form_name] = form