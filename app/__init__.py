from os import path, getenv
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api, abort
from flask_jwt import JWT
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from dotenv import load_dotenv

# local import\
# import them so that they are discoverable in flask db migrate
from app.models import user as User, admin as Admin, company as Company, employee as Employee  # noqa: F401
from config import app_config
from db import db
from app.security import authenticate, identity
from app.models.user import UserModel
from app.models.admin import AdminModel
from app.controller.employee import EmployeeController
from app.controller.company import CompanyController, SingleCompanyController
from app.controller.admin import AdminController


def create_app():
    # load dotenv in the base root
    APP_ROOT = path.join(path.dirname(__file__), '..')
    dotenv_path = path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)
    app = Flask(__name__)
    """Add appropiate configuration"""
    config_name = getenv('APP_SETTINGS', 'development')
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    jwt = JWT(app, authenticate, identity)
    bcrypt = Bcrypt(app)
    Migrate(app, db)

    @jwt.authentication_handler
    def custom_jwt_authenticate(email, password):
        user = UserModel.find_by_email(email)
        if user and bcrypt.check_password_hash(user.password, password):
            return user

    @jwt.auth_response_handler
    def customized_jwt_response(access_token, identity):
        admins = AdminModel.query_for_admin()
        if (len(admins) > 0):
            if admins[0].user_id == identity.id:
                return jsonify({
                    'access_token': access_token.decode('utf-8'),
                    'user_id': identity.id,
                    'isAdmin': True,
                    'admin_id': admins[0].id
                })
            else:
                return jsonify({
                    'access_token': access_token.decode('utf-8'),
                    'user_id': identity.id,
                    'isAdmin': False,
                    'admin_id': None
                })

    @jwt.jwt_error_handler
    def customized_jwt_error(error):
        abort(error.status_code, message=error.description)

    # Logging configuration
    logging.basicConfig()
    logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    logging.disable(logging.CRITICAL)

    api = Api(app)
    # Add Controllers
    api.add_resource(AdminController, '/api/v1/admin')
    api.add_resource(EmployeeController, '/api/v1/employee')
    api.add_resource(CompanyController, '/api/v1/company')
    api.add_resource(SingleCompanyController, '/api/v1/company/<int:company_id>')

    # binds the app to current context
    with app.app_context():
        db.create_all()

    return app
