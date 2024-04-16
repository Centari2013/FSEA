import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import create_engine, text
from datetime import datetime
from ..models.sqlalchemy_models import Employee, Department, Origin, Mission, Specimen

# Setup SQLAlchemy connection (update with your actual database URI)
engine = create_engine('postgresql://username:password@localhost/mydatabase')

class EmployeeType(SQLAlchemyObjectType):
    class Meta:
        model = Employee

class DepartmentType(SQLAlchemyObjectType):
    class Meta:
        model = Department

class OriginType(SQLAlchemyObjectType):
    class Meta:
        model = Origin

class MissionType(SQLAlchemyObjectType):
    class Meta:
        model = Mission

class SpecimenType(SQLAlchemyObjectType):
    class Meta:
        model = Specimen

class SearchResult(graphene.ObjectType):
    entity_type = graphene.String()
    data = graphene.JSONString()
    relevancy = graphene.Float()

def format_tsquery(search_input):
    tokens = search_input.split()
    escaped_tokens = [token.replace("'", "''") for token in tokens]
    return ' & '.join(escaped_tokens)

def perform_search(sql_query, query_param):
    with engine.connect() as connection:
        sql = text(sql_query)
        result = connection.execute(sql, {'query': query_param}).mappings().all()
    return result

class Search(graphene.Mutation):
    class Arguments:
        query = graphene.String(required=True)

    results = graphene.List(SearchResult)

    def mutate(self, info, query):
        formatted_query = format_tsquery(query)

        # Define your search SQL commands
        search_commands = {
            'employee': ("SELECT * FROM search_employee_details(:query)", EmployeeType),
            'department': ("SELECT * FROM search_department_details(:query)", DepartmentType),
            'origin': ("SELECT * FROM search_origin_details(:query)", OriginType),
            'mission': ("SELECT * FROM search_mission_details(:query)", MissionType),
            'specimen': ("SELECT * FROM search_specimen_details(:query)", SpecimenType),
        }

        results = []
        for key, (sql, gtype) in search_commands.items():
            for row in perform_search(sql, formatted_query):
                # Convert SQLAlchemy results to JSON-like data, assuming SQLAlchemy model fields match the dict keys
                data = {field: getattr(row, field, None) for field in row._fields}
                # Handle special types like dates
                if 'discovery_date' in data and data['discovery_date']:
                    data['discovery_date'] = data['discovery_date'].isoformat()
                if 'start_date' in data and data['start_date']:
                    data['start_date'] = data['start_date'].isoformat()
                if 'end_date' in data and data['end_date']:
                    data['end_date'] = data['end_date'].isoformat()

                results.append(SearchResult(entity_type=key, data=data, relevancy=row.get('relevancy', 0)))

        return Search(results=results)

class SearchMutation(graphene.ObjectType):
    search = Search.Field()


