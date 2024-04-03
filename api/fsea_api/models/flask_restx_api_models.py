from flask_restx import Model, fields
from fsea_api import api

ClearanceModel = api.model('Clearance', {
    'clearance_id': fields.Integer(description='The clearance unique identifier'),
    'clearance_name': fields.String(required=True, description='The name of the clearance level'),
    'description': fields.String(required=True, description='A description of the clearance level')
})

ContainmentStatusModel = api.model('ContainmentStatus', {
    'containment_status_id': fields.Integer(description='The containment status unique identifier'),
    'status_name': fields.String(required=True, description='The name of the containment status'),
    'description': fields.String(required=True, description='A description of the containment status')
})

DepartmentModel = api.model('Department', {
    'department_id': fields.Integer(description='Department unique identifier'),
    'department_name': fields.String(required=True, description='Name of the department'),
    'director_id': fields.String(description='Employee ID of the department director', nullable=True),
    'description': fields.String(description='A description of the department', nullable=True)
})

DesignationModel = api.model('Designation', {
    'designation_id': fields.Integer(description='Designation unique identifier'),
    'designation_name': fields.String(required=True, description='Name of the designation'),
    'abbreviation': fields.String(required=True, description='Abbreviation of the designation')
})

EmployeeModel = api.model('Employee', {
    'employee_id': fields.String(description='Employee unique identifier'),
    'department_id': fields.Integer(required=True, description='Identifier of the department the employee belongs to'),
    'first_name': fields.String(required=True, description='First name of the employee'),
    'last_name': fields.String(required=True, description='Last name of the employee'),
    'start_date': fields.Date(required=True, description='Start date of employment'),
    'end_date': fields.Date(description='End date of employment, if applicable', nullable=True),
    'notes': fields.Raw(description='JSONB field for additional notes', nullable=True)
})

EmployeeClearanceModel = api.model('EmployeeClearance', {
    'employee_id': fields.String(required=True, description='Employee ID'),
    'clearance_id': fields.Integer(required=True, description='Clearance ID')
})

EmployeeDesignationModel = api.model('EmployeeDesignation', {
    'employee_id': fields.String(required=True, description='Employee ID'),
    'designation_id': fields.Integer(required=True, description='Designation ID')
})

EmployeeMedicalRecordModel = api.model('EmployeeMedicalRecord', {
    'employee_id': fields.String(description='Employee unique identifier'),
    'dob': fields.Date(required=True, description='Date of birth'),
    'bloodtype': fields.String(description='Blood type', nullable=True),
    'sex': fields.String(description='Sex', nullable=True),
    'kilograms': fields.Float(description='Weight in kilograms', nullable=True),
    'height_cm': fields.Float(description='Height in centimeters', nullable=True),
    'notes': fields.Raw(description='JSONB field for additional notes', nullable=True)
})

EmployeeSessionModel = api.model('EmployeeSession', {
    'session_id': fields.String(description='Session unique identifier'),
    'employee_id': fields.String(required=True, description='Associated employee ID'),
    'created': fields.DateTime(description='Session creation timestamp'),
    'expires': fields.DateTime(description='Session expiration timestamp')
})

MissionModel = api.model('Mission', {
    'mission_id': fields.String(description='Mission unique identifier'),
    'mission_name': fields.String(required=True, description='Name of the mission'),
    'start_date': fields.Date(description='Mission start date', nullable=True),
    'end_date': fields.Date(description='Mission end date', nullable=True),
    'commander_id': fields.String(description='Commander employee ID', nullable=True),
    'supervisor_id': fields.String(description='Supervisor employee ID', nullable=True),
    'description': fields.String(required=True, description='A description of the mission'),
    'notes': fields.Raw(description='JSONB field for additional notes', nullable=True)
})

SpecimenContainmentStatusModel = api.model('SpecimenContainmentStatus', {
    'specimen_id': fields.String(required=True, description='Specimen unique identifier'),
    'containment_status_id': fields.Integer(required=True, description='Containment status unique identifier')
})

SpecimenMedicalRecordModel = api.model('SpecimenMedicalRecord', {
    'specimen_id': fields.String(required=True, description='Specimen unique identifier'),
    'bloodtype': fields.String(description='Blood type of the specimen', nullable=True),
    'sex': fields.String(description='Sex of the specimen', nullable=True),
    'kilograms': fields.Float(description='Weight of the specimen in kilograms', nullable=True),
    'notes': fields.Raw(description='JSONB field for additional notes', nullable=True)
})

SpecimenMissionModel = api.model('SpecimenMission', {
    'specimen_id': fields.String(required=True, description='Specimen unique identifier'),
    'mission_id': fields.String(required=True, description='Mission unique identifier'),
    'involvement_summary': fields.String(description='Summary of the specimen\'s involvement in the mission', nullable=True)
})

DepartmentMissionModel = api.model('DepartmentMission', {
    'department_id': fields.Integer(required=True, description='Department unique identifier'),
    'mission_id': fields.String(required=True, description='Mission unique identifier')
})

EmployeeMissionModel = api.model('EmployeeMission', {
    'employee_id': fields.String(required=True, description='Employee unique identifier'),
    'mission_id': fields.String(required=True, description='Mission unique identifier'),
    'involvement_summary': fields.String(description='Summary of the employee\'s involvement in the mission', nullable=True)
})

ResearcherSpecimenModel = api.model('ResearcherSpecimen', {
    'employee_id': fields.String(required=True, description='Employee unique identifier, acting as the researcher'),
    'specimen_id': fields.String(required=True, description='Specimen unique identifier')
})