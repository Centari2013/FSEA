from datetime import datetime, timedelta, timezone
from fsea_api import db
from sqlalchemy.dialects.postgresql import JSONB
from  sqlalchemy import CheckConstraint




class Clearance(db.Model):
    __tablename__ = 'clearances'
    clearance_id = db.Column(db.Integer, primary_key=True)
    clearance_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

class Resource(db.Model):
    __tablename__ = 'resources'
    resource_id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.Text, nullable=False)
    resource_type = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.CheckConstraint("resource_type IN ('column', 'table')", name='check_resource_type'),
    )

class ClearanceResourceAccess(db.Model):
    __tablename__ = 'clearance_resource_access'
    
    clearance_id = db.Column(db.Integer, db.ForeignKey('clearances.clearance_id'), primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.resource_id'), primary_key=True)
    access_type = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated = db.Column(db.DateTime, nullable=True)
    
    __table_args__ = (
        db.CheckConstraint("access_type IN ('read', 'write', 'read_write')", name='check_access_type'),
    )

class ContainmentStatus(db.Model):
    __tablename__ = 'containment_statuses'
    containment_status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)


class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.Text, nullable=False)
    director_id = db.Column(db.String(8), db.ForeignKey('employees.employee_id'))
    description = db.Column(db.Text)


class Designation(db.Model):
    __tablename__ = 'designations'
    designation_id = db.Column(db.Integer, primary_key=True)
    designation_name = db.Column(db.Text, nullable=False)
    abbreviation = db.Column(db.String(5), nullable=False)
    def __repr__(self):
        return f"<Designation(designation_id={self.designation_id}, designation_name='{self.designation_name}', abbreviation='{self.abbreviation}')>"



class Employee(db.Model):
    __tablename__ = 'employees'
    employee_id = db.Column(db.String(8), primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    notes = db.Column(JSONB)
    created = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated = db.Column(db.TIMESTAMP)


class EmployeeSession(db.Model):
    __tablename__ = 'employee_sessions'
    session_id = db.Column(db.String(36), primary_key=True)  # UUID for session ID
    employee_id = db.Column(db.String(8), db.ForeignKey('employees.employee_id'), nullable=False)
    created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expires = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(hours=4)) # 4 hour validity


class EmployeeClearance(db.Model):
    __tablename__ = 'employee_clearances'
    employee_id = db.Column(db.String(8), db.ForeignKey('employees.employee_id'), primary_key=True)
    clearance_id = db.Column(db.Integer, db.ForeignKey('clearances.clearance_id'), primary_key=True)


class EmployeeDesignation(db.Model):
    __tablename__ = 'employee_designations'
    employee_id = db.Column(db.String(8), db.ForeignKey('employees.employee_id'), primary_key=True)
    designation_id = db.Column(db.Integer, db.ForeignKey('designations.designation_id'), primary_key=True)


class EmployeeMedicalRecord(db.Model):
    __tablename__ = 'employee_medical_records'
    employee_id = db.Column(db.String(8), db.ForeignKey('employees.employee_id'), primary_key=True)
    dob = db.Column(db.Date)
    bloodtype = db.Column(db.String(10))
    sex = db.Column(db.String(10))
    kilograms = db.Column(db.Float)
    height_cm = db.Column(db.Float)
    notes = db.Column(JSONB)
    created = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated = db.Column(db.TIMESTAMP)



class EmployeeMission(db.Model):
    __tablename__ = 'employee_missions'
    employee_id = db.Column(db.String(8), db.ForeignKey('employees.employee_id'), primary_key=True)
    mission_id = db.Column(db.String(8), db.ForeignKey('missions.mission_id'), primary_key=True)
    involvement_summary = db.Column(db.Text)
    mission = db.relationship('Mission', back_populates='employee_missions', foreign_keys=[mission_id])


class DepartmentMission(db.Model):
    __tablename__ = 'department_missions'
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), primary_key=True)
    mission_id = db.Column(db.String(8), db.ForeignKey('missions.mission_id'), primary_key=True)
    mission = db.relationship('Mission', back_populates='department_missions', foreign_keys=[mission_id])


