import unittest
import json
import logging
from flask_migrate import Migrate

# import them so that they are discoverable in flask db migrate
from app.models import user as User, admin as Admin, company as Company, employee as Employeen  # noqa: F401
from db import db
from app import create_app
from config import app_config
from app.models.user import UserModel
from app.models.employee import EmployeeModel
from app.models.admin import AdminModel


demo_data = {
    "firstname": "duck",
    "lastname": "dodo",
    "username": "duck",
    "email": "duck@example.com",
    "password": "duck"
}
auth_data = {
    "email": "duck@example.com",
    "password": "duck"
}


def post_json(client, url, json_dict):
    return client.post(url, data=json.dumps(json_dict), content_type="application/json")


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


class TestConfig(app_config["testing"]):
    pass


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        self.data = demo_data
        self.auth_data = auth_data
        db.init_app(self.app)
        Migrate(self.app, db)
        logging.disable(logging.CRITICAL)

        # binds the app to current context
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class UserModelCase(BaseTestClass):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        self.data = demo_data
        self.auth_data = auth_data
        db.init_app(self.app)
        Migrate(self.app, db)
        logging.disable(logging.CRITICAL)

        # binds the app to current context
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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
