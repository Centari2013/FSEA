from .imports import *
from ..models.sqlalchemy_models import DepartmentMission

DepartmentMissionModel = api.model('DepartmentMission', {
    'department_id': fields.Integer(required=True, description='Department unique identifier'),
    'mission_id': fields.String(required=True, description='Mission unique identifier')
})

class AssociateMissionWithDepartment(Resource):
    def post(self, department_id):
        parser = reqparse.RequestParser()
        parser.add_argument('mission_id', type=str, required=True, help="Mission ID cannot be blank.")
        data = parser.parse_args()

        new_association = DepartmentMission(department_id=department_id, mission_id=data['mission_id'])
        try:
            db.session.add(new_association)
            db.session.commit()
            return {'message': 'Mission associated with department successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to associate mission with department. Error: {str(e)}'}, 500


class DisassociateMissionFromDepartment(Resource):
    def delete(self, department_id, mission_id):
        association = DepartmentMission.query.filter_by(department_id=department_id, mission_id=mission_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return {'message': 'Mission disassociated from department successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'message': f'Failed to disassociate mission from department. Error: {str(e)}'}, 500
        else:
            return {'message': 'Department-mission association not found'}, 404


class GetMissionsForDepartment(Resource):
    def get(self, department_id):
        associations = DepartmentMission.query.filter_by(department_id=department_id).all()
        if associations:
            missions = [{'mission_id': assoc.mission_id} for assoc in associations]
            return {'missions': missions}, 200
        else:
            return {'message': 'No missions found for this department'}, 404


class GetDepartmentsForMission(Resource):
    def get(self, mission_id):
        associations = DepartmentMission.query.filter_by(mission_id=mission_id).all()
        if associations:
            departments = [{'department_id': assoc.department_id} for assoc in associations]
            return {'departments': departments}, 200
        else:
            return {'message': 'No departments found for this mission'}, 404
