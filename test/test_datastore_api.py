import unittest

from dynamic_form.form_manager import FormManager
from dynamic_form.datastore_api import ApiDataStore


class MyTestCase(unittest.TestCase):

    @unittest.skip
    def test_get_login_form(self):
        ds = ApiDataStore(url="http://127.0.0.1:5001")
        form_manager = FormManager(ds_adapter=ds)


if __name__ == '__main__':
    unittest.main()
