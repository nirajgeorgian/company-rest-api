from flask_restful import Resource, reqparse, abort
from flask_jwt import jwt_required

from app.models.user import UserModel
from app.models.employee import EmployeeModel


class SingleEmployeeController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname', type=str, help='Enter firstname')
    parser.add_argument('lastname', type=str, help='Enter lastname')
    parser.add_argument('username', type=str, help='Enter username')
    parser.add_argument('email', type=str, help='Enter email')
    parser.add_argument('password', type=str, help='Enter password')

    @jwt_required()
    def get(self, employee_id):
        employee = EmployeeModel.find_by_id(employee_id)
        if not employee:
            abort(404, message="No Employee exists.")
        user = UserModel.find_by_id(employee.user_id)
        return {
            "employee": employee.get_employee(user)
        }, 200

    @jwt_required()
    def put(self, employee_id):
        data = SingleEmployeeController.parser.parse_args()
        employee = EmployeeModel.find_by_id(employee_id)
        if not employee:
            abort(404, message="No Employee exists.")
        user = UserModel.find_by_id(employee.user_id)
        user.firstname = data.firstname if data.firstname else None
        user.lastname = data.lastname if data.lastname else None
        user.save_to_db()
        return {
            "employee": employee.get_employee(user)
        }, 201

    @jwt_required()
    def delete(self, employee_id):
        employee = EmployeeModel.find_by_id(employee_id)
        if not employee:
            abort(404, message="No Employee exists.")
        employee.delete_from_db()
        return {
            "message": "Successfully deleted {}".format(employee.id)
        }, 200
