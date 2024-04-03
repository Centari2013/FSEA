from .imports import *
from ..models.sqlalchemy_models import Mission


class PostMission(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mission_id', type=str, required=True, help="Mission ID cannot be blank.")
        parser.add_argument('mission_name', type=str, required=False, default='NAME-PENDING', help="Optional: Mission name.")
        parser.add_argument('start_date', type=str, store_missing=False)  # Consider using a custom date type
        parser.add_argument('end_date', type=str, store_missing=False)  # Consider using a custom date type
        parser.add_argument('commander_id', type=str, store_missing=False)
        parser.add_argument('supervisor_id', type=str, store_missing=False)
        parser.add_argument('description', type=str, required=True, help="Description cannot be blank.")
        parser.add_argument('notes', type=str, store_missing=False)  # Optional, JSON string
        data = parser.parse_args()

        new_mission = Mission(**data)
        try:
            db.session.add(new_mission)
            db.session.commit()
            return {'mission_id': new_mission.mission_id}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to create new mission. Error: {str(e)}'}, 500



class GetMission(Resource):
    def get(self, mission_id):
        mission = Mission.query.get(mission_id)
        if mission:
            return {
                'mission_id': mission.mission_id,
                'mission_name': mission.mission_name,
                'start_date': mission.start_date.isoformat() if mission.start_date else None,
                'end_date': mission.end_date.isoformat() if mission.end_date else None,
                'commander_id': mission.commander_id,
                'supervisor_id': mission.supervisor_id,
                'description': mission.description,
                'notes': mission.notes,  # Assuming direct JSON storage and serialization
                'created': mission.created.isoformat(),
                'updated': mission.updated.isoformat() if mission.updated else None
            }, 200
        return {'message': 'Mission not found'}, 404


class PatchMission(Resource):
    def patch(self, mission_id):
        mission = Mission.query.get(mission_id)
        if not mission:
            return {'message': 'Mission not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('mission_name', type=str, store_missing=False)
        parser.add_argument('start_date', type=str, store_missing=False)  # Optional, consider using a custom date type
        parser.add_argument('end_date', type=str, store_missing=False)  # Optional
        parser.add_argument('commander_id', type=str, store_missing=False)
        parser.add_argument('supervisor_id', type=str, store_missing=False)
        parser.add_argument('description', type=str, store_missing=False)
        parser.add_argument('notes', type=str, store_missing=False)  # Optional, JSON string
        data = parser.parse_args()

        for key, value in data.items():
            setattr(mission, key, value)

        try:
            mission.updated = db.func.current_timestamp()  # Update the timestamp
            db.session.commit()
            return {'message': 'Mission updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to update mission. Error: {str(e)}'}, 500


class DeleteMission(Resource):
    def delete(self, mission_id):
        mission = Mission.query.get(mission_id)
        if not mission:
            return {'message': 'Mission not found'}, 404

        try:
            db.session.delete(mission)
            db.session.commit()
            return {'message': 'Mission deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to delete mission. Error: {str(e)}'}, 500


