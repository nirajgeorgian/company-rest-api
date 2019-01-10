from flask_restful import Resource, reqparse, abort
from flask_jwt import jwt_required, current_identity
from sqlalchemy.exc import ArgumentError, DataError
from db import db

from app.models.user import UserModel
from app.models.admin import AdminModel
from app.models.company import CompanyModel


class CompanyController(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', type=str, help='Enter company name')
    parser.add_argument('description', type=str, help='Enter company description')
    parser.add_argument('employees', action='append')

    @jwt_required()
    def post(self):
        data = CompanyController.parser.parse_args()
        name = data['name']
        old_company = CompanyModel.find_by_name(name)
        if old_company:
            abort(404, message="Company already exists.")
        admin_user = AdminModel.find_by_user_id(current_identity.id)
        if not admin_user:
            abort(403, message="Please use admin or ask admin to crete company.")
        company = CompanyModel(name=data['name'], description=data['description'])
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

    @jwt_required()
    def get(self):
        user = UserModel.find_by_id(current_identity.id)
        if not user:
            abort(500, message="Some internal fault on user.")
        admin_user = AdminModel.find_by_user_id(current_identity.id)
        if not admin_user:
            abort(403, message="Please use admin or ask admin to crete company.")
        companies = CompanyModel.query.all()
        if not len(companies):
            return {
                "companies": companies
            }
        res = {"companies": []}
        for company in companies:
            res["companies"].append(company.json())
        return res, 200
