import io
import os
import re
from setuptools import setup, find_packages

DOCUMENTATION_URL = "https://dynamic-webforms.readthedocs.io/en/latest/"
SOURCE_CODE_URL = "https://github.com/bedapub/Dynamic-Webforms"

module_path = os.path.dirname(__file__)

with io.open(os.path.join(module_path, "dynamic_form/__init__.py"), "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

with io.open(os.path.join(module_path, "./README.rst"), "rt", encoding="utf8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="Dynamic-Webforms",
    version=version,
    url=SOURCE_CODE_URL,
    project_urls={
        "Documentation": DOCUMENTATION_URL,
        "Code": SOURCE_CODE_URL,
    },
    author="Rafael S. Müller",
    author_email="rafa.molitoris@gmail.com",
    description="A package to dynamically load webforms from a data store (i.e. database) during runtime",
    packages=find_packages("dynamic_webform"),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    install_requires=[
        "pymongo",
        "wtforms",
        "flask_wtf",
        "expiringdict"
    ],
    keywords="form webform database datastore",
    classifiers=[
        "LICENCE :: OSI APPROVED :: GNU Lesser General Public License v3 (LGPLv3)",
        "OPERATION SYSTEM :: OS INDEPENDENT",
        "PROGRAMMING LANGUAGE :: PYTHON"
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
