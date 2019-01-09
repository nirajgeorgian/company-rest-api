from flask_restful import Resource, reqparse

from app.models.user import UserModel
from app.models.employee import EmployeeModel


class EmployeeController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname', type=str, help='Enter firstname')
    parser.add_argument('lastname', type=str, help='Enter lastname')
    parser.add_argument('username', type=str, help='Enter username')
    parser.add_argument('email', type=str, help='Enter email')
    parser.add_argument('password', type=str, help='Enter password')
    parser.add_argument('isAdmin', type=bool, help='Enter isAdmin')

    def post(self):
        data = EmployeeController.parser.parse_args()
        username = data['username']
        if UserModel.find_by_username(username):
            return {
                'message': "User already exists with this username %s".format(username)
            }, 400

        # Create a new Employee user
        user = UserModel(**data)
        employee = EmployeeModel(**data)

        # save the database
        user.save_to_db()
        employee.save_to_db()

        return {
            "message": "Successfully created employee."
        }, 201
