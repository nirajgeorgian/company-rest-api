import unittest
import json
import logging
from flask_migrate import Migrate

# import them so that they are discoverable in flask db migrate
from app.models import user as User, admin as Admin, company as Company, employee as Employeen  # noqa: F401
from db import db
from app import create_app
from config import app_config


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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


def post_json(client, url, json_dict):
    return client.post(url, data=json.dumps(json_dict), content_type="application/json")


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))
