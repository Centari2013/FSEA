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
api.add_resource(AssociateMissionWithDepartment, '/departments/<int:department_id>/missions')
api.add_resource(DisassociateMissionFromDepartment, '/departments/<int:department_id>/missions/<string:mission_id>')
api.add_resource(GetMissionsForDepartment, '/departments/<int:department_id>/missions')

api.add_resource(PostDesignation, '/designations')
api.add_resource(GetDesignation, '/designations/<int:designation_id>')
api.add_resource(PatchDesignation, '/designations/<int:designation_id>')
api.add_resource(DeleteDesignation, '/designations/<int:designation_id>')

api.add_resource(PostEmployee, '/employees')
api.add_resource(GetEmployee, '/employees/<string:employee_id>')
api.add_resource(PatchEmployee, '/employees/<string:employee_id>')
api.add_resource(DeleteEmployee, '/employees/<string:employee_id>')
api.add_resource(AssociateClearanceWithEmployee, '/employees/<string:employee_id>/clearances')
api.add_resource(GetEmployeeClearances, '/employees/<string:employee_id>/clearances')
api.add_resource(DisassociateClearanceFromEmployee, '/employees/<string:employee_id>/clearances/<int:clearance_id>')
api.add_resource(AssociateDesignationWithEmployee, '/employees/<string:employee_id>/designations')
api.add_resource(DisassociateDesignationFromEmployee, '/employees/<string:employee_id>/designations/<int:designation_id>')
api.add_resource(GetEmployeeDesignations, '/employees/<string:employee_id>/designations')
api.add_resource(GetEmployeeMedicalRecord, '/employees/<string:employee_id>/medical_record')
api.add_resource(PatchEmployeeMedicalRecord, '/employees/<string:employee_id>/medical_record')
api.add_resource(DeleteEmployeeMedicalRecord, '/employees/<string:employee_id>/medical_record')
api.add_resource(UpdateCredentials, 'employees/<string:employee_id>/credentials/')
api.add_resource(GetMissionsByEmployee, '/employees/<string:employee_id>/missions')
api.add_resource(GetSpecimensByResearcher, '/employees/<string:employee_id>/specimens')

api.add_resource(PostMission, '/missions')
api.add_resource(GetMission, '/missions/<string:mission_id>')
api.add_resource(PatchMission, '/missions/<string:mission_id>')
api.add_resource(DeleteMission, '/missions/<string:mission_id>')
api.add_resource(AssociateOriginWithMission, '/missions/<string:mission_id>/origins')
api.add_resource(GetOriginsForMission, '/missions/<string:mission_id>/origins')
api.add_resource(DisassociateOriginFromMission, '/missions/<string:mission_id>/origins/<string:origin_id>')
api.add_resource(GetSpecimensForMission, '/missions/<string:mission_id>/specimens')
api.add_resource(GetDepartmentsForMission, '/missions/<string:mission_id>/departments')
api.add_resource(AddEmployeeToMission, '/missions/<string:mission_id>/employees')
api.add_resource(RemoveEmployeeFromMission, '/missions/<string:mission_id>/employees/<string:employee_id>')
api.add_resource(GetEmployeesByMission, '/missions/<string:mission_id>/employees')

api.add_resource(PostOrigin, '/origins')
api.add_resource(GetOrigin, '/origins/<string:origin_id>')
api.add_resource(PatchOrigin, '/origins/<string:origin_id>')
api.add_resource(DeleteOrigin, '/origins/<string:origin_id>')
api.add_resource(GetMissionsForOrigin, '/origins/<string:origin_id>/missions')

api.add_resource(PostSpecimen, '/specimens')
api.add_resource(GetSpecimen, '/specimens/<string:specimen_id>')
api.add_resource(PatchSpecimen, '/specimens/<string:specimen_id>')
api.add_resource(DeleteSpecimen, '/specimens/<string:specimen_id>')
api.add_resource(AssociateContainmentStatusWithSpecimen, '/specimens/<string:specimen_id>/containment_statuses')
api.add_resource(GetContainmentStatusesForSpecimen, '/specimens/<string:specimen_id>/containment_statuses')
api.add_resource(DisassociateContainmentStatusFromSpecimen, '/specimens/<string:specimen_id>/containment_statuses/<int:containment_status_id>')
api.add_resource(GetSpecimenMedicalRecord, '/specimens/<string:specimen_id>/medical_record')
api.add_resource(PatchSpecimenMedicalRecord, '/specimens/<string:specimen_id>/medical_record')
api.add_resource(DeleteSpecimenMedicalRecord, '/specimens/<string:specimen_id>/medical_record')
api.add_resource(AddSpecimenMission, '/specimens/<string:specimen_id>/missions')
api.add_resource(DeleteSpecimenMission, '/specimens/<string:specimen_id>/missions/<string:mission_id>')
api.add_resource(GetMissionsForSpecimen, '/specimens/<string:specimen_id>/missions')
api.add_resource(AssociateResearcherWithSpecimen, '/specimens/<string:specimen_id>/researchers')
api.add_resource(DisassociateResearcherFromSpecimen, '/specimens/<string:specimen_id>/researchers/<string:employee_id>')
api.add_resource(GetResearchersBySpecimen, '/specimens/<string:specimen_id>/researchers')


# Other
api.add_resource(Login, '/login')
api.add_resource(GetSpecimensForContainmentStatus, '/containment_statuses/<int:containment_status_id>/specimens') 




