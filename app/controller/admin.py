from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import ArgumentError, DataError
from flask_jwt import jwt_required, current_identity
from db import db

from app.models.user import UserModel
from app.models.admin import AdminModel
from app.models.company import CompanyModel
from app.models.employee import EmployeeModel


class AdminController(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('firstname', required=True, type=str, help='Enter firstname')
    parser.add_argument('lastname', required=True, type=str, help='Enter lastname')
    parser.add_argument('username', required=True, type=str, help='Enter username')
    parser.add_argument('email', required=True, type=str, help='Enter email')
    parser.add_argument('password', required=True, type=str, help='Enter password')

    def post(self):
        existing_admin = AdminModel.query_for_admin()
        if existing_admin:
            abort(404, message="Super Admin already exist.")
        data = AdminController.parser.parse_args()
        user = UserModel(**data)
        user = user.hash_password()
        admin = AdminModel()
        user.admin_id = admin

        # Save to database
        try:
            db.session.add(user)
            db.session.add(admin)
            db.session.commit()
        except (ArgumentError, DataError):
            abort(500, message="Server internal error due to invalid argument.")

        return {
            "message": "Successfully created super admin."
        }, 201

    # Check for existing of superadmin
    def get(self):
        admins = AdminModel.query_for_admin()
        if admins:
            admin = admins[0]
            user_id = admin.id
            user = UserModel.find_by_id(user_id)
            if user:
                return {
                    "admin": admin.json(),
                    "user": user.json()
                }, 200
        abort(404, message="no super admin exist.")


class AdminEmployeesController(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('firstname', required=True, type=str, help='Enter firstname')
    parser.add_argument('lastname', required=True, type=str, help='Enter lastname')
    parser.add_argument('username', required=True, type=str, help='Enter username')
    parser.add_argument('email', required=True, type=str, help='Enter email')
    parser.add_argument('password', required=True, type=str, help='Enter password')
    parser.add_argument('isAdmin', required=True, type=bool, help='Enter isAdmin')

    @jwt_required()
    def post(self):
        data = AdminEmployeesController.parser.parse_args()
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


class AdminCompanyController(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', required=True, type=str, help='Enter company name')

    @jwt_required()
    def post(self):
        data = AdminCompanyController.parser.parse_args()
        name = data['name']
        old_company = CompanyModel.find_by_name(name)
        if old_company:
            abort(404, message="Company already exists.")
        admin_user = AdminModel.find_by_user_id(current_identity.id)
        if not admin_user:
            abort(403, message="Please use admin or ask admin to crete company.")
        company = CompanyModel(**data)
        admin_user.companies.append(company)

        # save the database
        try:
            db.session.add(admin_user)
            db.session.add(company)
            db.session.commit()
        except (ArgumentError, DataError):
            abort(500, message="Server internal error due to invalid argument.")

        return {
            "message": "Successfully created company."
        }, 201
