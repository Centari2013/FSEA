import graphene
import json
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URI"))


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
        result = connection.execute(sql, {'query': query_param}).all()
    return result


class Search(graphene.Mutation):
    class Arguments:
        query = graphene.String(required=True)

    results = graphene.List(SearchResult)

    def mutate(self, info, query):
        formatted_query = format_tsquery(query)
        search_commands = {
            'E': "SELECT * FROM search_employee_details(:query)",
            'D': "SELECT * FROM search_department_details(:query)",
            'O': "SELECT * FROM search_origin_details(:query)",
            'M': "SELECT * FROM search_mission_details(:query)",
            'S': "SELECT * FROM search_specimen_details(:query)"
        }

        results = []
        seen_ids = set()  # 🔥 Track unique ID combinations

        for key, sql in search_commands.items():
            for row in perform_search(sql, formatted_query):
                data = dict(row)  # Convert row to dictionary
                
                # Process dates into ISO format
                for date_field in ['discovery_date', 'start_date', 'end_date', 'acquisition_date']:
                    if date_field in data and data[date_field]:
                        data[date_field] = data[date_field].isoformat()

                # 🔥 Extract all `_id` fields into a tuple
                id_tuple = tuple(data[field] for field in data if field.endswith("_id"))

                if id_tuple and id_tuple not in seen_ids:
                    seen_ids.add(id_tuple)  # Store unique ID tuple
                    results.append(SearchResult(entity_type=key, data=data, relevancy=row['relevancy']))

        # 🔥 Sorting priority
        type_priority = {'D': 1, 'E': 2, 'O': 3, 'M': 4, 'S': 5}
        results = sorted(results, key=lambda x: (type_priority[x.entity_type], -x.relevancy))  # Highest relevancy first
        
        return Search(results=results)


class SearchMutation(graphene.ObjectType):
    search = Search.Field()
