from os import path, remove
import unittest
import json
import logging
from flask_migrate import Migrate

# import them so that they are discoverable in flask db migrate
from app.models import user as User, admin as Admin, company as Company, employee as Employeen  # noqa: F401
from db import db
from app import create_app


demo_data = {
    "id": 1,
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


class BaseTestClass(unittest.TestCase):
    db_test_path = path.join(path.dirname(__name__), 'company_test.db')

    def setUp(self):
        self.app = create_app()
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
        remove(self.db_test_path)


def get_auth_token(client, auth_default_cred, headers={}):
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    user_login = client.post("/api/v1/login", data=json.dumps(auth_default_cred), headers=headers)
    user_login_response = json.loads(user_login.data.decode('utf8'))
    return "JWT {}".format(user_login_response['access_token']), user_login_response


def post(client, url, json_dict, headers={}):
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    res = client.post("/api/v1/{}".format(url), data=json.dumps(json_dict), headers=headers)
    return res, json.loads(res.data.decode('utf8'))


def get(client, url, headers={}):
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    res = client.get("/api/v1/{}".format(url), headers=headers)
    return res, json.loads(res.data.decode('utf8'))


def auth_post(client, url, json_dict, token, headers={}):
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    headers['Authorization'] = token
    res = client.post("/api/v1/{}".format(url), data=json.dumps(json_dict), headers=headers)
    return res, json.loads(res.data.decode('utf8'))


def auth_put(client, url, json_dict, token, headers={}):
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    headers['Authorization'] = token
    res = client.put("/api/v1/{}".format(url), data=json.dumps(json_dict), headers=headers)
    return res, json.loads(res.data.decode('utf8'))


def auth_get(client, url, token, headers={}):
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    headers['Authorization'] = token
    res = client.get("/api/v1/{}".format(url), headers=headers)
    return res, json.loads(res.data.decode('utf8'))


def auth_del(client, url, token, headers={}):
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    headers['Authorization'] = token
    res = client.delete("/api/v1/{}".format(url), headers=headers)
    return res, json.loads(res.data.decode('utf8'))
