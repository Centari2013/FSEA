from ..config import *
from ...models.sqlalchemy_models import Specimen, SpecimenContainmentStatus, ContainmentStatus, Employee, ResearcherSpecimen
from datetime import datetime
from .containment_status import ContainmentStatusType
from ..employee.employee import EmployeeType

class SpecimenType(SQLAlchemyObjectType):
    class Meta:
        model = Specimen
        interfaces = (graphene.relay.Node,)
    
    containment_statuses = graphene.List(lambda: ContainmentStatusType)
    researchers = graphene.List(lambda: EmployeeType)

    def resolve_containment_statuses(self, info):
        status_ids = [c[0] for c in SpecimenContainmentStatus.query\
                        .filter_by(specimen_id=self.specimen_id)\
                        .with_entities(SpecimenContainmentStatus.containment_status_id)\
                        .all()]
        return ContainmentStatus.query.filter(ContainmentStatus.containment_status_id.in_(status_ids)).all()
    
    def resolve_researchers(self, info):
        employee_ids = [r[0] for r in ResearcherSpecimen.query\
                        .filter_by(specimen_id=self.specimen_id)\
                        .with_entities(ResearcherSpecimen.employee_id)\
                        .all()]
        return Employee.query.filter(Employee.employee_id.in_(employee_ids)).all()

class CreateSpecimen(graphene.Mutation):
    class Arguments:
        specimen_id = graphene.String(required=True)
        specimen_name = graphene.String(required=True)
        origin_id = graphene.String()
        mission_id = graphene.String()
        threat_level = graphene.Float(required=True)
        acquisition_date = graphene.Date(required=True)
        notes = graphene.String()
        description = graphene.String()

    specimen = graphene.Field(SpecimenType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, specimen_id, specimen_name, threat_level, acquisition_date, origin_id=None, mission_id=None, notes=None, description=None):
        new_specimen = Specimen(
            specimen_id=specimen_id,
            specimen_name=specimen_name,
            origin_id=origin_id,
            mission_id=mission_id,
            threat_level=threat_level,
            acquisition_date=acquisition_date,
            notes=notes,
            description=description
        )
        try:
            db.session.add(new_specimen)
            db.session.commit()
            return CreateSpecimen(specimen=new_specimen, success=True, message="New specimen created successfully")
        except Exception as e:
            db.session.rollback()
            return CreateSpecimen(success=False, message=f"Failed to create new specimen. Error: {str(e)}")

class UpdateSpecimen(graphene.Mutation):
    class Arguments:
        specimen_id = graphene.String(required=True)
        specimen_name = graphene.String()
        origin_id = graphene.String()
        mission_id = graphene.String()
        threat_level = graphene.Float()
        acquisition_date = graphene.Date()
        notes = graphene.String()
        description = graphene.String()

    specimen = graphene.Field(SpecimenType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, specimen_id, specimen_name=None, origin_id=None, mission_id=None, threat_level=None, acquisition_date=None, notes=None, description=None):
        specimen = Specimen.query.get(specimen_id)
        if not specimen:
            return UpdateSpecimen(success=False, message="Specimen not found")

        specimen.specimen_name = specimen_name if specimen_name is not None else specimen.specimen_name
        specimen.origin_id = origin_id if origin_id is not None else specimen.origin_id
        specimen.mission_id = mission_id if mission_id is not None else specimen.mission_id
        specimen.threat_level = threat_level if threat_level is not None else specimen.threat_level
        specimen.acquisition_date = acquisition_date if acquisition_date is not None else specimen.acquisition_date
        specimen.notes = notes if notes is not None else specimen.notes
        specimen.description = description if description is not None else specimen.description

        try:
            specimen.updated = datetime.utcnow()
            db.session.commit()
            return UpdateSpecimen(specimen=specimen, success=True, message="Specimen updated successfully")
        except Exception as e:
            db.session.rollback()
            return UpdateSpecimen(success=False, message=f"Failed to update specimen. Error: {str(e)}")

class DeleteSpecimen(graphene.Mutation):
    class Arguments:
        specimen_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, specimen_id):
        specimen = Specimen.query.get(specimen_id)
        if not specimen:
            return DeleteSpecimen(success=False, message="Specimen not found")

        try:
            db.session.delete(specimen)
            db.session.commit()
            return DeleteSpecimen(success=True, message="Specimen deleted successfully")
        except Exception as e:
            db.session.rollback()
            return DeleteSpecimen(success=False, message=f"Failed to delete specimen. Error: {str(e)}")

class SpecimenQuery(graphene.ObjectType):
    specimen = graphene.Field(SpecimenType, specimen_id=graphene.String(required=True))
    all_specimens = graphene.List(SpecimenType)

    def resolve_specimen(self, info, specimen_id):
        return Specimen.query.get(specimen_id)

    def resolve_all_specimens(self, info):
        return Specimen.query.all()

class SpecimenMutation(graphene.ObjectType):
    create_specimen = CreateSpecimen.Field()
    update_specimen = UpdateSpecimen.Field()
    delete_specimen = DeleteSpecimen.Field()


