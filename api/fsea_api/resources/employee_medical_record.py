from .config import *
from ..models.sqlalchemy_models import EmployeeMedicalRecord
from datetime import datetime

class EmployeeMedicalRecordType(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeMedicalRecord
        interfaces = (graphene.relay.Node,)

class GetEmployeeMedicalRecord(graphene.ObjectType):
    class Arguments:
        employee_id = graphene.Int(required=True)

    medical_record = graphene.Field(EmployeeMedicalRecordType)

    def resolve_medical_record(self, info, employee_id):
        return EmployeeMedicalRecord.query.get(employee_id)

class UpdateEmployeeMedicalRecord(graphene.Mutation):
    class Arguments:
        employee_id = graphene.Int(required=True)
        dob = graphene.Date()
        bloodtype = graphene.String()
        sex = graphene.String()
        kilograms = graphene.Float()
        height_cm = graphene.Float()
        notes = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, employee_id, **kwargs):
        medical_record = EmployeeMedicalRecord.query.get(employee_id)
        if not medical_record:
            return UpdateEmployeeMedicalRecord(success=False, message="Medical record not found")

        for key, value in kwargs.items():
            if value is not None:
                setattr(medical_record, key, value)

        try:
            medical_record.updated = datetime.utcnow()
            db.session.commit()
            return UpdateEmployeeMedicalRecord(success=True, message="Medical record updated successfully")
        except Exception as e:
            db.session.rollback()
            return UpdateEmployeeMedicalRecord(success=False, message=f"Failed to update medical record. Error: {str(e)}")

class DeleteEmployeeMedicalRecord(graphene.Mutation):
    class Arguments:
        employee_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, employee_id):
        medical_record = EmployeeMedicalRecord.query.get(employee_id)
        if not medical_record:
            return DeleteEmployeeMedicalRecord(success=False, message="Medical record not found")

        try:
            db.session.delete(medical_record)
            db.session.commit()
            return DeleteEmployeeMedicalRecord(success=True, message="Medical record deleted successfully")
        except Exception as e:
            db.session.rollback()
            return DeleteEmployeeMedicalRecord(success=False, message=f"Failed to delete medical record. Error: {str(e)}")

class EmployeeMedicalQuery(graphene.ObjectType):
    employee_medical_record = graphene.Field(EmployeeMedicalRecordType, employee_id=graphene.Int(required=True))
    resolve_employee_medical_record = GetEmployeeMedicalRecord.resolve_medical_record

class EmployeeMedicalMutation(graphene.ObjectType):
    update_employee_medical_record = UpdateEmployeeMedicalRecord.Field()
    delete_employee_medical_record = DeleteEmployeeMedicalRecord.Field()


