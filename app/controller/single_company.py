from flask_restful import Resource, reqparse, abort
from flask_jwt import jwt_required, current_identity

from app.models.admin import AdminModel
from app.models.user import UserModel
from app.models.company import CompanyModel


class SingleCompanyController(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', type=str, help='Enter company name')
    parser.add_argument('description', type=str, help='Enter company description')
    parser.add_argument('employees', action='append')

    @jwt_required()
    def get(self, company_id):
        company = CompanyModel.find_by_id(company_id)
        if not company:
            abort(404, message="no company exist with the provided id.")
        return company.json(), 200

    @jwt_required()
    def put(self, company_id):
        data = SingleCompanyController.parser.parse_args()
        user = UserModel.find_by_id(current_identity.id)
        if not user:
            abort(404, message="no user. Please use valid account")
        admin = AdminModel.find_by_id(user.admin_id.id)
        if not admin:
            abort(404, message="no admin data exists.")
        company = CompanyModel.find_by_id(company_id)
        if not company:
            abort(404, message="no company exist with the provided company_id.")
        company.description = data.description if data.description else company.description
        company.save_to_db()
        return company.json()

    @jwt_required()
    def delete(self, company_id):
        user = UserModel.find_by_id(current_identity.id)
        if not user:
            abort(404, message="no user. Please use valid account")
        admin = AdminModel.find_by_id(user.admin_id.id)
        if not admin:
            abort(404, message="no admin data exists.")
        company = CompanyModel.find_by_id(company_id)
        if not company:
            abort(404, message="no company exist with the provided company_id.")
        company.delete_from_db()
        return company.json(), 200
