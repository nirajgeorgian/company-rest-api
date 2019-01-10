import unittest

from tests.test_base import BaseTestClass, post, get, auth_get, auth_put, get_auth_token


class AdminApiTest(BaseTestClass):
    def test_admin_creation(self):
        json_res, dict_res = post(self.client(), "/api/v1/admin", json_dict=self.data)
        self.assertEqual(json_res.status_code, 201)
        self.assertEqual(dict_res["message"], "Successfully created super admin.")

    def test_admin_get(self):
        json_res, dict_res = get(self.client(), "/api/v1/admin")
        self.assertEqual(json_res.status_code, 404)
        post(self.client(), "/api/v1/admin", json_dict=self.data)
        json_res, dict_res = get(self.client(), "/api/v1/admin")
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(dict_res['email'], self.data['email'])

    def test_single_admin_get(self):
        # create the admin
        post(self.client(), "/api/v1/admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        json_res, dict_res = auth_get(self.client(), "/api/v1/admin/{}".format(auth_data['admin_id']), token=token)
        self.assertEqual(json_res.status_code, 200)

    def test_single_admin_update(self):
        # create the admin
        post(self.client(), "/api/v1/admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        put_data = {
            "firstname": "updated_name",
            "lastname": "woohoo"
        }
        u = "/api/v1/admin/{}".format(auth_data['admin_id'])
        json_res, dict_res = auth_put(self.client(), u, put_data, self.auth_data, token)
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(dict_res["firstname"], put_data["firstname"])
        self.assertEqual(dict_res["lastname"], put_data["lastname"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
