from .config import *
from ..models.sqlalchemy_models import EmployeeMission

class EmployeeMissionType(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeMission
        interfaces = (graphene.relay.Node,)

class AddEmployeeToMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.String(required=True)
        employee_id = graphene.String(required=True)
        involvement_summary = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, mission_id, employee_id, involvement_summary=None):
        new_link = EmployeeMission(
            employee_id=employee_id,
            mission_id=mission_id,
            involvement_summary=involvement_summary
        )
        try:
            db.session.add(new_link)
            db.session.commit()
            return AddEmployeeToMission(success=True, message="Employee added to mission successfully")
        except Exception as e:
            db.session.rollback()
            return AddEmployeeToMission(success=False, message=f"Failed to add employee to mission. Error: {str(e)}")

class RemoveEmployeeFromMission(graphene.Mutation):
    class Arguments:
        mission_id = graphene.String(required=True)
        employee_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, mission_id, employee_id):
        link = EmployeeMission.query.filter_by(employee_id=employee_id, mission_id=mission_id).first()
        if link:
            try:
                db.session.delete(link)
                db.session.commit()
                return RemoveEmployeeFromMission(success=True, message="Employee removed from mission successfully")
            except Exception as e:
                db.session.rollback()
                return RemoveEmployeeFromMission(success=False, message=f"Failed to remove employee from mission. Error: {str(e)}")
        else:
            return RemoveEmployeeFromMission(success=False, message="Association not found")

class EmployeeMissionQuery(graphene.ObjectType):
    missions_by_employee = graphene.List(
        EmployeeMissionType,
        employee_id=graphene.String(required=True)
    )
    employees_by_mission = graphene.List(
        EmployeeMissionType,
        mission_id=graphene.String(required=True)
    )

    def resolve_missions_by_employee(self, info, employee_id):
        return EmployeeMission.query.filter_by(employee_id=employee_id).all()

    def resolve_employees_by_mission(self, info, mission_id):
        return EmployeeMission.query.filter_by(mission_id=mission_id).all()

class EmployeeMissionMutation(graphene.ObjectType):
    add_employee_to_mission = AddEmployeeToMission.Field()
    remove_employee_from_mission = RemoveEmployeeFromMission.Field()


