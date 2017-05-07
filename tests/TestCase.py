from helloFlask import get_product
import os
import json
import unittest


class TestCase(unittest.TestCase):

    # def test_shoes(self):
        # # response = helloFlask.app('/shoes', follow_redirects=True)
        # response = helloFlask.get_product('/shoes', follow_redirects=True)
        # self.assertEqual(response.status_code, 200)

    # def test_shop(self):
    #     tester = helloFlask.get_http_status_code()
    #     self.assertTrue(tester, isinstance(tester, str))

    def test_get_products(self):
        get_product
        self.assertIn(b'Connection OK', tester)


if __name__ == '__main__':
    unittest.main()
