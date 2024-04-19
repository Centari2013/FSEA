from .config import *
from ..models.sqlalchemy_models import Designation

class DesignationType(SQLAlchemyObjectType):
    class Meta:
        model = Designation
        interfaces = (graphene.relay.Node,)

class CreateDesignation(graphene.Mutation):
    class Arguments:
        designation_name = graphene.String(required=True)
        abbreviation = graphene.String(required=True)

    designation = graphene.Field(DesignationType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, designation_name, abbreviation):
        new_designation = Designation(designation_name=designation_name, abbreviation=abbreviation)
        try:
            db.session.add(new_designation)
            db.session.commit()
            return CreateDesignation(designation=new_designation, success=True, message="Designation created successfully")
        except Exception as e:
            db.session.rollback()
            return CreateDesignation(success=False, message="Failed to create new designation. Error: " + str(e))

class UpdateDesignation(graphene.Mutation):
    class Arguments:
        designation_id = graphene.Int(required=True)
        designation_name = graphene.String()
        abbreviation = graphene.String()

    designation = graphene.Field(DesignationType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, designation_id, designation_name=None, abbreviation=None):
        designation = Designation.query.get(designation_id)
        if not designation:
            return UpdateDesignation(success=False, message="Designation not found")

        if designation_name:
            designation.designation_name = designation_name
        if abbreviation:
            designation.abbreviation = abbreviation

        try:
            db.session.commit()
            return UpdateDesignation(designation=designation, success=True, message="Designation updated successfully")
        except Exception as e:
            db.session.rollback()
            return UpdateDesignation(success=False, message="Failed to update designation. Error: " + str(e))

class DeleteDesignation(graphene.Mutation):
    class Arguments:
        designation_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, designation_id):
        designation = Designation.query.get(designation_id)
        if not designation:
            return DeleteDesignation(success=False, message="Designation not found")

        try:
            db.session.delete(designation)
            db.session.commit()
            return DeleteDesignation(success=True, message="Designation deleted successfully")
        except Exception as e:
            db.session.rollback()
            return DeleteDesignation(success=False, message="Failed to delete designation. Error: " + str(e))

class DesignationQuery(graphene.ObjectType):
    all_designations = graphene.List(DesignationType)
    designations = graphene.List(DesignationType, designation_ids=graphene.List(graphene.Int, required=True))

    def resolve_all_designations(self, info):
        # Return all designations
        return Designation.query.all()

    def resolve_designations(self, info, designation_ids):
        # Query for designations with IDs in the provided list
        return Designation.query.filter(Designation.id.in_(designation_ids)).all()

class DesignationMutation(graphene.ObjectType):
    create_designation = CreateDesignation.Field()
    update_designation = UpdateDesignation.Field()
    delete_designation = DeleteDesignation.Field()


