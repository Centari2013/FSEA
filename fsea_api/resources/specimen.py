from .imports import *
from ..models import Specimen

class PostSpecimen(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('specimen_id', type=str, required=True, help="Specimen ID cannot be blank.")
        parser.add_argument('specimen_name', type=str, required=True, help="Specimen name cannot be blank.")
        parser.add_argument('origin_id', type=str, store_missing=False)
        parser.add_argument('mission_id', type=str, store_missing=False)
        parser.add_argument('threat_level', type=float, required=True, help="Threat level must be between 0 and 10.", choices=range(11))
        parser.add_argument('acquisition_date', type=str, required=True, help="Acquisition date cannot be blank.")  # Consider using a custom date type
        parser.add_argument('notes', type=str, store_missing=False)  # Optional, JSON string
        parser.add_argument('description', type=str, store_missing=False)
        data = parser.parse_args()

        new_specimen = Specimen(**data)
        try:
            db.session.add(new_specimen)
            db.session.commit()
            return {'specimen_id': new_specimen.specimen_id}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to create new specimen. Error: {str(e)}'}, 500


class GetSpecimen(Resource):
    def get(self, specimen_id):
        specimen = Specimen.query.get(specimen_id)
        if specimen:
            return {
                'specimen_id': specimen.specimen_id,
                'specimen_name': specimen.specimen_name,
                'origin_id': specimen.origin_id,
                'mission_id': specimen.mission_id,
                'threat_level': specimen.threat_level,
                'acquisition_date': specimen.acquisition_date.isoformat(),
                'notes': specimen.notes,
                'description': specimen.description,
                'created': specimen.created.isoformat(),
                'updated': specimen.updated.isoformat() if specimen.updated else None
            }, 200
        return {'message': 'Specimen not found'}, 404


class PatchSpecimen(Resource):
    def patch(self, specimen_id):
        specimen = Specimen.query.get(specimen_id)
        if not specimen:
            return {'message': 'Specimen not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('specimen_name', type=str, store_missing=False)
        parser.add_argument('origin_id', type=str, store_missing=False)
        parser.add_argument('mission_id', type=str, store_missing=False)
        parser.add_argument('threat_level', type=float, store_missing=False, choices=[*(float(x) for x in range(11))])
        parser.add_argument('acquisition_date', type=str, store_missing=False)  # Consider using a custom date type
        parser.add_argument('notes', type=str, store_missing=False)  # Optional, JSON string
        parser.add_argument('description', type=str, store_missing=False)
        data = parser.parse_args()

        for key, value in data.items():
            setattr(specimen, key, value)

        try:
            specimen.updated = db.func.current_timestamp()  # Update the timestamp
            db.session.commit()
            return {'message': 'Specimen updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to update specimen. Error: {str(e)}'}, 500



class DeleteSpecimen(Resource):
    def delete(self, specimen_id):
        specimen = Specimen.query.get(specimen_id)
        if not specimen:
            return {'message': 'Specimen not found'}, 404

        try:
            db.session.delete(specimen)
            db.session.commit()
            return {'message': 'Specimen deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to delete specimen. Error: {str(e)}'}, 500

