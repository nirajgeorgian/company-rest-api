from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import ArgumentError, DataError
from db import db

from app.models.user import UserModel
from app.models.admin import AdminModel


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
