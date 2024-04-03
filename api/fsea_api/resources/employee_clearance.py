from .imports import *
from ..models.sqlalchemy_models import EmployeeClearance



class AssociateClearanceWithEmployee(Resource):
    def post(self, employee_id):
        parser = reqparse.RequestParser()
        parser.add_argument('clearance_id', type=int, required=True, help="Clearance ID cannot be blank.")
        data = parser.parse_args()

        # Assuming a model EmployeeClearance exists that represents this relationship
        new_association = EmployeeClearance(employee_id=employee_id, clearance_id=data['clearance_id'])
        try:
            db.session.add(new_association)
            db.session.commit()
            return {'message': 'Clearance associated with employee successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to associate clearance with employee. Error: {str(e)}'}, 500


class DisassociateClearanceFromEmployee(Resource):
    def delete(self, employee_id, clearance_id):
        association = EmployeeClearance.query.filter_by(employee_id=employee_id, clearance_id=clearance_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return {'message': 'Clearance disassociated from employee successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'message': f'Failed to disassociate clearance from employee. Error: {str(e)}'}, 500
        else:
            return {'message': 'Association not found'}, 404


class GetEmployeeClearances(Resource):
    def get(self, employee_id):
        clearances = EmployeeClearance.query.filter_by(employee_id=employee_id).all()
        if clearances:
            return {'clearances': [{'clearance_id': clearance.clearance_id} for clearance in clearances]}, 200
        else:
            return {'message': 'No clearances found for the given employee'}, 404
