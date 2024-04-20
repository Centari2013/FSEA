from ..config import *
from ...models.sqlalchemy_models import SpecimenContainmentStatus

class SpecimenContainmentStatusType(SQLAlchemyObjectType):
    class Meta:
        model = SpecimenContainmentStatus
        interfaces = (graphene.relay.Node,)

class AssociateContainmentStatusWithSpecimen(graphene.Mutation):
    class Arguments:
        specimen_id = graphene.Int(required=True)
        containment_status_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, specimen_id, containment_status_id):
        new_association = SpecimenContainmentStatus(specimen_id=specimen_id, containment_status_id=containment_status_id)
        try:
            db.session.add(new_association)
            db.session.commit()
            return AssociateContainmentStatusWithSpecimen(success=True, message="Containment status associated with specimen successfully")
        except Exception as e:
            db.session.rollback()
            return AssociateContainmentStatusWithSpecimen(success=False, message=f"Failed to associate containment status with specimen. Error: {str(e)}")

class DisassociateContainmentStatusFromSpecimen(graphene.Mutation):
    class Arguments:
        specimen_id = graphene.Int(required=True)
        containment_status_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, specimen_id, containment_status_id):
        association = SpecimenContainmentStatus.query.filter_by(specimen_id=specimen_id, containment_status_id=containment_status_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return DisassociateContainmentStatusFromSpecimen(success=True, message="Containment status disassociated from specimen successfully")
            except Exception as e:
                db.session.rollback()
                return DisassociateContainmentStatusFromSpecimen(success=False, message=f"Failed to disassociate containment status from specimen. Error: {str(e)}")
        else:
            return DisassociateContainmentStatusFromSpecimen(success=False, message="Association not found")

class SpecimenContainmentStatusQuery(graphene.ObjectType):
    containment_statuses_for_specimen = graphene.List(graphene.Int, specimen_id=graphene.Int(required=True))
    specimens_for_containment_status = graphene.List(graphene.Int, containment_status_id=graphene.Int(required=True))

    def resolve_containment_statuses_for_specimen(self, info, specimen_id):
        associations = SpecimenContainmentStatus.query.filter_by(specimen_id=specimen_id).all()
        return [assoc.containment_status_id for assoc in associations]

    def resolve_specimens_for_containment_status(self, info, containment_status_id):
        associations = SpecimenContainmentStatus.query.filter_by(containment_status_id=containment_status_id).all()
        return [assoc.specimen_id for assoc in associations]

class SpecimenContainmentStatusMutation(graphene.ObjectType):
    associate_containment_status_with_specimen = AssociateContainmentStatusWithSpecimen.Field()
    disassociate_containment_status_from_specimen = DisassociateContainmentStatusFromSpecimen.Field()


