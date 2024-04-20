from ..config import *
from ...models.sqlalchemy_models import EmployeeDesignation

class EmployeeDesignationType(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeDesignation
        interfaces = (graphene.relay.Node,)

class AssociateDesignationWithEmployee(graphene.Mutation):
    class Arguments:
        employee_id = graphene.String(required=True)
        designation_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, employee_id, designation_id):
        new_association = EmployeeDesignation(employee_id=employee_id, designation_id=designation_id)
        try:
            db.session.add(new_association)
            db.session.commit()
            return AssociateDesignationWithEmployee(success=True, message="Designation associated with employee successfully")
        except Exception as e:
            db.session.rollback()
            return AssociateDesignationWithEmployee(success=False, message=f"Failed to associate designation with employee. Error: {str(e)}")

class DisassociateDesignationFromEmployee(graphene.Mutation):
    class Arguments:
        employee_id = graphene.String(required=True)
        designation_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, employee_id, designation_id):
        association = EmployeeDesignation.query.filter_by(employee_id=employee_id, designation_id=designation_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return DisassociateDesignationFromEmployee(success=True, message="Designation disassociated from employee successfully")
            except Exception as e:
                db.session.rollback()
                return DisassociateDesignationFromEmployee(success=False, message=f"Failed to disassociate designation from employee. Error: {str(e)}")
        else:
            return DisassociateDesignationFromEmployee(success=False, message="Association not found")

class GetEmployeeDesignations(graphene.ObjectType):
    class Arguments:
        employee_id = graphene.String(required=True)

    designations = graphene.List(graphene.Int)

    def resolve_designations(self, info, employee_id):
        print(employee_id)
        associations = EmployeeDesignation.query.filter_by(employee_id=employee_id).all()
        print(associations)
        if associations:
            return [association.designation_id for association in associations]
        else:
            return []

class EmployeeDesignationQuery(graphene.ObjectType):
    employee_designations = graphene.Field(GetEmployeeDesignations, employee_id=graphene.String(required=True))

class EmployeeDesignationMutation(graphene.ObjectType):
    associate_designation_with_employee = AssociateDesignationWithEmployee.Field()
    disassociate_designation_from_employee = DisassociateDesignationFromEmployee.Field()

