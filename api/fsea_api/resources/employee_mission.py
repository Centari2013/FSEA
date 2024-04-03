from .imports import *
from ..models.sqlalchemy_models import EmployeeMission

class AddEmployeeToMission(Resource):
    def post(self, mission_id):
        parser = reqparse.RequestParser()
        parser.add_argument('employee_id', type=str, required=True, help="Employee ID cannot be blank.")
        parser.add_argument('involvement_summary', type=str, required=False, help="Optional: Involvement summary.")
        data = parser.parse_args()

        new_link = EmployeeMission(
            employee_id=data['employee_id'],
            mission_id=mission_id,
            involvement_summary=data.get('involvement_summary')
        )
        try:
            db.session.add(new_link)
            db.session.commit()
            return {'message': 'Employee added to mission successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to add employee to mission. Error: {str(e)}'}, 500


class GetMissionsByEmployee(Resource):
    def get(self, employee_id):
        links = EmployeeMission.query.filter_by(employee_id=employee_id).all()
        if links:
            missions = [{
                'mission_id': link.mission_id,
                'involvement_summary': link.involvement_summary
            } for link in links]
            return {'missions': missions}, 200
        else:
            return {'message': 'No missions found for this employee'}, 404

class GetEmployeesByMission(Resource):
    def get(self, mission_id):
        links = EmployeeMission.query.filter_by(mission_id=mission_id).all()
        if links:
            employees = [{
                'employee_id': link.employee_id,
                'involvement_summary': link.involvement_summary
            } for link in links]
            return {'employees': employees}, 200
        else:
            return {'message': 'No employees found for this mission'}, 404


class RemoveEmployeeFromMission(Resource):
    def delete(self, employee_id, mission_id):
        link = EmployeeMission.query.filter_by(employee_id=employee_id, mission_id=mission_id).first()
        if link:
            try:
                db.session.delete(link)
                db.session.commit()
                return {'message': 'Employee removed from mission successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback


