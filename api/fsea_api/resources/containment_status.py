from .config import *
from ..models.sqlalchemy_models import ContainmentStatus  


class ContainmentStatusType(SQLAlchemyObjectType):
    class Meta:
        model = ContainmentStatus
        interfaces = (graphene.relay.Node,)


class CreateContainmentStatus(graphene.Mutation):
    class Arguments:
        status_name = graphene.String(required=True)
        description = graphene.String(required=True)

    containment_status = graphene.Field(ContainmentStatusType)

    def mutate(self, info, status_name, description):
        new_status = ContainmentStatus(status_name=status_name, description=description)
        db.session.add(new_status)
        db.session.commit()
        return CreateContainmentStatus(containment_status=new_status)

class UpdateContainmentStatus(graphene.Mutation):
    class Arguments:
        containment_status_id = graphene.Int(required=True)
        status_name = graphene.String()
        description = graphene.String()

    containment_status = graphene.Field(ContainmentStatusType)

    def mutate(self, info, containment_status_id, status_name=None, description=None):
        status = ContainmentStatus.query.get(containment_status_id)
        if not status:
            raise Exception('Containment status not found')

        if status_name:
            status.status_name = status_name
        if description:
            status.description = description

        db.session.commit()
        return UpdateContainmentStatus(containment_status=status)

class DeleteContainmentStatus(graphene.Mutation):
    class Arguments:
        containment_status_id = graphene.Int(required=True)

    status = graphene.String()

    def mutate(self, info, containment_status_id):
        status = ContainmentStatus.query.get(containment_status_id)
        if not status:
            raise Exception('Containment status not found')

        db.session.delete(status)
        db.session.commit()
        return DeleteContainmentStatus(status="Containment status deleted successfully")

class ContainmentStatusQuery(graphene.ObjectType):
    all_containment_statuses = graphene.List(ContainmentStatusType)
    containment_status = graphene.Field(ContainmentStatusType, containment_status_id=graphene.Int(required=True))

    def resolve_all_containment_statuses(self, info):
        return ContainmentStatus.query.all()

    def resolve_containment_status(self, info, containment_status_id):
        return ContainmentStatus.query.get(containment_status_id)

class ContainmentStatusMutation(graphene.ObjectType):
    create_containment_status = CreateContainmentStatus.Field()
    update_containment_status = UpdateContainmentStatus.Field()
    delete_containment_status = DeleteContainmentStatus.Field()