from .config import *
from ..models.sqlalchemy_models import Employee

class EmployeeType(SQLAlchemyObjectType):
    class Meta:
        model = Employee
        interfaces = (graphene.relay.Node,)

class CreateEmployee(graphene.Mutation):
    class Arguments:
        employee_id = graphene.String(required=True)
        department_id = graphene.Int(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        start_date = graphene.Date(required=True)
        end_date = graphene.Date()
        notes = graphene.String()

    employee = graphene.Field(EmployeeType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, employee_id, department_id, first_name, last_name, start_date, end_date=None, notes=None):
        new_employee = Employee(
            employee_id=employee_id,
            department_id=department_id,
            first_name=first_name,
            last_name=last_name,
            start_date=start_date,
            end_date=end_date,
            notes=notes
        )
        try:
            db.session.add(new_employee)
            db.session.commit()
            return CreateEmployee(employee=new_employee, success=True, message="New employee created successfully")
        except Exception as e:
            db.session.rollback()
            return CreateEmployee(success=False, message=f"Failed to create new employee. Error: {str(e)}")

class UpdateEmployee(graphene.Mutation):
    class Arguments:
        employee_id = graphene.String(required=True)
        department_id = graphene.Int()
        first_name = graphene.String()
        last_name = graphene.String()
        start_date = graphene.Date()
        end_date = graphene.Date()
        notes = graphene.String()

    employee = graphene.Field(EmployeeType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, employee_id, department_id=None, first_name=None, last_name=None, start_date=None, end_date=None, notes=None):
        employee = Employee.query.get(employee_id)
        if not employee:
            return UpdateEmployee(success=False, message="Employee not found")

        if department_id:
            employee.department_id = department_id
        if first_name:
            employee.first_name = first_name
        if last_name:
            employee.last_name = last_name
        if start_date:
            employee.start_date = start_date
        if end_date:
            employee.end_date = end_date
        if notes:
            employee.notes = notes

        try:
            db.session.commit()
            return UpdateEmployee(employee=employee, success=True, message="Employee updated successfully")
        except Exception as e:
            db.session.rollback()
            return UpdateEmployee(success=False, message=f"Failed to update employee. Error: {str(e)}")

class DeleteEmployee(graphene.Mutation):
    class Arguments:
        employee_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, employee_id):
        employee = Employee.query.get(employee_id)
        if not employee:
            return DeleteEmployee(success=False, message="Employee not found")

        try:
            db.session.delete(employee)
            db.session.commit()
            return DeleteEmployee(success=True, message="Employee deleted successfully")
        except Exception as e:
            db.session.rollback()
            return DeleteEmployee(success=False, message=f"Failed to delete employee. Error: {str(e)}")

class EmployeeQuery(graphene.ObjectType):
    employee = graphene.Field(EmployeeType, employee_id=graphene.String(required=True))
    all_employees = graphene.List(EmployeeType, department_id=graphene.Int(required=False))

    def resolve_employee(self, info, employee_id):
        return Employee.query.get(employee_id)

    def resolve_all_employees(self, info, department_id=None):
        query = Employee.query
        if department_id:
            query = query.filter(Employee.department_id == department_id)
        return query.all()

class EmployeeMutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()
    delete_employee = DeleteEmployee.Field()


