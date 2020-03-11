import io
import os
import re
from setuptools import setup, find_packages

DOCUMENTATION_URL = "https://dynamic-form.readthedocs.io/en/stable/"
SOURCE_CODE_URL = "https://github.com/bedapub/dynamic-form"

module_path = os.path.dirname(__file__)

with io.open(os.path.join(module_path, "dynamic_form/__init__.py"), "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

with io.open(os.path.join(module_path, "./README.rst"), "rt", encoding="utf8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="dynamic_form",
    version=version,
    url=SOURCE_CODE_URL,
    project_urls={
        "Documentation": DOCUMENTATION_URL,
        "Code": SOURCE_CODE_URL,
    },
    author="Rafael S. Müller",
    author_email="rafa.molitoris@gmail.com",
    description="A package to dynamically load webforms from a data store (i.e. database) during runtime",
    packages=find_packages(),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    install_requires=[
        "pymongo>=3.10.1",
        "wtforms>=2.2.1",
        "flask_wtf>=0.14.2",
        "expiringdict>=1.2.0"
    ],
    keywords="form webform database datastore",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
    ],
    extra_require={
        "dev": [
            "unittest"
            "coverage",
        ],
        "docs": [
            "Sphinx",
            "sphinx-rdt-theme"
        ],
    }
)
