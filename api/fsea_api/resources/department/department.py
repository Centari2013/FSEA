from ..config import *
from ...models.sqlalchemy_models import Department, Employee, DepartmentMission, EmployeeDesignation, Designation
from ..employee.designation import DesignationType

class CustomEmployeeType(graphene.ObjectType):
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

class CustomDepartmentMissionType(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentMission
        interfaces = (graphene.relay.Node,)
        exclude_fields = ('department_id')
    mission_name = graphene.String()

    def resolve_mission_name(self, info):
        # Utilize the relationship to get the mission name
        return self.mission.mission_name if self.mission else None

class DepartmentType(SQLAlchemyObjectType):
    class Meta:
        model = Department
        interfaces = (graphene.relay.Node,)
        exclude_fields = ('director_id')
    
    director = graphene.Field(lambda: CustomEmployeeType)
    missions = graphene.List(CustomDepartmentMissionType)
    employees = graphene.List(CustomEmployeeType)


    def resolve_director(self, info):
        # Assuming Employee is imported from your SQLAlchemy model definitions
        employee = Employee.query.get(self.director_id)
        
        return CustomEmployeeType(
            employee_id=employee.employee_id,
            first_name=employee.first_name,
            last_name=employee.last_name
        )
       
    def resolve_missions(self, info):
        return DepartmentMission.query.filter(DepartmentMission.department_id == self.department_id).all()
    
    def resolve_employees(self, info):
        employees = Employee.query.filter(Employee.department_id == self.department_id).all()
        
        return [
            CustomEmployeeType(
                employee_id=emp.employee_id,
                first_name=emp.first_name,
                last_name=emp.last_name
            ) for emp in employees
        ]
    

class CreateDepartment(graphene.Mutation):
    class Arguments:
        department_name = graphene.String(required=True)
        description = graphene.String()
        director_id = graphene.Int()

    department = graphene.Field(lambda: DepartmentType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, department_name, description=None, director_id=None):
        new_department = Department(department_name=department_name, description=description, director_id=director_id)
        try:
            db.session.add(new_department)
            db.session.commit()
            return CreateDepartment(department=new_department, success=True, message="Department created successfully")
        except Exception as e:
            db.session.rollback()
            return CreateDepartment(success=False, message="Failed to create new department. Error: " + str(e))

class UpdateDepartment(graphene.Mutation):
    class Arguments:
        department_id = graphene.Int(required=True)
        department_name = graphene.String()
        description = graphene.String()
        director_id = graphene.Int()

    department = graphene.Field(lambda: DepartmentType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, department_id, department_name=None, description=None, director_id=None):
        department = Department.query.get(department_id)
        if not department:
            return UpdateDepartment(success=False, message="Department not found")

        if department_name:
            department.department_name = department_name
        if description:
            department.description = description
        if director_id:
            department.director_id = director_id

        try:
            db.session.commit()
            return UpdateDepartment(department=department, success=True, message="Department updated successfully")
        except Exception as e:
            db.session.rollback()
            return UpdateDepartment(success=False, message="Failed to update department. Error: " + str(e))

class DeleteDepartment(graphene.Mutation):
    class Arguments:
        department_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, department_id):
        department = Department.query.get(department_id)
        if not department:
            return DeleteDepartment(success=False, message="Department not found")

        try:
            db.session.delete(department)
            db.session.commit()
            return DeleteDepartment(success=True, message="Department deleted successfully")
        except Exception as e:
            db.session.rollback()
            return DeleteDepartment(success=False, message="Failed to delete department. Error: " + str(e))

class DepartmentQuery(graphene.ObjectType):
    all_departments = graphene.List(DepartmentType)
    department = graphene.Field(DepartmentType, department_id=graphene.Int(required=True))

    def resolve_all_departments(self, info):
        return Department.query.all()

    def resolve_department(self, info, department_id):
        return Department.query.get(department_id)

class DepartmentMutation(graphene.ObjectType):
    create_department = CreateDepartment.Field()
    update_department = UpdateDepartment.Field()
    delete_department = DeleteDepartment.Field()

