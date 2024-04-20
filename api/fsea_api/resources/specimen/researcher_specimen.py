from ..config import *
from ...models.sqlalchemy_models import ResearcherSpecimen

class ResearcherSpecimenType(SQLAlchemyObjectType):
    class Meta:
        model = ResearcherSpecimen
        interfaces = (graphene.relay.Node,)

class AssociateResearcherWithSpecimen(graphene.Mutation):
    class Arguments:
        specimen_id = graphene.String(required=True)
        employee_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, specimen_id, employee_id):
        new_association = ResearcherSpecimen(employee_id=employee_id, specimen_id=specimen_id)
        try:
            db.session.add(new_association)
            db.session.commit()
            return AssociateResearcherWithSpecimen(success=True, message="Researcher associated with specimen successfully")
        except Exception as e:
            db.session.rollback()
            return AssociateResearcherWithSpecimen(success=False, message=f"Failed to associate researcher with specimen. Error: {str(e)}")

class DisassociateResearcherFromSpecimen(graphene.Mutation):
    class Arguments:
        specimen_id = graphene.String(required=True)
        employee_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, specimen_id, employee_id):
        association = ResearcherSpecimen.query.filter_by(employee_id=employee_id, specimen_id=specimen_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return DisassociateResearcherFromSpecimen(success=True, message="Researcher disassociated from specimen successfully")
            except Exception as e:
                db.session.rollback()
                return DisassociateResearcherFromSpecimen(success=False, message=f"Failed to disassociate researcher from specimen. Error: {str(e)}")
        else:
            return DisassociateResearcherFromSpecimen(success=False, message="Researcher-specimen link not found")

class ResearcherSpecimenQuery(graphene.ObjectType):
    specimens_by_researcher = graphene.List(graphene.String, employee_id=graphene.String(required=True))
    researchers_by_specimen = graphene.List(graphene.String, specimen_id=graphene.String(required=True))

    def resolve_specimens_by_researcher(self, info, employee_id):
        links = ResearcherSpecimen.query.filter_by(employee_id=employee_id).all()
        return [link.specimen_id for link in links]

    def resolve_researchers_by_specimen(self, info, specimen_id):
        links = ResearcherSpecimen.query.filter_by(specimen_id=specimen_id).all()
        return [link.employee_id for link in links]

class ResearcherSpecimenMutation(graphene.ObjectType):
    associate_researcher_with_specimen = AssociateResearcherWithSpecimen.Field()
    disassociate_researcher_from_specimen = DisassociateResearcherFromSpecimen.Field()


