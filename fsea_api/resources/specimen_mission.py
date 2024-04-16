from .config import *
from ..models.sqlalchemy_models import SpecimenMission

class SpecimenMissionType(SQLAlchemyObjectType):
    class Meta:
        model = SpecimenMission
        interfaces = (graphene.relay.Node,)

class AddSpecimenToMission(graphene.Mutation):
    class Arguments:
        specimen_id = graphene.Int(required=True)
        mission_id = graphene.Int(required=True)
        involvement_summary = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, specimen_id, mission_id, involvement_summary):
        new_link = SpecimenMission(specimen_id=specimen_id, mission_id=mission_id, involvement_summary=involvement_summary)
        try:
            db.session.add(new_link)
            db.session.commit()
            return AddSpecimenToMission(success=True, message="Specimen associated with mission successfully")
        except Exception as e:
            db.session.rollback()
            return AddSpecimenToMission(success=False, message=f"Failed to add specimen to mission. Error: {str(e)}")

class RemoveSpecimenFromMission(graphene.Mutation):
    class Arguments:
        specimen_id = graphene.Int(required=True)
        mission_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, specimen_id, mission_id):
        link = SpecimenMission.query.filter_by(specimen_id=specimen_id, mission_id=mission_id).first()
        if link:
            try:
                db.session.delete(link)
                db.session.commit()
                return RemoveSpecimenFromMission(success=True, message="Specimen disassociated from mission successfully")
            except Exception as e:
                db.session.rollback()
                return RemoveSpecimenFromMission(success=False, message=f"Failed to remove specimen from mission. Error: {str(e)}")
        else:
            return RemoveSpecimenFromMission(success=False, message="Specimen-mission association not found")

class SpecimenMissionQuery(graphene.ObjectType):
    missions_for_specimen = graphene.List(
        SpecimenMissionType, 
        specimen_id=graphene.Int(required=True), 
        resolver=lambda self, info, specimen_id: SpecimenMission.query.filter_by(specimen_id=specimen_id).all()
    )

    specimens_for_mission = graphene.List(
        SpecimenMissionType, 
        mission_id=graphene.Int(required=True), 
        resolver=lambda self, info, mission_id: SpecimenMission.query.filter_by(mission_id=mission_id).all()
    )

class SpecimenMissionMutation(graphene.ObjectType):
    add_specimen_to_mission = AddSpecimenToMission.Field()
    remove_specimen_from_mission = RemoveSpecimenFromMission.Field()


