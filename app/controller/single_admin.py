from flask_restful import Resource, reqparse, abort
from flask_jwt import jwt_required, current_identity

from app.models.admin import AdminModel
from app.models.user import UserModel


class SingleAdminController(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('firstname', type=str, help='Enter firstname')
    parser.add_argument('lastname', type=str, help='Enter lastname')
    parser.add_argument('username', type=str, help='Enter username')
    parser.add_argument('email', type=str, help='Enter email')
    parser.add_argument('password', type=str, help='Enter password')

    @jwt_required()
    def get(self, admin_id):
        admin = AdminModel.find_by_id(admin_id)
        if not admin:
            abort(404, message="no admin data exists.")
        user_id = current_identity.id
        user = UserModel.find_by_id(user_id)
        return admin.get_admin(user), 200

    @jwt_required()
    def put(self, admin_id):
        data = SingleAdminController.parser.parse_args()
        admin = AdminModel.find_by_id(admin_id)
        user_id = current_identity.id
        if not admin:
            abort(404, message="no admin data exists.")
        if not admin.user_id == user_id:
            abort(402, message="Only admin can updtae itself")
        user = UserModel.find_by_id(user_id)
        user.firstname = data.firstname if data.firstname else None
        user.lastname = data.lastname if data.lastname else None
        user.save_to_db()
        return admin.get_admin(user), 200
