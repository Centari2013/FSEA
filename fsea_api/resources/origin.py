from .imports import *
from ..models.sqlalchemy_models import Origin

class PostOrigin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('origin_id', type=str, required=True, help="Origin ID cannot be blank.")
        parser.add_argument('origin_name', type=str, required=True, help="Origin name cannot be blank.")
        parser.add_argument('discovery_date', type=str, required=True, help="Discovery date cannot be blank.")  # Consider using a custom date type
        parser.add_argument('description', type=str, required=True, help="Description cannot be blank.")
        parser.add_argument('notes', type=str, store_missing=False)  # Optional, JSON string
        data = parser.parse_args()

        new_origin = Origin(**data)
        try:
            db.session.add(new_origin)
            db.session.commit()
            return {'origin_id': new_origin.origin_id}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to create new origin. Error: {str(e)}'}, 500


class GetOrigin(Resource):
    def get(self, origin_id):
        origin = Origin.query.get(origin_id)
        if origin:
            return {
                'origin_id': origin.origin_id,
                'origin_name': origin.origin_name,
                'discovery_date': origin.discovery_date.isoformat(),
                'description': origin.description,
                'notes': origin.notes,  # Assuming direct JSON storage and serialization
                'created': origin.created.isoformat(),
                'updated': origin.updated.isoformat() if origin.updated else None
            }, 200
        return {'message': 'Origin not found'}, 404


class PatchOrigin(Resource):
    def patch(self, origin_id):
        origin = Origin.query.get(origin_id)
        if not origin:
            return {'message': 'Origin not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('origin_name', type=str, store_missing=False)
        parser.add_argument('discovery_date', type=str, store_missing=False)  # Consider using a custom date type
        parser.add_argument('description', type=str, store_missing=False)
        parser.add_argument('notes', type=str, store_missing=False)  # Optional, JSON string
        data = parser.parse_args()

        for key, value in data.items():
            setattr(origin, key, value)

        try:
            origin.updated = db.func.current_timestamp()  # Update the timestamp
            db.session.commit()
            return {'message': 'Origin updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to update origin. Error: {str(e)}'}, 500


class DeleteOrigin(Resource):
    def delete(self, origin_id):
        origin = Origin.query.get(origin_id)
        if not origin:
            return {'message': 'Origin not found'}, 404

        try:
            db.session.delete(origin)
            db.session.commit()
            return {'message': 'Origin deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to delete origin. Error: {str(e)}'}, 500



