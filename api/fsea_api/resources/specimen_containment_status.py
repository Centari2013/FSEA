from .imports import *
from .. models import SpecimenContainmentStatus

class AssociateContainmentStatusWithSpecimen(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('specimen_id', type=str, required=True, help="Specimen ID cannot be blank.")
        parser.add_argument('containment_status_id', type=int, required=True, help="Containment status ID cannot be blank.")
        data = parser.parse_args()

        new_association = SpecimenContainmentStatus(**data)
        try:
            db.session.add(new_association)
            db.session.commit()
            return {'message': 'Containment status associated with specimen successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to associate containment status with specimen. Error: {str(e)}'}, 500


class DisassociateContainmentStatusFromSpecimen(Resource):
    def delete(self, specimen_id, containment_status_id):
        association = SpecimenContainmentStatus.query.filter_by(specimen_id=specimen_id, containment_status_id=containment_status_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return {'message': 'Containment status disassociated from specimen successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'message': f'Failed to disassociate containment status from specimen. Error: {str(e)}'}, 500
        else:
            return {'message': 'Association not found'}, 404


class GetContainmentStatusesForSpecimen(Resource):
    def get(self, specimen_id):
        associations = SpecimenContainmentStatus.query.filter_by(specimen_id=specimen_id).all()
        if associations:
            statuses = [{'containment_status_id': assoc.containment_status_id} for assoc in associations]
            return {'containment_statuses': statuses}, 200
        else:
            return {'message': 'No containment statuses found for this specimen'}, 404


class GetSpecimensForContainmentStatus(Resource):
    def get(self, containment_status_id):
        associations = SpecimenContainmentStatus.query.filter_by(containment_status_id=containment_status_id).all()
        if associations:
            specimens = [{'specimen_id': assoc.specimen_id} for assoc in associations]
            return {'specimens': specimens}, 200
        else:
            return {'message': 'No specimens found for this containment status'}, 404


