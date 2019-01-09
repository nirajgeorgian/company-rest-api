from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import ArgumentError, DataError
from db import db

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
        email = data['email']
        if UserModel.find_by_username(username) or UserModel.find_by_email(email):
            return {
                'message': "User already exists."
            }, 400

        # Create a new Employee user
        employee = EmployeeModel(isAdmin=data['isAdmin'])
        user_data = data
        del user_data['isAdmin']
        user = UserModel(**user_data)
        user = user.hash_password()
        user.users_employees.append(employee)

        # save the database
        try:
            db.session.add(user)
            db.session.add(employee)
            db.session.commit()
        except (ArgumentError, DataError):
            abort(500, message="Server internal error due to invalid argument.")

        return {
            "message": "Successfully created employee."
        }, 201
