from .imports import *
from ..models.sqlalchemy_models import Designation 


DesignationModel = api.model('Designation', {
    'designation_id': fields.Integer(description='Designation unique identifier'),
    'designation_name': fields.String(required=True, description='Name of the designation'),
    'abbreviation': fields.String(required=True, description='Abbreviation of the designation')
})

class PostDesignation(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('designation_name', type=str, required=True, help="Designation name cannot be blank.")
        parser.add_argument('abbreviation', type=str, required=True, help="Abbreviation cannot be blank.")
        data = parser.parse_args()
        new_designation = Designation(**data)

        try:
            db.session.add(new_designation)
            db.session.commit()
            return {'designation_id': new_designation.designation_id}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return {'message': 'Failed to create new designation. The server encountered an error.'}, 500


class GetDesignation(Resource):
    def get(self, designation_id):
        designation = Designation.query.get(designation_id)
        if designation:
            return {
                'designation_id': designation.designation_id,
                'designation_name': designation.designation_name,
                'abbreviation': designation.abbreviation
            }, 200
        return {'message': 'Designation not found'}, 404

class PatchDesignation(Resource):
    def patch(self, designation_id):
        designation = Designation.query.get(designation_id)
        if not designation:
            return {'message': 'Designation not found'}, 404
        
        parser = reqparse.RequestParser()
        parser.add_argument('designation_name', type=str, required=False, help="Optional: New designation name.")
        parser.add_argument('abbreviation', type=str, required=False, help="Optional: New abbreviation.")
     
        data = parser.parse_args()

        if data['designation_name']:
            designation.designation_name = data['designation_name']
        if data['abbreviation']:
            designation.abbreviation = data['abbreviation']
        try:
            db.session.commit()
            return {'message': 'Designation updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return {'message': 'Failed to update designation. The server encountered an error.'}, 500
        

class DeleteDesignation(Resource):
    def delete(self, designation_id):
        designation = Designation.query.get(designation_id)
        if not designation:
            return {'message': 'Designation not found'}, 404

        try:
            db.session.delete(designation)
            db.session.commit()
            return {'message': 'Designation deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return {'message': 'Failed to delete designation. The server encountered an error.'}, 500

