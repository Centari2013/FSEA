from flask_restful import Resource, reqparse
from ..models import Clearance  
from .. import db  


class PostClearance(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('clearance_name', type=str, required=True, help="Clearance name cannot be blank.")
        parser.add_argument('description', type=str, required=True, help="Description cannot be blank.")
        data = parser.parse_args()
        new_clearance = Clearance(**data)
        db.session.add(new_clearance)
        db.session.commit()
        return {'clearance_id': new_clearance.clearance_id}, 201

class GetClearance(Resource):
    def get(self, clearance_id):
        clearance = Clearance.query.get(clearance_id)
        if clearance:
            return {
                'clearance_id': clearance.clearance_id,
                'clearance_name': clearance.clearance_name,
                'description': clearance.description
            }, 200
        return {'message': 'Clearance not found'}, 404

class PatchClearance(Resource):
    def patch(self, clearance_id):
        clearance = Clearance.query.get(clearance_id)
        if not clearance:
            return {'message': 'Clearance not found'}, 404
        
        parser = reqparse.RequestParser()
        parser.add_argument('clearance_name', type=str, required=False, help="Optional: New clearance name.")
        parser.add_argument('description', type=str, required=False, help="Optional: New description.")
        data = parser.parse_args()

        if data['clearance_name']:
            clearance.clearance_name = data['clearance_name']
        if data['description']:
            clearance.description = data['description']

        db.session.commit()
        return {'message': 'Clearance updated successfully'}, 200

class DeleteClearance(Resource):
    def delete(self, clearance_id):
        clearance = Clearance.query.get(clearance_id)
        if not clearance:
            return {'message': 'Clearance not found'}, 404

        db.session.delete(clearance)
        db.session.commit()
        return {'message': 'Clearance deleted successfully'}, 200
