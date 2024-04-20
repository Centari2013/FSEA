from ..config import *
from ...models.sqlalchemy_models import SpecimenMedicalRecord
from datetime import datetime

class SpecimenMedicalRecordType(SQLAlchemyObjectType):
    class Meta:
        model = SpecimenMedicalRecord
        interfaces = (graphene.relay.Node,)

class SpecimenMedicalQuery(graphene.ObjectType):
    specimen_medical_record = graphene.Field(SpecimenMedicalRecordType, specimen_id=graphene.Int(required=True))

    def resolve_specimen_medical_record(self, info, specimen_id):
        return SpecimenMedicalRecord.query.get(specimen_id)

class UpdateSpecimenMedicalRecord(graphene.Mutation):
    class Arguments:
        specimen_id = graphene.Int(required=True)
        bloodtype = graphene.String()
        sex = graphene.String()
        kilograms = graphene.Float()
        notes = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()
    medical_record = graphene.Field(SpecimenMedicalRecordType)

    def mutate(self, info, specimen_id, bloodtype=None, sex=None, kilograms=None, notes=None):
        medical_record = SpecimenMedicalRecord.query.get(specimen_id)
        if not medical_record:
            return UpdateSpecimenMedicalRecord(success=False, message="Specimen medical record not found")

        if bloodtype is not None:
            medical_record.bloodtype = bloodtype
        if sex is not None:
            medical_record.sex = sex
        if kilograms is not None:
            medical_record.kilograms = kilograms
        if notes is not None:
            medical_record.notes = notes

        try:
            medical_record.updated = datetime.utcnow()
            db.session.commit()
            return UpdateSpecimenMedicalRecord(success=True, message="Specimen medical record updated successfully", medical_record=medical_record)
        except Exception as e:
            db.session.rollback()
            return UpdateSpecimenMedicalRecord(success=False, message=f"Failed to update specimen medical record. Error: {str(e)}")

class DeleteSpecimenMedicalRecord(graphene.Mutation):
    class Arguments:
        specimen_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, specimen_id):
        medical_record = SpecimenMedicalRecord.query.get(specimen_id)
        if not medical_record:
            return DeleteSpecimenMedicalRecord(success=False, message="Specimen medical record not found")

        try:
            db.session.delete(medical_record)
            db.session.commit()
            return DeleteSpecimenMedicalRecord(success=True, message="Specimen medical record deleted successfully")
        except Exception as e:
            db.session.rollback()
            return DeleteSpecimenMedicalRecord(success=False, message=f"Failed to delete specimen medical record. Error: {str(e)}")

class SpecimenMedicalMutation(graphene.ObjectType):
    update_specimen_medical_record = UpdateSpecimenMedicalRecord.Field()
    delete_specimen_medical_record = DeleteSpecimenMedicalRecord.Field()

