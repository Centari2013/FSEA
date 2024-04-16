from .config import *
from ..models.sqlalchemy_models import MissionOrigin

class MissionOriginType(SQLAlchemyObjectType):
    class Meta:
        model = MissionOrigin
        interfaces = (graphene.relay.Node,)

class AssociateOriginWithMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.String(required=True)
        origin_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, mission_id, origin_id):
        association = MissionOrigin(mission_id=mission_id, origin_id=origin_id)
        try:
            db.session.add(association)
            db.session.commit()
            return AssociateOriginWithMission(success=True, message="Origin associated with mission successfully")
        except Exception as e:
            db.session.rollback()
            return AssociateOriginWithMission(success=False, message=f"Failed to associate origin with mission. Error: {str(e)}")

class DisassociateOriginFromMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.String(required=True)
        origin_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, mission_id, origin_id):
        association = MissionOrigin.query.filter_by(mission_id=mission_id, origin_id=origin_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return DisassociateOriginFromMission(success=True, message="Origin disassociated from mission successfully")
            except Exception as e:
                db.session.rollback()
                return DisassociateOriginFromMission(success=False, message=f"Failed to disassociate origin from mission. Error: {str(e)}")
        else:
            return DisassociateOriginFromMission(success=False, message="Association not found")

class MissionOriginQuery(graphene.ObjectType):
    origins_for_mission = graphene.List(graphene.String, mission_id=graphene.String(required=True))
    missions_for_origin = graphene.List(graphene.String, origin_id=graphene.String(required=True))

    def resolve_origins_for_mission(self, info, mission_id):
        associations = MissionOrigin.query.filter_by(mission_id=mission_id).all()
        return [assoc.origin_id for assoc in associations]

    def resolve_missions_for_origin(self, info, origin_id):
        associations = MissionOrigin.query.filter_by(origin_id=origin_id).all()
        return [assoc.mission_id for assoc in associations]

class MissionOriginMutation(graphene.ObjectType):
    associate_origin_with_mission = AssociateOriginWithMission.Field()
    disassociate_origin_from_mission = DisassociateOriginFromMission.Field()


