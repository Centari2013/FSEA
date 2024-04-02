from .imports import *
from ..models import ContainmentStatus  


class PostContainmentStatus(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('status_name', type=str, required=True, help="Status name cannot be blank.")
        parser.add_argument('description', type=str, required=True, help="Description cannot be blank.")
        data = parser.parse_args()
        new_status = ContainmentStatus(**data)
        try:
            db.session.add(new_status)
            db.session.commit()
            return {'status_id': new_status.containment_status_id}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return {'message': 'Failed to create new status. The server encountered an error.'}, 500


class GetContainmentStatus(Resource):
    def get(self, containment_status_id):
        status = ContainmentStatus.query.get(containment_status_id)
        if status:
            return {
                'containment_status_id': status.containment_status_id,
                'status_name': status.status_name,
                'description': status.description
            }, 200
        return {'message': 'Containment status not found'}, 404

class PatchContainmentStatus(Resource):
    def patch(self, containment_status_id):
        status = ContainmentStatus.query.get(containment_status_id)
        if not status:
            return {'message': 'Containment status not found'}, 404
        
        parser = reqparse.RequestParser()
        parser.add_argument('status_name', type=str, required=False, help="Optional: New status name.")
        parser.add_argument('description', type=str, required=False, help="Optional: New description.")
        data = parser.parse_args()

        if data['status_name']:
            status.status_name = data['status_name']
        if data['description']:
            status.description = data['description']

        try:
            db.session.commit()
            return {'message': 'Containment status updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return {'message': 'Failed to update containment status. The server encountered an error.'}, 500


class DeleteContainmentStatus(Resource):
    def delete(self, containment_status_id):
        status = ContainmentStatus.query.get(containment_status_id)
        if not status:
            return {'message': 'Containment status not found'}, 404

        try:
            db.session.delete(status)
            db.session.commit()
            return {'message': 'Containment status deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return {'message': 'Failed to delete containment status. The server encountered an error.'}, 500

