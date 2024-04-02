from .imports import *
from ..models import SpecimenMedicalRecord

class GetSpecimenMedicalRecord(Resource):
    def get(self, specimen_id):
        medical_record = SpecimenMedicalRecord.query.get(specimen_id)
        if medical_record:
            return {
                'specimen_id': medical_record.specimen_id,
                'bloodtype': medical_record.bloodtype,
                'sex': medical_record.sex,
                'kilograms': medical_record.kilograms,
                'notes': medical_record.notes,
                'created': medical_record.created.isoformat(),
                'updated': medical_record.updated.isoformat() if medical_record.updated else None
            }, 200
        return {'message': 'Specimen medical record not found'}, 404

class PatchSpecimenMedicalRecord(Resource):
    def patch(self, specimen_id):
        medical_record = SpecimenMedicalRecord.query.get(specimen_id)
        if not medical_record:
            return {'message': 'Specimen medical record not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('bloodtype', type=str, store_missing=False)
        parser.add_argument('sex', type=str, store_missing=False)
        parser.add_argument('kilograms', type=float, store_missing=False)
        parser.add_argument('notes', type=str, store_missing=False)  # Optional, JSON string
        data = parser.parse_args()

        for key, value in data.items():
            setattr(medical_record, key, value)

        try:
            medical_record.updated = db.func.current_timestamp()  # Update the timestamp
            db.session.commit()
            return {'message': 'Specimen medical record updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to update specimen medical record. Error: {str(e)}'}, 500

class DeleteSpecimenMedicalRecord(Resource):
    def delete(self, specimen_id):
        medical_record = SpecimenMedicalRecord.query.get(specimen_id)
        if not medical_record:
            return {'message': 'Specimen medical record not found'}, 404

        try:
            db.session.delete(medical_record)
            db.session.commit()
            return {'message': 'Specimen medical record deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to delete specimen medical record. Error: {str(e)}'}, 500
