import requests


from dynamic_form.abstract_datastore import AbstractDataStore


class ApiDataStore(AbstractDataStore):

    def __init__(self, url):
        self.url = url

    def load_form(self, identifier):
        raise NotImplementedError

    def load_form_by_name(self, name):
        raise NotImplementedError

    def load_all_forms(self):
        """ Load all forms from the API """
        results = requests.get(f"{self.url}/forms/")

        if results.status_code != 200:
            raise Exception(results.json())

        for result in results.json():
            yield result

    def insert_form(self, form_template):
        raise NotImplementedError
        # results = requests.post(f"{self.url}/form", json=form_template)
        # return results

    def find_form(self, *args, id=None, **kwargs):
        raise NotImplementedError
        # results = requests.get(f"{self.url}/form/id/{id}")
        # return results

    def deprecate_form(self, identifier):
        raise NotImplementedError
