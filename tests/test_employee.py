import unittest
from db import db

from tests.test_base import BaseTestClass
from app.models.user import UserModel
from app.models.employee import EmployeeModel


class EmployeeModelTest(BaseTestClass):
    def test_employee(self):
        e = EmployeeModel(isAdmin=False)
        u = UserModel(firstname="dodo", lastname="duck", username="dodo", email="dodo@example.com", password="dodo")
        u.users_employees.append(e)

        # save to local db
        db.session.add(u)
        db.session.add(e)
        db.session.commit()

        user = UserModel.find_by_username("dodo")
        employee = EmployeeModel.query.filter_by(user_id=user.id).first()

        self.assertEqual(user.username, "dodo")
        self.assertEqual(user.email, "dodo@example.com")
        self.assertEqual(employee.user_id, user.id)
        self.assertFalse(employee.isAdmin)


if __name__ == "__main__":
    unittest.main(verbosity=2)
