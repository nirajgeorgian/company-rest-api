import unittest

from tests.test_base import BaseTestClass, post, get_auth_token, auth_post, auth_put, auth_get, auth_del

company_data = {
    "name": "company1",
    "description": "simple company1"
}


class CompanyApiTest(BaseTestClass):
    def test_company_create(self):
        # create the admin
        post(self.client(), "admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        json_res, dict_res = auth_post(self.client(), "companies", company_data, token)
        self.assertEqual(json_res.status_code, 201)
        self.assertEqual(dict_res["name"], company_data["name"])
        json_res, dict_res = auth_post(self.client(), "companies", company_data, token)
        self.assertEqual(json_res.status_code, 409)
        self.assertEqual(dict_res["message"], "Company already exists.")

    def test_companies_get(self):
        # create the admin
        post(self.client(), "admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        json_res, dict_res = auth_post(self.client(), "companies", company_data, token)
        json_res, dict_res = auth_get(self.client(), "companies", token)
        self.assertEqual(json_res.status_code, 200)

    def test_company_get(self):
        # create the admin
        post(self.client(), "admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        json_res, dict_res = auth_post(self.client(), "companies", company_data, token)
        id = dict_res["id"]
        json_res, dict_res = auth_get(self.client(), "company/{}".format(id), token)
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(dict_res["name"], company_data["name"])

    def test_company_update(self):
        # create the admin
        post(self.client(), "admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        json_res, dict_res = auth_post(self.client(), "companies", company_data, token)
        id = dict_res["id"]
        update_data = {
            "description": "simple company1"
        }
        json_res, dict_res = auth_put(self.client(), "company/{}".format(id), update_data, token)
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(dict_res["description"], "simple company1")

    def test_company_delete(self):
        # create the admin
        post(self.client(), "admin", json_dict=self.data)
        # receive the login token
        token, auth_data = get_auth_token(self.client(), self.auth_data)
        json_res, dict_res = auth_post(self.client(), "companies", company_data, token)
        id = dict_res["id"]
        json_res, dict_res = auth_del(self.client(), "company/{}".format(id), token)
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(dict_res["name"], company_data["name"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
