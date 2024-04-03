from .imports import *
from ..models.sqlalchemy_models import MissionOrigin

class AssociateOriginWithMission(Resource):
    def post(self, mission_id):
        parser = reqparse.RequestParser()
        parser.add_argument('origin_id', type=str, required=True, help="Origin ID cannot be blank.")
        data = parser.parse_args()

        association = MissionOrigin(mission_id=mission_id, origin_id=data['origin_id'])
        try:
            db.session.add(association)
            db.session.commit()
            return {'message': 'Origin associated with mission successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to associate origin with mission. Error: {str(e)}'}, 500


class DisassociateOriginFromMission(Resource):
    def delete(self, mission_id, origin_id):
        association = MissionOrigin.query.filter_by(mission_id=mission_id, origin_id=origin_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return {'message': 'Origin disassociated from mission successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'message': f'Failed to disassociate origin from mission. Error: {str(e)}'}, 500
        else:
            return {'message': 'Association not found'}, 404


class GetOriginsForMission(Resource):
    def get(self, mission_id):
        associations = MissionOrigin.query.filter_by(mission_id=mission_id).all()
        if associations:
            origins = [{'origin_id': assoc.origin_id} for assoc in associations]
            return {'origins': origins}, 200
        else:
            return {'message': 'No origins found for this mission'}, 404


class GetMissionsForOrigin(Resource):
    def get(self, origin_id):
        associations = MissionOrigin.query.filter_by(origin_id=origin_id).all()
        if associations:
            missions = [{'mission_id': assoc.mission_id} for assoc in associations]
            return {'missions': missions}, 200
        else:
            return {'message': 'No missions found for this origin'}, 404
