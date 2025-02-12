import graphene
import json
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

from .access_control import has_permissions_or

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URI"))

# Import permission functions
class SearchResult(graphene.ObjectType):
    entity_type = graphene.String()
    data = graphene.JSONString()
    relevancy = graphene.Float()


def format_tsquery(search_input):
    tokens = search_input.split()
    escaped_tokens = [token.replace("'", "''") for token in tokens]
    return ' & '.join(escaped_tokens)


def perform_search(info, sql_query, e_type, query_param, *permissions):
    """Runs a search query if the user has permission."""
    '''if not has_permissions_or(info, *permissions):
        return []  # No access, return an empty list'''

    with engine.connect() as connection:
        sql = text(sql_query)
        result = connection.execute(sql, {'query': query_param}).all()
    
    # Convert results into dictionaries & format dates
    formatted_results = []
    for row in result:
        data = dict(row)
        
        # Convert date fields to ISO format
        for date_field in ['discovery_date', 'start_date', 'end_date', 'acquisition_date']:
            if date_field in data and data[date_field]:
                data[date_field] = data[date_field].isoformat()
        
        formatted_results.append(SearchResult(entity_type=e_type, data=data, relevancy=row['relevancy']))

    return formatted_results


# 🚀 **Individual Search Functions with Permission Checks**
def search_employees(info, query):
    return perform_search(info, "SELECT * FROM search_employee_details(:query)", "E", query, "employees:table:read", "employees:table:read_write")


def search_departments(info, query):
    return perform_search(info, "SELECT * FROM search_department_details(:query)", "D", query, "departments:table:read", "departments:table:read")


def search_origins(info, query):
    return perform_search(info, "SELECT * FROM search_origin_details(:query)", "O", query, "origins:table:read", "origins:table:read_write")


def search_missions(info, query):
    return perform_search(info, "SELECT * FROM search_mission_details(:query)", "M", query, "missions:table:read", "missions:table:read_write")


def search_specimens(info, query):
    return perform_search(info, "SELECT * FROM search_specimen_details(:query)", "S", query, "specimens:table:read", "specimens:table:read_write")


# 🚀 **GraphQL Mutation with Permission Checks**
class Search(graphene.Mutation):
    class Arguments:
        query = graphene.String(required=True)

    results = graphene.List(SearchResult)

    def mutate(self, info, query):
        formatted_query = format_tsquery(query)

        results = []
        results.extend(search_employees(info, formatted_query))
        results.extend(search_departments(info, formatted_query))
        results.extend(search_origins(info, formatted_query))
        results.extend(search_missions(info, formatted_query))
        results.extend(search_specimens(info, formatted_query))

        # Define type priority
        type_priority = {'D': 1, 'E': 2, 'O': 3, 'M': 4, 'S': 5}

        # Weights for sorting
        RELEVANCY_WEIGHT = 0.6
        TYPE_PRIORITY_WEIGHT = 0.3  

        def combined_score(result):
            relevancy = (result.relevancy if result.relevancy is not None else 0) * RELEVANCY_WEIGHT
            type_penalty = type_priority.get(result.entity_type, 100) * TYPE_PRIORITY_WEIGHT
            return relevancy - type_penalty

        results = sorted(results, key=combined_score)

        return Search(results=results)


class SearchMutation(graphene.ObjectType):
    search = Search.Field()
