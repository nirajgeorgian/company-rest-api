from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import ArgumentError, DataError
from flask_jwt import jwt_required, current_identity
from db import db

from app.models.user import UserModel
from app.models.admin import AdminModel
from app.models.employee import EmployeeModel


class EmployeeController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname', type=str, help='Enter firstname')
    parser.add_argument('lastname', type=str, help='Enter lastname')
    parser.add_argument('username', type=str, help='Enter username')
    parser.add_argument('email', type=str, help='Enter email')
    parser.add_argument('password', type=str, help='Enter password')
    parser.add_argument('isAdmin', type=bool, help='Enter isAdmin')

    @jwt_required()
    def get(self):
        user = UserModel.find_by_id(current_identity.id)
        if not user:
            abort(500, message="Some internal user fault.")
        employees = EmployeeModel.query.all()
        res = {"employees": []}
        if len(employees) == 0:
            return res, 200
        for employee in employees:
            user = UserModel.find_by_id(employee.user_id)
            res["employees"].append(employee.get_employee(user))
        return res, 200

    @jwt_required()
    def post(self):
        data = EmployeeController.parser.parse_args()
        username = data['username']
        email = data['email']
        if (UserModel.find_by_username(username) or UserModel.find_by_email(email)):
            return {
                'message': "User already exists."
            }, 400
        # Because only admin can create employee
        admin_user = AdminModel.find_by_user_id(current_identity.id)
        if not admin_user:
            abort(403, message="Please use admin or ask admin to crete company.")

        # Create a new Employee user
        employee = EmployeeModel(isAdmin=data['isAdmin'])
        user_data = data
        del user_data['isAdmin']
        user = UserModel(**user_data)
        user = user.hash_password()
        user.employee_id = employee
        employee.user_id = user

        # save the database
        try:
            db.session.add(user)
            db.session.add(employee)
            db.session.commit()
        except (ArgumentError, DataError):
            abort(500, message="Server internal error due to invalid argument.")

        return employee.get_employee(user), 201
