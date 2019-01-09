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
            abort(500, message="Some internal fault.")
        admin_user = AdminModel.find_by_user_id(current_identity.id)
        if not admin_user:
            abort(403, message="Please use admin or ask admin to crete company.")
        employees = EmployeeModel.query.all()
        if not len(employees):
            abort(500, message="Some internal fault.")
        res = {"employees": []}
        for employee in employees:
            user = UserModel.find_by_id(employee.user_id)
            employee_id = employee.id
            isAdmin = employee.isAdmin
            firstname = user.firstname
            lastname = user.lastname
            username = user.username
            email = user.email
            res["employees"].append({
                "id": user.id,
                "employee_id": employee_id,
                "isAdmin": isAdmin,
                "firstname": firstname,
                "lastname": lastname,
                "username": username,
                "email": email
            })
        return res, 200

    @jwt_required()
    def post(self):
        data = EmployeeController.parser.parse_args()
        username = data['username']
        email = data['email']
        if UserModel.find_by_username(username) or UserModel.find_by_email(email):
            return {
                'message': "User already exists."
            }, 400
        admin_user = AdminModel.find_by_user_id(current_identity.id)
        if not admin_user:
            abort(403, message="Please use admin or ask admin to crete company.")

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
