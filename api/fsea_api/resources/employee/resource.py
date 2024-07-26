from ..config import *
from ...models.sqlalchemy_models import Resource


class ResourceType(SQLAlchemyObjectType):
    class Meta:
        model = Resource
        interfaces = (graphene.relay.Node,)

class ResourceQuery(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    get_resources = graphene.List(ResourceType, ids=graphene.List(graphene.Int))

    def resolve_get_resources(self, info, ids=None):
        query = ResourceType.get_query(info)
        if ids:
            query = query.filter(Resource.resource_id.in_(ids))
        return query.all()


class CreateResource(graphene.Mutation):
    class Arguments:
        resource_name = graphene.String(required=True)
        description = graphene.String(required=True)
        resource_type = graphene.String(required=True)

    resource = graphene.Field(ResourceType)

    def mutate(self, info, resource_name, description, resource_type):
        new_resource = Resource(resource_name=resource_name, description=description, resource_type=resource_type)
        db.session.add(new_resource)
        db.session.commit()
        return CreateResource(resource=new_resource)

class UpdateResource(graphene.Mutation):
    class Arguments:
        resource_id = graphene.Int(required=True)
        resource_type = graphene.String()
        resource_name = graphene.String()
        description = graphene.String()

    resource = graphene.Field(ResourceType)

    def mutate(self, info, resource_id, resource_name=None, description=None, resource_type=None):
        resource = Resource.query.get(resource_id)
        if resource is None:
            raise Exception('No resource found with id {}'.format(resource_id))

        if resource_name:
            resource.resource_name = resource_name
        if description:
            resource.description = description
        if resource_type:
            resource.resource_type = resource_type
        
        db.session.commit()
        return UpdateResource(resource=resource)

class DeleteResource(graphene.Mutation):
    class Arguments:
        resource_id = graphene.Int(required=True)

    status = graphene.String()

    def mutate(self, info, resource_id):
        resource = Resource.query.get(resource_id)
        if resource is None:
            raise Exception('No resource found with id {}'.format(resource_id))

        db.session.delete(resource)
        db.session.commit()
        return DeleteResource(status="Resource deleted successfully")
    

class ResourceQuery(graphene.ObjectType):
    all_resources = graphene.List(ResourceType)
    resource = graphene.Field(ResourceType, resource_id=graphene.Int(required=True))

    def resolve_all_resources(self, info):
        return Resource.query.all()

    def resolve_resource(self, info, resource_id):
        return Resource.query.get(resource_id)

class ResourceMutation(graphene.ObjectType):
    create_resource = CreateResource.Field()
    update_resource = UpdateResource.Field()
    delete_resource = DeleteResource.Field()