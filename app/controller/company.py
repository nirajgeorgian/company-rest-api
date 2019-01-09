from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
# from sqlalchemy.exc import ArgumentError, DataError
# from db import db

# from app.models.user import UserModel


class CompanyController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('employees', action='append')

    @jwt_required
    def get(self):
        pass

    @jwt_required()
    def post(self):
        pass


class SingleCompanyController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('employees', action='append')

    @jwt_required
    def get(self):
        pass

    @jwt_required()
    def put(self):
        pass
