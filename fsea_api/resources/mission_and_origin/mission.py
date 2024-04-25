from ..config import *
from ...models.sqlalchemy_models import Mission, EmployeeDesignation, Designation, Employee, Origin, EmployeeMission, DepartmentMission, MissionOrigin, Mission, Department
from ..employee.designation import DesignationType
from datetime import datetime


class MissionCustomOriginType(graphene.ObjectType):
    origin_id = graphene.String()
    origin_name = graphene.String()
class MissionCustomDepartmentType(graphene.ObjectType):
    department_id = graphene.Int()
    department_name = graphene.String()

class MissionCustomEmployeeType(graphene.ObjectType):
    employee_id = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    designations = graphene.List(lambda: DesignationType)

    def resolve_designations(self, info):
        designation_ids = [d[0] for d in (EmployeeDesignation.query
                           .filter_by(employee_id=self.employee_id)
                           .with_entities(EmployeeDesignation.designation_id)
                           .all())]
        designations = Designation.query.filter(Designation.designation_id.in_(designation_ids)).all()
        return designations
class MissionType(SQLAlchemyObjectType):
    class Meta:
        model = Mission
        interfaces = (graphene.relay.Node,)
        exclude_fields = ('commander_id', 'supervisor_id')
    
    commander = graphene.Field(MissionCustomEmployeeType)
    supervisor = graphene.Field(MissionCustomEmployeeType)
    employees = graphene.List(MissionCustomEmployeeType)
    departments = graphene.List(MissionCustomDepartmentType)
    origins = graphene.List(MissionCustomOriginType)
    
    def resolve_commander(self, info):
        commander = Employee.query.get(self.commander_id)
        if commander:
            return MissionCustomEmployeeType(
                employee_id=commander.employee_id,
                first_name=commander.first_name,
                last_name=commander.last_name
            )
        return None

    def resolve_supervisor(self, info):
        supervisor = Employee.query.get(self.supervisor_id)
        if supervisor:
            return MissionCustomEmployeeType(
                employee_id=supervisor.employee_id,
                first_name=supervisor.first_name,
                last_name=supervisor.last_name
            )
        return None

    def resolve_employees(self, info):
        employee_missions = EmployeeMission.query.filter_by(mission_id=self.mission_id).all()
        employees = [Employee.query.get(em.employee_id) for em in employee_missions]
        return [
            MissionCustomEmployeeType(
                employee_id=emp.employee_id,
                first_name=emp.first_name,
                last_name=emp.last_name
            ) for emp in employees if emp
        ]

    def resolve_departments(self, info):
        department_missions = DepartmentMission.query.filter_by(mission_id=self.mission_id).all()
        departments = [Department.query.get(dm.department_id) for dm in department_missions]
        return [
            MissionCustomDepartmentType(
                department_id=dept.department_id,
                department_name=dept.department_name
            ) for dept in departments if dept
        ]

    def resolve_origins(self, info):
        mission_origins = MissionOrigin.query.filter_by(mission_id=self.mission_id).all()
        origins = [Origin.query.get(mo.origin_id) for mo in mission_origins]
        return [
            MissionCustomOriginType(
                origin_id=origin.origin_id,
                origin_name=origin.origin_name
            ) for origin in origins if origin
        ]


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


