from ..config import *
from ...models.sqlalchemy_models import ClearanceResourceAccess

class ClearanceResourceAccessType(SQLAlchemyObjectType):
    class Meta:
        model = ClearanceResourceAccess
        interfaces = (graphene.relay.Node,)

class AssociateClearanceWithResource(graphene.Mutation):
    class Arguments:
        clearance_id = graphene.Int(required=True)
        resource_id = graphene.Int(required=True)
        access_type = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, clearance_id, resource_id, access_type):
        new_association = ClearanceResourceAccess(clearance_id=clearance_id, resource_id=resource_id, access_type=access_type)
        try:
            db.session.add(new_association)
            db.session.commit()
            return AssociateClearanceWithResource(success=True, message="Resource associated with clearance successfully")
        except Exception as e:
            db.session.rollback()
            return AssociateClearanceWithResource(success=False, message=f"Failed to associate resource with clearance. Error: {str(e)}")

class DisassociateClearanceFromResource(graphene.Mutation):
    class Arguments:
        clearance_id = graphene.Int(required=True)
        resource_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, clearance_id, resource_id):
        association = ClearanceResourceAccess.query.filter_by(clearance_id=clearance_id, resource_id=resource_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return DisassociateClearanceFromResource(success=True, message="Resource disassociated from clearance successfully")
            except Exception as e:
                db.session.rollback()
                return DisassociateClearanceFromResource(success=False, message=f"Failed to disassociate resource from clearance. Error: {str(e)}")
        else:
            return DisassociateClearanceFromResource(success=False, message="Association not found")


class GetClearanceResourceAccesses(graphene.ObjectType):
    resources = graphene.List(ClearanceResourceAccessType, clearance_id=graphene.Int(required=True))

    def resolve_resources(self, info, clearance_id):
        return ClearanceResourceAccess.query.filter_by(clearance_id=clearance_id).all()

class ClearanceResourceAccessQuery(graphene.ObjectType):
    clearance_resources = graphene.List(ClearanceResourceAccessType, clearance_id=graphene.Int(required=True))

    def resolve_clearance_resources(self, info, clearance_id):
        return ClearanceResourceAccess.query.filter_by(clearance_id=clearance_id).all()


class ClearanceResourceAccessMutation(graphene.ObjectType):
    associate_clearance_with_resource = AssociateClearanceWithResource.Field()
    disassociate_clearance_from_resource = DisassociateClearanceFromResource.Field()



