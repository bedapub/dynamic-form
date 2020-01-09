from setuptools import setup, find_packages

setup(
    name="DynamicForm",
    version="0.1",
    url="",
    author="Rafael S. Mueller",
    author_email="rafael.mueller1@gmail.com",
    description="Read and write forms dynamically from a datastore (i.e. database) during runtime",
    packages=["dynamic_form"],
    long_description=open("README.md").read(), install_requires=['requests', 'pymongo', 'wtforms']
)