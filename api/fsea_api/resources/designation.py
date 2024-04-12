from .imports import *
from ..models.sqlalchemy_models import Designation 


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


class GetDesignationsList(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('ids', action='split', location='args')  # 'split' will split the comma-separated string into a list
            args = parser.parse_args()
            
            if type(args['ids']) is not list:
                designation_ids = [args['ids']]
            if not designation_ids:
                return {'message': 'No designation IDs provided'}, 400
            
        
            # Assuming designation_ids is a list of strings, converting them to integers
            designation_ids = [int(id) for id in designation_ids]
            
            # Querying for multiple IDs using SQLAlchemy .filter() and .in_()
            designations = Designation.query.filter(Designation.designation_id.in_(designation_ids)).all()
            
            if designations:
                designation_list = [
                    {
                        'designation_id': designation.designation_id,
                        'designation_name': designation.designation_name,
                        'abbreviation': designation.abbreviation
                    } for designation in designations
                ]

                return {"designations": designation_list}, 200

            else:
                return {'message': 'Designations not found'}, 404
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {'message': 'Internal server error. Please try again later.'}, 404


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

