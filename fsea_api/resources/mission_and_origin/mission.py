from ..config import *
from ...models.sqlalchemy_models import Mission
from datetime import datetime

class MissionType(SQLAlchemyObjectType):
    class Meta:
        model = Mission
        interfaces = (graphene.relay.Node,)

class CreateMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.String(required=True)
        mission_name = graphene.String(default_value="NAME-PENDING")
        start_date = graphene.Date()
        end_date = graphene.Date()
        commander_id = graphene.String()
        supervisor_id = graphene.String()
        description = graphene.String(required=True)
        notes = graphene.String()

    mission = graphene.Field(MissionType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, mission_id, description, mission_name=None, start_date=None, end_date=None, commander_id=None, supervisor_id=None, notes=None):
        new_mission = Mission(
            mission_id=mission_id,
            mission_name=mission_name,
            start_date=start_date,
            end_date=end_date,
            commander_id=commander_id,
            supervisor_id=supervisor_id,
            description=description,
            notes=notes
        )
        try:
            db.session.add(new_mission)
            db.session.commit()
            return CreateMission(mission=new_mission, success=True, message="New mission created successfully")
        except Exception as e:
            db.session.rollback()
            return CreateMission(success=False, message=f"Failed to create new mission. Error: {str(e)}")

class UpdateMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.String(required=True)
        mission_name = graphene.String()
        start_date = graphene.Date()
        end_date = graphene.Date()
        commander_id = graphene.String()
        supervisor_id = graphene.String()
        description = graphene.String()
        notes = graphene.String()

    mission = graphene.Field(MissionType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, mission_id, mission_name=None, start_date=None, end_date=None, commander_id=None, supervisor_id=None, description=None, notes=None):
        mission = Mission.query.get(mission_id)
        if not mission:
            return UpdateMission(success=False, message="Mission not found")

        mission.mission_name = mission_name if mission_name is not None else mission.mission_name
        mission.start_date = start_date if start_date is not None else mission.start_date
        mission.end_date = end_date if end_date is not None else mission.end_date
        mission.commander_id = commander_id if commander_id is not None else mission.commander_id
        mission.supervisor_id = supervisor_id if supervisor_id is not None else mission.supervisor_id
        mission.description = description if description is not None else mission.description
        mission.notes = notes if notes is not None else mission.notes

        try:
            mission.updated = datetime.utcnow()
            db.session.commit()
            return UpdateMission(mission=mission, success=True, message="Mission updated successfully")
        except Exception as e:
            db.session.rollback()
            return UpdateMission(success=False, message=f"Failed to update mission. Error: {str(e)}")

class DeleteMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, mission_id):
        mission = Mission.query.get(mission_id)
        if not mission:
            return DeleteMission(success=False, message="Mission not found")

        try:
            db.session.delete(mission)
            db.session.commit()
            return DeleteMission(success=True, message="Mission deleted successfully")
        except Exception as e:
            db.session.rollback()
            return DeleteMission(success=False, message=f"Failed to delete mission. Error: {str(e)}")

class MissionQuery(graphene.ObjectType):
    missions = graphene.List(MissionType, mission_ids=graphene.List(graphene.String, required=True))
    all_missions = graphene.List(MissionType)

    def resolve_missions(self, info, mission_ids):
        return Mission.query.filter(Mission.mission_id.in_(mission_ids)).all()

    def resolve_all_missions(self, info):
        return Mission.query.all()

class MissionMutation(graphene.ObjectType):
    create_mission = CreateMission.Field()
    update_mission = UpdateMission.Field()
    delete_mission = DeleteMission.Field()


