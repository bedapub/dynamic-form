===============
Getting started
===============

Form Manager
============
The :class:`FormManager` is the controller of this package. It is his job to load and save forms from and to a data
store. It can be found in :py:mod:`dynamic_form.form_manager.FormManager`.


The constructor of the :class:`FormManager` expects two arguments: a data store adapter (`ds_adapter`) and an input
parser (`input_parser`). If the data store contains a form, we load it through the form manager by the form's name.

.. code-block:: python

    from dynamic_form import ApiDataStore, JsonFlaskParser


    form_manager = FormManager(
                        ds_adapter=ApiDataStore(),
                        input_parser=JsonFlaskParser())

    form_manager.get_form("signup")


Data Store Adapter & Input Parser
=================================
The data store adapter and the input parser allow to use the :class:`FormManager` with any combination of a data
store and form. The package comes with a concrete implementation for both, the data store and the input parser.

- The data store adapter serves as the interface to the underlying data store. It is responsible to fetch and dump
  forms in the data store representation.

- The input parser is responsible to convert form into and from the data store representation.
  representation.

All concrete implementation of the data store adapter and the input parser have to inherit from their abstract base
classes:
:py:mod:`dynamic_form.abstract_datastore.AbstractDataStore` and
:py:mod:`dynamic_form.abstract_parser.AbstractParserAdapter`.


API Data Store
==============
The :py:mod:`dynamic_form.datastore_api.ApiDataStore` accesses the data store through an API. Forms are fetched from
`<url>/forms/` where `<url>` is passed as an argument to the constructor.


Json Flask Parser
=================
The :py:mod:`dynamic_form.parser_json.JsonFlaskParser` converts a json document into a FlaskForm.
