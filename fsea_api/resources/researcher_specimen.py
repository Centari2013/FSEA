from .imports import *
from ..models import ResearcherSpecimen

class AssociateResearcherWithSpecimen(Resource):
    def post(self, specimen_id):
        parser = reqparse.RequestParser()
        parser.add_argument('employee_id', type=str, required=True, help="Employee ID cannot be blank.")
        data = parser.parse_args()

        new_association = ResearcherSpecimen(employee_id=data['employee_id'], specimen_id=specimen_id)
        try:
            db.session.add(new_association)
            db.session.commit()
            return {'message': 'Researcher associated with specimen successfully'}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to associate researcher with specimen. Error: {str(e)}'}, 500


class DisassociateResearcherFromSpecimen(Resource):
    def delete(self, employee_id, specimen_id):
        association = ResearcherSpecimen.query.filter_by(employee_id=employee_id, specimen_id=specimen_id).first()
        if association:
            try:
                db.session.delete(association)
                db.session.commit()
                return {'message': 'Researcher disassociated from specimen successfully'}, 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'message': f'Failed to disassociate researcher from specimen. Error: {str(e)}'}, 500
        else:
            return {'message': 'Researcher-specimen link not found'}, 404


class GetSpecimensByResearcher(Resource):
    def get(self, employee_id):
        links = ResearcherSpecimen.query.filter_by(employee_id=employee_id).all()
        if links:
            specimens = [{'specimen_id': link.specimen_id} for link in links]
            return {'specimens': specimens}, 200
        else:
            return {'message': 'No specimens found for this researcher'}, 404


class GetResearchersBySpecimen(Resource):
    def get(self, specimen_id):
        links = ResearcherSpecimen.query.filter_by(specimen_id=specimen_id).all()
        if links:
            researchers = [{'employee_id': link.employee_id} for link in links]
            return {'researchers': researchers}, 200
        else:
            return {'message': 'No researchers found for this specimen'}, 404
