from dataclasses import field
from sqlalchemy import join, select
from functools import lru_cache
from graphql.execution.base import ResolveInfo
from graphql import GraphQLNonNull, GraphQLObjectType

TABLE_PERMISSIONS = {
    "departmenttype": {
        "read": ["departments:table:read", "departments:table:read_write"],
        "write": ["departments:table:read_write"]
    },
    "documents": {
        "read": ["documents:table:read", "documents:table:read_write"],
        "write": ["documents:table:read_write"]
    },
    "employee_designations": {
        "read": ["employee_designations:table:read_write"],
        "write": ["employee_designations:table:read_write"]
    },
    "employeemedicalrecordtype": {
        "read": ["employee_medical_records:table:read_write"],
        "write": ["employee_medical_records:table:read_write"]
    },
    "employeemissiontype": {
        "read": ["employee_missions:table:read_write"],
        "write": ["employee_missions:table:read_write"]
    },
    "employee_sessions": {
        "read": ["employee_sessions:table:read", "employee_sessions:table:read_write"],
        "write": ["employee_sessions:table:read_write"]
    },
    "employeetype": {
        "read": ["employees:table:read", "employees:table:read_write"],
        "write": ["employees:table:read_write"]
    },
    "missiontype": {
        "read": ["missions:table:read", "missions:table:read_write"],
        "write": ["missions:table:read_write"]
    },
    "missionorigintype": {
        "read": ["mission_origins:table:read_write"],
        "write": ["mission_origins:table:read_write"]
    },
    "origintype": {
        "read": ["origins:table:read", "origins:table:read_write"],
        "write": ["origins:table:read_write"]
    },
    "researcherspecimentype": {
        "read": ["researcher_specimens:table:read_write"],
        "write": ["researcher_specimens:table:read_write"]
    },
    "specimencontainmentstatustype": {
        "read": ["specimen_containment_statuses:table:read_write"],
        "write": ["specimen_containment_statuses:table:read_write"]
    },
    "specimenmedicalrecordtype": {
        "read": ["specimen_medical_records:table:read_write"],
        "write": ["specimen_medical_records:table:read_write"]
    },
    "specimenmissiontype": {
        "read": ["specimen_missions:table:read_write"],
        "write": ["specimen_missions:table:read_write"]
    },
    "specimentype": {
        "read": ["specimens:table:read_write"],
        "write": ["specimens:table:read_write"]
    }
}

FIELD_PERMISSIONS = {
    "notes": {
        "read": ["employee_notes:column:read", "employee_notes:column:read_write"],
        "write": ["employee_notes:column:read_write"]
    },
    "passwords": {
        "read": ["passwords:column:read_write"],
        "write": ["passwords:column:read_write"]
    },
    "specimen_threat_level": {
        "read": ["specimen_threat_level:column:read_write"],
        "write": ["specimen_threat_level:column:read_write"]
    }
}



class PermissionsMiddleware:
    def resolve(self, next, root, info: ResolveInfo, **args):
        field_name = info.field_name
        parent_type = info.parent_type.name.lower()
        operation_type = info.operation.operation

        # Extract or create the cache for this request
        request = info.context
        if not hasattr(request, 'permission_cache'):
            request.permission_cache = {}
        if not hasattr(request, 'access_denied_fields'):
            request.access_denied_fields = {}

        cache_key = (field_name, parent_type, operation_type)
        if cache_key in request.permission_cache:
            if not request.permission_cache[cache_key]:
                return self.handle_access_denied(info, request, parent_type, field_name)
            return next(root, info, **args)

        employee_id = extract_employee_id(info)
        employee_permissions = get_employee_permissions_cached(employee_id)

        # Determine the required permissions based on the operation type
        required_permission_type = 'read' if operation_type == 'query' else 'write'

        # Check table-level permissions
        if parent_type in TABLE_PERMISSIONS:
            required_permissions = TABLE_PERMISSIONS[parent_type].get(required_permission_type, [])
            if not any(permission in employee_permissions for permission in required_permissions):
                request.permission_cache[cache_key] = False
                return self.handle_access_denied(info, request, parent_type, field_name)

        # Check field-level permissions
        if field_name in FIELD_PERMISSIONS:
            required_permissions = FIELD_PERMISSIONS[field_name].get(required_permission_type, [])
            if not any(permission in employee_permissions for permission in required_permissions):
                request.permission_cache[cache_key] = False
                return self.handle_access_denied(info, request, parent_type, field_name)

        # Store the result in the cache
        request.permission_cache[cache_key] = True

        return next(root, info, **args)

    def handle_access_denied(self, info, request, parent_type, field_name):
        if parent_type not in request.access_denied_fields:
            request.access_denied_fields[parent_type] = []
        request.access_denied_fields[parent_type].append(field_name)
        
        # Handle non-nullable field gracefully by returning a default value
        field_type = info.return_type
        if isinstance(field_type, GraphQLNonNull):
            field_type = field_type.of_type  # Get the underlying type

        # Check if it's a custom GraphQL object
        if isinstance(field_type, GraphQLObjectType):
            return self.create_placeholder_object(field_type)

        # Determine a default value based on the type
        if field_type.name == 'String':
            return "Access Denied"
        elif field_type.name == 'Int':
            return -1  # or any other placeholder value
        elif field_type.name == 'Float':
            return -1.0  # or any other placeholder value
        elif field_type.name == 'Boolean':
            return False  # or any other placeholder value
        else:
            return None
    
    def create_placeholder_object(self, object_type):
        placeholder = {}
        for field_name, field in object_type.fields.items():
            field_type = field.type
            if isinstance(field_type, GraphQLNonNull):
                field_type = field_type.of_type  # Get the underlying type

            if field_type.name == 'String':
                placeholder[field_name] = "Access Denied"
            elif field_type.name == 'Int':
                placeholder[field_name] = -1
            elif field_type.name == 'Float':
                placeholder[field_name] = -1.0
            elif field_type.name == 'Boolean':
                placeholder[field_name] = False
            else:
                placeholder[field_name] = None
        return placeholder

@lru_cache(maxsize=128)
def get_employee_permissions_cached(employee_id):
    return get_employee_permissions(employee_id)

def get_employee_permissions(employee_id):
    from ..models.sqlalchemy_models import EmployeeClearance, Resource, ClearanceResourceAccess as CRA
    from ..resources.config import engine

    user_clearance_ids = [c.clearance_id for c in EmployeeClearance.query.filter_by(employee_id=employee_id).all()]
    with engine.connect() as connection:
        j = join(CRA, Resource, CRA.resource_id == Resource.resource_id)
        query = select([Resource.resource_name, Resource.resource_type, CRA.access_type]).select_from(j).where(CRA.clearance_id.in_(user_clearance_ids))
        result = connection.execute(query)
        return {":".join([r.resource_name, r.resource_type, r.access_type]) for r in result}

def extract_employee_id(info):
    request = info.context
    if not request:
        raise Exception('Request context not found')

    employee_id = request.headers.get('x-employee-id')
    if not employee_id:
        raise Exception('Employee ID not found in context')

    return employee_id