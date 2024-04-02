from .imports import *
from ..models import SpecimenMission

class AddSpecimenMission(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('specimen_id', type=str, required=True, help="Specimen ID cannot be blank.")
        parser.add_argument('mission_id', type=str, required=True, help="Mission ID cannot be blank.")
        parser.add_argument('involvement_summary', type=str, required=True, help="Involvement summary cannot be blank.")
        data = parser.parse_args()

        new_link = SpecimenMission(**data)
        try:
            db.session.add(new_link)
            db.session.commit()
            return {'message': 'Specimen associated with mission successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to add specimen to mission. Error: {str(e)}'}, 500


class DeleteSpecimenMission(Resource):
    def delete(self, specimen_id, mission_id):
        link = SpecimenMission.query.filter_by(specimen_id=specimen_id, mission_id=mission_id).first()
        if link:
            try:
                db.session.delete(link)
                db.session.commit()
                return {'message': 'Specimen disassociated from mission successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'message': f'Failed to remove specimen from mission. Error: {str(e)}'}, 500
        else:
            return {'message': 'Specimen-mission association not found'}, 404


class GetMissionsForSpecimen(Resource):
    def get(self, specimen_id):
        links = SpecimenMission.query.filter_by(specimen_id=specimen_id).all()
        if links:
            missions = [{'mission_id': link.mission_id, 'involvement_summary': link.involvement_summary} for link in links]
            return {'missions': missions}, 200
        else:
            return {'message': 'No missions found for this specimen'}, 404


class GetSpecimensForMission(Resource):
    def get(self, mission_id):
        links = SpecimenMission.query.filter_by(mission_id=mission_id).all()
        if links:
            specimens = [{'specimen_id': link.specimen_id, 'involvement_summary': link.involvement_summary} for link in links]
            return {'specimens': specimens}, 200
        else:
            return {'message': 'No specimens found for this mission'}, 404
