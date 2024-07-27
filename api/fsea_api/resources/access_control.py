from .config import *
from functools import wraps
from sqlalchemy import join, select
from ..models.sqlalchemy_models import EmployeeClearance, Resource, ClearanceResourceAccess as CRA

def getEmployeePermissions(info):
    request = info.context
    if request:
        employee_id = request.headers.get('x-employee-id')
     
        if not employee_id:
            raise Exception('Employee ID not found in context')
    if employee_id is None:
        raise Exception('Authentication credentials were not provided')
    
    # Retrieve clearance_ids for the given employee_id
    user_clearance_ids = [c.clearance_id for c in EmployeeClearance.query.filter_by(employee_id=employee_id).all()]
    

    with engine.connect() as connection:
        # Create a join query
        j = join(CRA, Resource, CRA.resource_id == Resource.resource_id)
        query = select([Resource.resource_name, Resource.resource_type, CRA.access_type]).select_from(j).where(CRA.clearance_id.in_(user_clearance_ids))
        result = connection.execute(query)
        return [":".join([r[0],r[1],r[2]]) for r in result]

def has_permission(permission_name):
    def decorator(func):
        @wraps(func)
        def wrapper(root, info, *args, **kwargs):
            
            if permission_name not in getEmployeePermissions(info):
                raise Exception('You do not have permission to perform this action')
            return func(root, info, *args, **kwargs)
        return wrapper
    return decorator

def has_permissions_and(*permission_names):
    def decorator(func):
        @wraps(func)
        def wrapper(root, info, *args, **kwargs):
            for permission_name in permission_names:
                if permission_name not in getEmployeePermissions(info):
                    raise Exception(f'You do not have permission to perform this action: {permission_name}')
            return func(root, info, *args, **kwargs)
        return wrapper
    return decorator

def has_permissions_or(*permission_names):
    def decorator(func):
        @wraps(func)
        def wrapper(root, info, *args, **kwargs):
            if not any(permission_name in getEmployeePermissions(info) for permission_name in permission_names):
                raise Exception('You do not have any of the required permissions to perform this action')
            return func(root, info, *args, **kwargs)
        return wrapper
    return decorator


possible_permissions = [
    "credentials:table:read_write",
    "departments:table:read",
    "departments:table:read_write",
    "designations:table:read_write",
    "documents:table:read",
    "documents:table:read_write",
    "employee_designations:table:read_write",
    "employee_medical_records:table:read_write",
    "employee_missions:table:read_write",
    "employee_notes:column:read_write",
    "employee_sessions:table:read",
    "employee_sessions:table:read_write",
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
    "specimen_threat_level:column:read_write"
]
