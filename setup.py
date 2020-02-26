from setuptools import setup

setup(
    name="DynamicForm",
    version="0.2",
    url="",
    author="Rafael S. Mueller",
    author_email="rafael.mueller1@gmail.com",
    description="Read and write forms dynamically from a data store (i.e. database) during runtime",
    packages=["dynamic_form"],
    long_description=open("README.rst").read(), install_requires=['pymongo', 'wtforms']
)
