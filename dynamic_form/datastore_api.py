import requests


from dynamic_form.abstract_datastore import AbstractDataStore


class ApiDataStore(AbstractDataStore):
    """Concrete implementation for a data store that uses an API"""

    def __init__(self, url):
        self.url = url

    def load_form(self, identifier):
        result = requests.get(f"{self.url}/forms/id/{identifier}")
        yield self._process_results(result)

    def load_form_by_name(self, name):
        header = {"X-Fields": "name, id"}
        res_all_forms = requests.get(f"{self.url}/forms/", headers=header)

        try:
            form_entry = next(filter(lambda entry: entry["name"] == name, res_all_forms.json()))

            res = requests.get(f"{self.url}/forms/id/{form_entry['id']}")

            return res.json()

        except StopIteration:
            raise AttributeError(f"Form with name {name} not found")

    def load_all_forms(self):
        """Load all forms from the API"""
        results = requests.get(f"{self.url}/forms/")

        return self._process_results(results)

    def _process_results(self, results):

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
