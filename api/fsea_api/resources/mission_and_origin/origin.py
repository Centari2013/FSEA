from ..config import *
from ...models.sqlalchemy_models import Origin
from datetime import datetime

class OriginType(SQLAlchemyObjectType):
    class Meta:
        model = Origin
        interfaces = (graphene.relay.Node,)

class CreateOrigin(graphene.Mutation):
    class Arguments:
        origin_id = graphene.String(required=True)
        origin_name = graphene.String(required=True)
        discovery_date = graphene.Date(required=True)
        description = graphene.String(required=True)
        notes = graphene.String()

    origin = graphene.Field(OriginType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, origin_id, origin_name, discovery_date, description, notes=None):
        new_origin = Origin(
            origin_id=origin_id,
            origin_name=origin_name,
            discovery_date=discovery_date,
            description=description,
            notes=notes
        )
        try:
            db.session.add(new_origin)
            db.session.commit()
            return CreateOrigin(origin=new_origin, success=True, message="New origin created successfully")
        except Exception as e:
            db.session.rollback()
            return CreateOrigin(success=False, message=f"Failed to create new origin. Error: {str(e)}")

class UpdateOrigin(graphene.Mutation):
    class Arguments:
        origin_id = graphene.String(required=True)
        origin_name = graphene.String()
        discovery_date = graphene.Date()
        description = graphene.String()
        notes = graphene.String()

    origin = graphene.Field(OriginType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, origin_id, origin_name=None, discovery_date=None, description=None, notes=None):
        origin = Origin.query.get(origin_id)
        if not origin:
            return UpdateOrigin(success=False, message="Origin not found")

        if origin_name:
            origin.origin_name = origin_name
        if discovery_date:
            origin.discovery_date = discovery_date
        if description:
            origin.description = description
        if notes:
            origin.notes = notes

        try:
            origin.updated = datetime.utcnow()
            db.session.commit()
            return UpdateOrigin(origin=origin, success=True, message="Origin updated successfully")
        except Exception as e:
            db.session.rollback()
            return UpdateOrigin(success=False, message=f"Failed to update origin. Error: {str(e)}")

class DeleteOrigin(graphene.Mutation):
    class Arguments:
        origin_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, origin_id):
        origin = Origin.query.get(origin_id)
        if not origin:
            return DeleteOrigin(success=False, message="Origin not found")

        try:
            db.session.delete(origin)
            db.session.commit()
            return DeleteOrigin(success=True, message="Origin deleted successfully")
        except Exception as e:
            db.session.rollback()
            return DeleteOrigin(success=False, message=f"Failed to delete origin. Error: {str(e)}")

class OriginQuery(graphene.ObjectType):
    origin = graphene.Field(OriginType, origin_id=graphene.String(required=True))
    all_origins = graphene.List(OriginType)

    def resolve_origin(self, info, origin_id):
        return Origin.query.get(origin_id)

    def resolve_all_origins(self, info):
        return Origin.query.all()

class OriginMutation(graphene.ObjectType):
    create_origin = CreateOrigin.Field()
    update_origin = UpdateOrigin.Field()
    delete_origin = DeleteOrigin.Field()


