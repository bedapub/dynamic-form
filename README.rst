Dynamic Form
============

A package to create forms dynamically from a data store during runtime.

Documentation
-------------
Sphinx documentation is available in `/doc`. Change into `/doc` and call `make html` to create the documentation. The
documentation includes a getting started section.

Built with
----------
The core software does not have any dependencies besides the python standard library. The concrete implementations
of the data store and the input parser depend on:

* pyMongo - `MongoDsAdapter`
* requests - `ApiDataStore`
* wt_forms - `JsonFlaskAdapter`
* wtforms - `JsonFlaskAdapter`

Purpose
-------
This package was written during a six month internship and was developed as part of the Study Registration Tool
prototype.



Authors
-------
* **[Rafael Müller](rafael.mueller1@gmail.com)** - Initial work
* **Laura Badi** - Supervisor
