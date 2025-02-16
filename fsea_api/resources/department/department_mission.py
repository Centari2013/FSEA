from ..config import *
from ...models.sqlalchemy_models import DepartmentMission

@mapper.type(DepartmentMission)
class DepartmentMissionType:
    pass

def associate_mission_with_department(info: strawberry.Info, department_id, mission_id):
    with SessionLocal() as session:
        new_association = DepartmentMission(department_id=department_id, mission_id=mission_id)
        try:
            session.add(new_association)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False

def disassociate_mission_from_department(info: strawberry.Info, department_id, mission_id):
    with SessionLocal() as session:
        association = session.query(DepartmentMission).filter_by(department_id=department_id, mission_id=mission_id).first()
        if association:
            try:
                session.delete(association)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                return False
        else:
            return False

def get_missions_for_department(info: strawberry.Info, department_id):
    with SessionLocal() as session:
        associations = session.query(DepartmentMission).filter_by(department_id=department_id).all()
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


