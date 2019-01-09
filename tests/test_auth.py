import unittest
from db import db

from tests.test_base import BaseTestClass, post_json, json_of_response
from app.models.user import UserModel
from app.models.employee import EmployeeModel
from app.models.admin import AdminModel


class UserModelCase(BaseTestClass):
    def test_admin_creation(self):
        res = post_json(self.client(), "/api/v1/admin", json_dict=self.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_of_response(res), {"message": "Successfully created super admin."})

    def test_admin_get(self):
        res = self.client().get("/api/v1/admin")
        self.assertEqual(res.status_code, 404)
        post_json(self.client(), "/api/v1/admin", json_dict=self.data)
        after_post_res = self.client().get("/api/v1/admin")
        self.assertEqual(after_post_res.status_code, 200)

    def test_login(self):
        post_json(self.client(), "/api/v1/admin", json_dict=self.data)
        login_res = post_json(self.client(), "/api/v1/login", json_dict=self.auth_data)
        self.assertEqual(login_res.status_code, 200)

    def test_user(self):
        u = UserModel(firstname="dodo", lastname="duck", username="dodo", email="dodo@example.com", password="dodo@N9")
        self.assertEqual(u.username, "dodo")

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

    def test_createadmin(self):
        u = UserModel(firstname="dodo", lastname="duck", username="dodo", email="dodo@example.com", password="dodo")
        a = AdminModel()
        u.admin_id = a

        db.session.add(u)
        db.session.add(a)
        db.session.commit()

        user = UserModel.find_by_username("dodo")
        admin = AdminModel.query.filter_by(user_id=user.id).first()
        self.assertEqual(admin.user_id, user.id)


if __name__ == "__main__":
    unittest.main(verbosity=2)
