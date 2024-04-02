from .imports import *
from ..models import Employee


class PostEmployee(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('employee_id', type=str, required=True, help="Employee ID cannot be blank.")
        parser.add_argument('department_id', type=int, required=True, help="Department ID cannot be blank.")
        parser.add_argument('first_name', type=str, required=True, help="First name cannot be blank.")
        parser.add_argument('last_name', type=str, required=True, help="Last name cannot be blank.")
        parser.add_argument('start_date', type=str, required=True, help="Start date cannot be blank.")  # Consider using a custom date type
        parser.add_argument('end_date', type=str, store_missing=False)  # Optional, use store_missing=False to exclude from parsed args if not provided
        parser.add_argument('notes', type=str, store_missing=False)  # Optional, JSON string, validate and parse in your logic
        data = parser.parse_args()

        new_employee = Employee(**data)
        try:
            db.session.add(new_employee)
            db.session.commit()
            return {'employee_id': new_employee.employee_id}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Failed to create new employee. The server encountered an error.'}, 500


class GetEmployee(Resource):
    def get(self, employee_id):
        employee = Employee.query.get(employee_id)
        if employee:
            return {
                'employee_id': employee.employee_id,
                'department_id': employee.department_id,
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'start_date': employee.start_date.isoformat(), 
                'end_date': employee.end_date.isoformat() if employee.end_date else None,
                'notes': employee.notes,  
                'created': employee.created.isoformat(),
                'updated': employee.updated.isoformat() if employee.updated else None
            }, 200
        return {'message': 'Employee not found'}, 404
    
class PatchEmployee(Resource):
    def patch(self, employee_id):
        employee = Employee.query.get(employee_id)
        if not employee:
            return {'message': 'Employee not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('department_id', type=int)
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('start_date', type=str)  
        parser.add_argument('end_date', type=str, store_missing=False)  
        parser.add_argument('notes', type=str, store_missing=False) 
        data = parser.parse_args()

        for key, value in data.items():
            setattr(employee, key, value)

        try:
            db.session.commit()
            return {'message': 'Employee updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to update employee. Error: {str(e)}'}, 500


class DeleteEmployee(Resource):
    def delete(self, employee_id):
        employee = Employee.query.get(employee_id)
        if not employee:
            return {'message': 'Employee not found'}, 404

        try:
            db.session.delete(employee)
            db.session.commit()
            return {'message': 'Employee deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to delete employee. Error: {str(e)}'}, 500
