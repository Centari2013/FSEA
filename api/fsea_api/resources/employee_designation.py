from .imports import *
from ..models import EmployeeDesignation

class AssociateDesignationWithEmployee(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('employee_id', type=str, required=True, help="Employee ID cannot be blank.")
        parser.add_argument('designation_id', type=int, required=True, help="Designation ID cannot be blank.")
        data = parser.parse_args()

        new_association = EmployeeDesignation(**data)
        try:
            db.session.add(new_association)
            db.session.commit()
            return {'message': 'Designation associated with employee successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to associate designation with employee. Error: {str(e)}'}, 500


class DisassociateDesignationFromEmployee(Resource):
    def delete(self, employee_id, designation_id):
        association = EmployeeDesignation.query.filter_by(employee_id=employee_id, designation_id=designation_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return {'message': 'Designation disassociated from employee successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'message': f'Failed to disassociate designation from employee. Error: {str(e)}'}, 500
        else:
            return {'message': 'Association not found'}, 404


class GetEmployeeDesignations(Resource):
    def get(self, employee_id):
        designations = EmployeeDesignation.query.filter_by(employee_id=employee_id).all()
        if designations:
            return {'designations': [{'designation_id': designation.designation_id} for designation in designations]}, 200
        else:
            return {'message': 'No designations found for the given employee'}, 404


