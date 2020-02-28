Dynamic Form
============

A package to create forms dynamically from a data store during runtime.

Documentation
-------------
Please find the documentation on `Read the Docs`_.

.. _Read the docs: https://dynamic-webforms.readthedocs.io/en/latest

Built with
----------
The core component of the software does not have any dependencies besides the python standard library. The concrete
implementations of the data store and the input parser depend on:

* pyMongo - `MongoDataStore`
* wt_forms - `JsonFormParser`
* wtforms - `JsonFormParser`

Purpose
-------
This package was written during a six month internship and was developed as part of the Study Registration Tool
prototype.


Authors
-------
* **Rafael Müller** <mailto:rafa.molitoris@gmail.com> - Initial work
* **Laura Badi** - Supervisor
