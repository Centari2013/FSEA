from .config import *
from ..models.sqlalchemy_models import EmployeeClearance

class EmployeeClearanceType(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeClearance
        interfaces = (graphene.relay.Node,)

class AssociateClearanceWithEmployee(graphene.Mutation):
    class Arguments:
        employee_id = graphene.Int(required=True)
        clearance_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, employee_id, clearance_id):
        new_association = EmployeeClearance(employee_id=employee_id, clearance_id=clearance_id)
        try:
            db.session.add(new_association)
            db.session.commit()
            return AssociateClearanceWithEmployee(success=True, message="Clearance associated with employee successfully")
        except Exception as e:
            db.session.rollback()
            return AssociateClearanceWithEmployee(success=False, message=f"Failed to associate clearance with employee. Error: {str(e)}")

class DisassociateClearanceFromEmployee(graphene.Mutation):
    class Arguments:
        employee_id = graphene.Int(required=True)
        clearance_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, employee_id, clearance_id):
        association = EmployeeClearance.query.filter_by(employee_id=employee_id, clearance_id=clearance_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return DisassociateClearanceFromEmployee(success=True, message="Clearance disassociated from employee successfully")
            except Exception as e:
                db.session.rollback()
                return DisassociateClearanceFromEmployee(success=False, message=f"Failed to disassociate clearance from employee. Error: {str(e)}")
        else:
            return DisassociateClearanceFromEmployee(success=False, message="Association not found")

class GetEmployeeClearances(graphene.ObjectType):
    class Arguments:
        employee_id = graphene.Int(required=True)

    clearances = graphene.List(graphene.Int)

    def resolve_clearances(self, info, employee_id):
        clearances = EmployeeClearance.query.filter_by(employee_id=employee_id).all()
        if clearances:
            return [clearance.clearance_id for clearance in clearances]
        else:
            return []

class EmployeeClearanceQuery(graphene.ObjectType):
    employee_clearances = graphene.Field(GetEmployeeClearances, employee_id=graphene.Int(required=True))

class EmployeeClearanceMutation(graphene.ObjectType):
    associate_clearance_with_employee = AssociateClearanceWithEmployee.Field()
    disassociate_clearance_from_employee = DisassociateClearanceFromEmployee.Field()


