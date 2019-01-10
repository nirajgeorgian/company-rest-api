import unittest

from tests.test_base import BaseTestClass, post


class UserModelCase(BaseTestClass):
    def test_login(self):
        post(self.client(), "admin", json_dict=self.data)
        json_res, dict_res = post(self.client(), "login", json_dict=self.auth_data)
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(dict_res['isAdmin'], True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
