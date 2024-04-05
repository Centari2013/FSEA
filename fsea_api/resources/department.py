from .imports import *
from ..models.sqlalchemy_models import Department 





class PostDepartment(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('department_name', type=str, required=True, help="Department name cannot be blank.")
        parser.add_argument('description', type=str, help="Optional: Description.")
        parser.add_argument('director_id', type=str, help="Optional: Director Id.")
        data = parser.parse_args()
        new_department = Department(**data)
        try:
            db.session.add(new_department)
            db.session.commit()
            return {'department_id': new_department.department_id}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return {'message': 'Failed to create new department. The server encountered an error.'}, 500


class GetDepartment(Resource):
    def get(self, department_id):
        department = Department.query.get(department_id)
        if department:
            return {
                'department_id': department.department_id,
                'department_name': department.department_name,
                'director_id': department.director_id,
                'description': department.description
            }, 200
        return {'message': 'Department not found'}, 404
    
class GetAllDepartments(Resource):
    def get(self):
        departments = Department.query.all()
        if departments:
            return [{
                'department_id': department.department_id,
                'department_name': department.department_name,
                'director_id': department.director_id,
                'description': department.description
            } for department in departments], 200
        return {'message': 'Departments not found'}, 404

class PatchDepartment(Resource):
    def patch(self, department_id):
        department = Department.query.get(department_id)
        if not department:
            return {'message': 'Department not found'}, 404
        
        parser = reqparse.RequestParser()
        parser.add_argument('department_name', type=str, required=False, help="Optional: New department name.")
        parser.add_argument('description', type=str, required=False, help="Optional: New description.")
        parser.add_argument('director_id', type=str, help="Optional: Director Id.")
        data = parser.parse_args()

        if data['department_name']:
            department.department_name = data['department_name']
        if data['description']:
            department.description = data['description']
        if data['director_id']:
            department.director_id = data['director_id']

        try:
            db.session.commit()
            return {'message': 'Department updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return {'message': 'Failed to update department. The server encountered an error.'}, 500


class DeleteDepartment(Resource):
    def delete(self, department_id):
        department = Department.query.get(department_id)
        if not department:
            return {'message': 'Department not found'}, 404

        try:
            db.session.delete(department)
            db.session.commit()
            return {'message': 'Department deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return {'message': 'Failed to delete department. The server encountered an error.'}, 500

