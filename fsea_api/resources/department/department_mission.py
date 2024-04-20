from ..config import *
from ...models.sqlalchemy_models import DepartmentMission

class DepartmentMissionType(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentMission
        interfaces = (graphene.relay.Node,)

class AssociateMissionWithDepartment(graphene.Mutation):
    class Arguments:
        department_id = graphene.Int(required=True)
        mission_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, department_id, mission_id):
        new_association = DepartmentMission(department_id=department_id, mission_id=mission_id)
        try:
            db.session.add(new_association)
            db.session.commit()
            return AssociateMissionWithDepartment(success=True, message="Mission associated with department successfully")
        except Exception as e:
            db.session.rollback()
            return AssociateMissionWithDepartment(success=False, message=f"Failed to associate mission with department. Error: {str(e)}")

class DisassociateMissionFromDepartment(graphene.Mutation):
    class Arguments:
        department_id = graphene.Int(required=True)
        mission_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, department_id, mission_id):
        association = DepartmentMission.query.filter_by(department_id=department_id, mission_id=mission_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return DisassociateMissionFromDepartment(success=True, message="Mission disassociated from department successfully")
            except Exception as e:
                db.session.rollback()
                return DisassociateMissionFromDepartment(success=False, message=f"Failed to disassociate mission from department. Error: {str(e)}")
        else:
            return DisassociateMissionFromDepartment(success=False, message="Department-mission association not found")

class GetMissionsForDepartment(graphene.ObjectType):
    class Arguments:
        department_id = graphene.Int(required=True)

    missions = graphene.List(graphene.String)

    def resolve_missions(self, info, department_id):
        associations = DepartmentMission.query.filter_by(department_id=department_id).all()
        if associations:
            return [assoc.mission_id for assoc in associations]
        else:
            return None

class GetDepartmentsForMission(graphene.ObjectType):
    class Arguments:
        mission_id = graphene.Int(required=True)

    departments = graphene.List(graphene.String)

    def resolve_departments(self, info, mission_id):
        associations = DepartmentMission.query.filter_by(mission_id=mission_id).all()
        if associations:
            return [assoc.department_id for assoc in associations]
        else:
            return None

class DepartmentMissionMutation(graphene.ObjectType):
    associate_mission_with_department = AssociateMissionWithDepartment.Field()
    disassociate_mission_from_department = DisassociateMissionFromDepartment.Field()

class DepartmentMissionQuery(graphene.ObjectType):
    get_missions_for_department = graphene.Field(GetMissionsForDepartment, department_id=graphene.Int(required=True))
    get_departments_for_mission = graphene.Field(GetDepartmentsForMission, mission_id=graphene.Int(required=True))


