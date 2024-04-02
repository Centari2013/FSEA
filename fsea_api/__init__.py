from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
db = SQLAlchemy(app)
api = Api(app)


from fsea_api.resources import *
api.add_resource(PostClearance, '/clearances')
api.add_resource(GetClearance, '/clearances/<int:clearance_id>')
api.add_resource(PatchClearance, '/clearances/<int:clearance_id>')
api.add_resource(DeleteClearance, '/clearances/<int:clearance_id>')

api.add_resource(PostContainmentStatus, '/containment_statuses')
api.add_resource(GetContainmentStatus, '/containment_statuses/<int:containment_status_id>')
api.add_resource(PatchContainmentStatus, '/containment_statuses/<int:containment_status_id>')
api.add_resource(DeleteContainmentStatus, '/containment_statuses/<int:containment_status_id>')

api.add_resource(PostDepartment, '/departments')
api.add_resource(GetDepartment, '/departments/<int:department_id>')
api.add_resource(PatchDepartment, '/departments/<int:department_id>')
api.add_resource(DeleteDepartment, '/departments/<int:department_id>')

api.add_resource(PostDesignation, '/designations')
api.add_resource(GetDesignation, '/designations/<int:designation_id>')
api.add_resource(PatchDesignation, '/designations/<int:designation_id>')
api.add_resource(DeleteDesignation, '/designations/<int:designation_id>')

api.add_resource(PostEmployee, '/employees')
api.add_resource(GetEmployee, '/employees/<string:employee_id>')
api.add_resource(PatchEmployee, '/employees/<string:employee_id>')
api.add_resource(DeleteEmployee, '/employees/<string:employee_id>')

api.add_resource(AssociateClearanceWithEmployee, '/employee_clearances')
api.add_resource(DisassociateClearanceFromEmployee, '/employee_clearances/<string:employee_id>/<int:clearance_id>')
api.add_resource(GetEmployeeClearances, '/employee_clearances/<string:employee_id>')

api.add_resource(AssociateDesignationWithEmployee, '/employee_designations')
api.add_resource(DisassociateDesignationFromEmployee, '/employee_designations/<string:employee_id>/<int:designation_id>')
api.add_resource(GetEmployeeDesignations, '/employee_designations/<string:employee_id>')

api.add_resource(PostEmployeeMedicalRecord, '/employee_medical_records')
api.add_resource(GetEmployeeMedicalRecord, '/employee_medical_records/<string:employee_id>')
api.add_resource(PatchEmployeeMedicalRecord, '/employee_medical_records/<string:employee_id>')
api.add_resource(DeleteEmployeeMedicalRecord, '/employee_medical_records/<string:employee_id>')

api.add_resource(PostMission, '/missions')
api.add_resource(GetMission, '/missions/<string:mission_id>')
api.add_resource(PatchMission, '/missions/<string:mission_id>')
api.add_resource(DeleteMission, '/missions/<string:mission_id>')

api.add_resource(PostOrigin, '/origins')
api.add_resource(GetOrigin, '/origins/<string:origin_id>')
api.add_resource(PatchOrigin, '/origins/<string:origin_id>')
api.add_resource(DeleteOrigin, '/origins/<string:origin_id>')

api.add_resource(AssociateOriginWithMission, '/mission-origins')
api.add_resource(DisassociateOriginFromMission, '/mission-origins/<string:mission_id>/<string:origin_id>')
api.add_resource(GetOriginsForMission, '/missions/<string:mission_id>/origins')
api.add_resource(GetMissionsForOrigin, '/origins/<string:origin_id>/missions')


