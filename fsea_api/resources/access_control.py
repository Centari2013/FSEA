from .config import *
from functools import wraps
from sqlalchemy import join, select
from ..models.sqlalchemy_models import EmployeeClearance, Resource, ClearanceResourceAccess as CRA

'''
When employee tries to access table:
- Use their employeeID to get all of their clearances.
- Use those clearanceIDs to get resource names and access types.
- If the resource name and access type matches the user's actions, then send raw data, otherwise disallow/redact.

'''

def getEmployeePermissions(info):
    request = info.context
    
    if request:
        employee_id = request.headers.get('employee_id')
     
        if not employee_id:
            raise Exception('Employee ID not found in headers', request.headers)
    if employee_id.is_anonymous:
        raise Exception('Authentication credentials were not provided')
    
    # Retrieve clearance_ids for the given employee_id
    user_clearance_ids = EmployeeClearance.query.filter_by(employee_id=employee_id).all()
    user_clearance_ids = [id_ for id_, in user_clearance_ids] 

    with engine.connect() as connection:
        # Create a join query
        j = join(CRA, Resource, CRA.resource_id == Resource.id)
        query = select([Resource.resource_name, CRA.resource_type, Resource.access_type]).select_from(j).where(CRA.clearance_id.in_(user_clearance_ids))
        result = connection.execute(query)
        return [":".join([r[0],r[1],r[2]]) for r in result]

def has_permission(info, permission_name):
    permissions = getEmployeePermissions(info)
    return permissions is not None and permission_name in permissions
       

def has_permissions_and(info, *permission_names):
    permissions = getEmployeePermissions(info)
    return permissions is not None and all(permission_name in permissions for permission_name in permission_names)
            

def has_permissions_or(info, *permission_names):
    permissions = getEmployeePermissions(info)
    return permissions is not None and any(permission_name in permissions for permission_name in permission_names)
    


'''possible_permissions = [
    #"credentials:table:read_write",
    "departments:table:read",
    "departments:table:read_write",
    "designations:table:read_write",
    "documents:table:read",
    "documents:table:read",
    "documents:table:read_write",
    "employee_designations:table:read_write",
    "employee_medical_records:table:read_write",
    "employee_medical_records:table:write",
    "employee_missions:table:read_write",
    "employee_notes:column:read_write",
    "employee_sessions:table:read",
    "employee_sessions:table:read_write",
    "employees:table:read",
    "employees:table:read",
    "employees:table:read_write",
    "missions:table:read",
    "missions:table:read_write",
    "mission_origins:table:read_write",
    "origins:table:read",
    "origins:table:read_write",
    "passwords:column:read_write",
    "researcher_specimens:table:read_write",
    "specimen_containment_statuses:table:read_write",
    "specimen_medical_records:table:read_write",
    "specimen_missions:table:read_write",
    "specimens:table:read_write",
    "specimens:table:read_write",
    "specimen_threat_level:column:read_write"
]
'''