class Mission(db.Model):
    __tablename__ = 'missions'
    mission_id = db.Column(db.String(8), primary_key=True)
    mission_name = db.Column(db.Text, nullable=False, default='NAME-PENDING')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    commander_id = db.Column(db.String(8), db.ForeignKey('employees.employee_id'))
    supervisor_id = db.Column(db.String(8), db.ForeignKey('employees.employee_id'))
    description = db.Column(db.Text, nullable=False)
    notes = db.Column(JSONB)
    created = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated = db.Column(db.TIMESTAMP)

    employee_missions = db.relationship('EmployeeMission', back_populates='mission', foreign_keys=[EmployeeMission.mission_id])
    department_missions = db.relationship('DepartmentMission', back_populates='mission', foreign_keys=[DepartmentMission.mission_id])


class Origin(db.Model):
    __tablename__ = 'origins'
    origin_id = db.Column(db.String(8), primary_key=True)
    origin_name = db.Column(db.Text, nullable=False)
    discovery_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    notes = db.Column(JSONB)
    created = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated = db.Column(db.TIMESTAMP)


class MissionOrigin(db.Model):
    __tablename__ = 'mission_origins'
    mission_id = db.Column(db.String(8), db.ForeignKey('missions.mission_id'), primary_key=True)
    origin_id = db.Column(db.String(8), db.ForeignKey('origins.origin_id'), primary_key=True)


class Specimen(db.Model):
    __tablename__ = 'specimens'
    specimen_id = db.Column(db.String(8), primary_key=True)
    specimen_name = db.Column(db.Text, nullable=False)
    origin_id = db.Column(db.String(8), db.ForeignKey('origins.origin_id'))
    mission_id = db.Column(db.String(8), db.ForeignKey('missions.mission_id'))
    threat_level = db.Column(db.Float)
    acquisition_date = db.Column(db.Date, nullable=False)
    notes = db.Column(JSONB)
    description = db.Column(db.Text)
    created = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated = db.Column(db.TIMESTAMP)
    __table_args__ = (
        CheckConstraint('threat_level>=0 AND threat_level<=10'),
    )


class SpecimenContainmentStatus(db.Model):
    __tablename__ = 'specimen_containment_statuses'
    specimen_id = db.Column(db.String(8), db.ForeignKey('specimens.specimen_id'), primary_key=True)
    containment_status_id = db.Column(db.Integer, db.ForeignKey('containment_statuses.containment_status_id'), primary_key=True)


class SpecimenMedicalRecord(db.Model):
    __tablename__ = 'specimen_medical_records'
    specimen_id = db.Column(db.String(8), db.ForeignKey('specimens.specimen_id'), primary_key=True)
    bloodtype = db.Column(db.String(10))
    sex = db.Column(db.String(10))
    kilograms = db.Column(db.Float)
    notes = db.Column(JSONB)
    created = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated = db.Column(db.TIMESTAMP)
    __table_args__ = (
        CheckConstraint('kilograms>0'),
    )

class SpecimenMission(db.Model):
    __tablename__ = 'specimen_missions'
    specimen_id = db.Column(db.String(8), db.ForeignKey('specimens.specimen_id'), primary_key=True)
    mission_id = db.Column(db.String(8), db.ForeignKey('missions.mission_id'), primary_key=True)
    involvement_summary = db.Column(db.Text)


class Credential(db.Model):
    __tablename__ = 'credentials'
    employee_id = db.Column(db.String(8), db.ForeignKey('employees.employee_id'), primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    login_attempts = db.Column(db.Integer, default=0)
    created = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated = db.Column(db.TIMESTAMP)





class ResearcherSpecimen(db.Model):
    __tablename__ = 'researcher_specimens'
    employee_id = db.Column(db.String(8), db.ForeignKey('employees.employee_id'), primary_key=True)
    specimen_id = db.Column(db.String(8), db.ForeignKey('specimens.specimen_id'), primary_key=True)
