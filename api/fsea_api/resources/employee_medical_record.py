from .imports import *
from ..models.sqlalchemy_models import EmployeeMedicalRecord


EmployeeMedicalRecordModel = api.model('EmployeeMedicalRecord', {
    'employee_id': fields.String(description='Employee unique identifier'),
    'dob': fields.Date(required=True, description='Date of birth'),
    'bloodtype': fields.String(description='Blood type', nullable=True),
    'sex': fields.String(description='Sex', nullable=True),
    'kilograms': fields.Float(description='Weight in kilograms', nullable=True),
    'height_cm': fields.Float(description='Height in centimeters', nullable=True),
    'notes': fields.Raw(description='JSONB field for additional notes', nullable=True)
})


class GetEmployeeMedicalRecord(Resource):
    def get(self, employee_id):
        medical_record = EmployeeMedicalRecord.query.get(employee_id)
        if medical_record:
            return {
                'employee_id': medical_record.employee_id,
                'dob': medical_record.dob.isoformat(),
                'bloodtype': medical_record.bloodtype,
                'sex': medical_record.sex,
                'kilograms': medical_record.kilograms,
                'height_cm': medical_record.height_cm,
                'notes': medical_record.notes, 
                'created': medical_record.created.isoformat(),
                'updated': medical_record.updated.isoformat() if medical_record.updated else None
            }, 200
        return {'message': 'Medical record not found'}, 404

class PatchEmployeeMedicalRecord(Resource):
    def patch(self, employee_id):
        medical_record = EmployeeMedicalRecord.query.get(employee_id)
        if not medical_record:
            return {'message': 'Medical record not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('dob', type=str, store_missing=False) 
        parser.add_argument('bloodtype', type=str, store_missing=False, choices=('A+', 'O+', 'B+', 'AB+', 'A-', 'O-', 'B-', 'AB-', 'V-', 'V+', 'BF', 'undefined'))
        parser.add_argument('sex', type=str, store_missing=False, choices=('m', 'f', 'inter', 'unknown', 'undefined'))
        parser.add_argument('kilograms', type=float, store_missing=False)
        parser.add_argument('height_cm', type=float, store_missing=False)
        parser.add_argument('notes', type=str, store_missing=False) 
        data = parser.parse_args()

        for key, value in data.items():
            setattr(medical_record, key, value)

        try:
            medical_record.updated = db.func.current_timestamp()
            db.session.commit()
            return {'message': 'Medical record updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to update medical record. Error: {str(e)}'}, 500

class DeleteEmployeeMedicalRecord(Resource):
    def delete(self, employee_id):
        medical_record = EmployeeMedicalRecord.query.get(employee_id)
        if not medical_record:
            return {'message': 'Medical record not found'}, 404

        try:
            db.session.delete(medical_record)
            db.session.commit()
            return {'message': 'Medical record deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to delete medical record. Error: {str(e)}'}, 500





