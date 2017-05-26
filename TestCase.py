from pprint import pprint
from flask import Flask
import unittest
import helloFlask


app = Flask(__name__)


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.app = app.test_client()

    # Testing response of a GET request
    def test_get_product(self):
        self.app = helloFlask.app.test_client()
        resp = self.app.get('/get_product?get_data=2287400000')
        pprint(resp)
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main().runTests()

