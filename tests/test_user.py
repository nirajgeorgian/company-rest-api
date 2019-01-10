import unittest

from tests.test_base import BaseTestClass
from app.models.user import UserModel


class UserModelTest(BaseTestClass):
    def test_user(self):
        u = UserModel(firstname="dodo", lastname="duck", username="dodo", email="dodo@example.com", password="dodo@N9")
        self.assertEqual(u.username, "dodo")


if __name__ == "__main__":
    unittest.main(verbosity=2)
