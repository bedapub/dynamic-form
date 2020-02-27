===============
Getting started
===============

Workflow
========
To load a form, the Form Manager is instructed to create a form. The Form Manager passes the request to the Data
Store. The Data Store establishes a connection to the database and downloads the form template and returns it
to the Form Manager. The Form Parser is requested to convert the form template into a form. The converted form is
returned via the Form Manager.

.. figure:: ./images/DynamicForm_Workflow.png
    :width: 400
    :align: center
    :alt: Workflow of dynamic form

    The workflow to load a form from a data store.

Components
==========
Dynamic form consists of four components:

1. Form Manager
2. Data Store
3. Form Parser
4. Template Builder

There are interfaces for Data Store and Form Parser. This allows any combination of data sources and form types. The
corresponding implementations are passed to the Form Manager. All concrete implementation of the data store and the
form parser have to inherit from their abstract base classes: :py:mod:`dynamic_form.interfaces.IDataStore` and
:py:mod:`dynamic_form.interfaces.IFormParser`, respectively.

Form Manager
------------
The :class:`FormManager` is the controller of this package. It is his job to load and save forms from and to a data
store. It can be found in :py:mod:`dynamic_form.form_manager.FormManager`. The constructor of the
:class:`FormManager` expects two arguments: a data store and a form parser. If the data store contains a form, we
load it through the form manager by the form's name.

.. code-block:: python

    from pymongo import MongoClient
    from dynamic_form import FormManager, MongoDataStore, JsonFlaskParser

    client = MongoClient()
    form_manager = FormManager(
                        data_store=MongoDataStore(client["database"]["collection"]),
                        input_parser=JsonFlaskParser())

    form_manager.get_form("signup")


Data Store
----------
The data store serves as the interface to the underlying data store. It is responsible to fetch and dump forms in the
data store representation.

Form Parser
-----------
The form parser is responsible to convert form templates from the data store into forms.
