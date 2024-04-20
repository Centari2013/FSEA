from ..config import *
from ...models.sqlalchemy_models import Clearance


class ClearanceType(SQLAlchemyObjectType):
    class Meta:
        model = Clearance
        interfaces = (graphene.relay.Node,)

class ClearanceQuery(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    get_clearances = graphene.List(ClearanceType, ids=graphene.List(graphene.Int))

    def resolve_get_clearances(self, info, ids=None):
        query = ClearanceType.get_query(info)
        if ids:
            query = query.filter(Clearance.clearance_id.in_(ids))
        return query.all()


class CreateClearance(graphene.Mutation):
    class Arguments:
        clearance_name = graphene.String(required=True)
        description = graphene.String(required=True)

    clearance = graphene.Field(ClearanceType)

    def mutate(self, info, clearance_name, description):
        new_clearance = Clearance(clearance_name=clearance_name, description=description)
        db.session.add(new_clearance)
        db.session.commit()
        return CreateClearance(clearance=new_clearance)

class UpdateClearance(graphene.Mutation):
    class Arguments:
        clearance_id = graphene.Int(required=True)
        clearance_name = graphene.String()
        description = graphene.String()

    clearance = graphene.Field(ClearanceType)

    def mutate(self, info, clearance_id, clearance_name=None, description=None):
        clearance = Clearance.query.get(clearance_id)
        if clearance is None:
            raise Exception('No clearance found with id {}'.format(clearance_id))

        if clearance_name:
            clearance.clearance_name = clearance_name
        if description:
            clearance.description = description
        
        db.session.commit()
        return UpdateClearance(clearance=clearance)

class DeleteClearance(graphene.Mutation):
    class Arguments:
        clearance_id = graphene.Int(required=True)

    status = graphene.String()

    def mutate(self, info, clearance_id):
        clearance = Clearance.query.get(clearance_id)
        if clearance is None:
            raise Exception('No clearance found with id {}'.format(clearance_id))

        db.session.delete(clearance)
        db.session.commit()
        return DeleteClearance(status="Clearance deleted successfully")
    

class ClearanceQuery(graphene.ObjectType):
    all_clearances = graphene.List(ClearanceType)
    clearance = graphene.Field(ClearanceType, clearance_id=graphene.Int(required=True))

    def resolve_all_clearances(self, info):
        return Clearance.query.all()

    def resolve_clearance(self, info, clearance_id):
        return Clearance.query.get(clearance_id)

class ClearanceMutation(graphene.ObjectType):
    create_clearance = CreateClearance.Field()
    update_clearance = UpdateClearance.Field()
    delete_clearance = DeleteClearance.Field()