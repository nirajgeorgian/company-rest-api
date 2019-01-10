import unittest

from tests.test_base import BaseTestClass, post, get_auth_token, auth_post, auth_get, auth_del, auth_put

employee_data = {
    "email": "user1@example.com",
    "password": "user1",
    "firstname": "user1",
    "lastname": "user1",
    "username": "user1",
    "isAdmin": False
}


class EmployeeApiTest(BaseTestClass):
    def test_employee_create(self):
        # create the admin
        post(self.client(), "admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        json_res, dict_res = auth_post(self.client(), "employees", employee_data, token)
        self.assertEqual(json_res.status_code, 201)
        self.assertEqual(dict_res["username"], employee_data["username"])

    def test_employees_get(self):
        # create the admin
        post(self.client(), "admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        json_res, dict_res = auth_post(self.client(), "employees", employee_data, token)
        json_res, dict_res = auth_get(self.client(), "employees", token)
        self.assertEqual(json_res.status_code, 200)

    def test_employee_get(self):
        # create the admin
        post(self.client(), "admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        json_res, dict_res = auth_post(self.client(), "employees", employee_data, token)
        id = dict_res["employee_id"]
        json_res, dict_res = auth_get(self.client(), "employee/{}".format(id), token)
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(dict_res["username"], employee_data["username"])

    def test_employee_update(self):
        # create the admin
        post(self.client(), "admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        json_res, dict_res = auth_post(self.client(), "employees", employee_data, token)
        id = dict_res["employee_id"]
        update_data = {
            "firstname": "updated name"
        }
        json_res, dict_res = auth_put(self.client(), "employee/{}".format(id), update_data, token)
        self.assertEqual(json_res.status_code, 201)
        self.assertEqual(dict_res["firstname"], update_data["firstname"])

    def test_employee_delete(self):
        # create the admin
        post(self.client(), "admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        json_res, dict_res = auth_post(self.client(), "employees", employee_data, token)
        id = dict_res["employee_id"]
        json_res, dict_res = auth_del(self.client(), "employee/{}".format(id), token)
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(dict_res["username"], employee_data["username"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
