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
        for key, sql in search_commands.items():
            for row in perform_search(sql, formatted_query):
                data = dict(row)  # Convert row to a dictionary directly
                # Process dates and other types as needed
                for date_field in ['discovery_date', 'start_date', 'end_date', 'acquisition_date']:
                    if date_field in data and data[date_field]:
                        data[date_field] = data[date_field].isoformat()
                
                results.append(SearchResult(entity_type=key, data=data, relevancy=row['relevancy']))
        # Define your type priority mapping
        type_priority = {'D': 1, 'E': 2, 'O': 3, 'M': 4, 'S': 5}

        # Set up some weights — adjust these until your results stop looking like a shitshow.
        RELEVANCY_WEIGHT = 1.0
        TYPE_PRIORITY_WEIGHT = 0.3  # Adjust this to balance type priority influence

        def combined_score(result):
            # Multiply relevancy by its weight
            relevancy = (result.relevancy if result.relevancy is not None else 0) * RELEVANCY_WEIGHT
            # Apply type penalty based on type priority
            type_penalty = type_priority.get(result.entity_type, 100) * TYPE_PRIORITY_WEIGHT
            return relevancy - type_penalty

        # Now sort your results by this unified combined score (higher score first)
        results = sorted(results, key=combined_score, reverse=True)

        return Search(results=results)

class SearchMutation(graphene.ObjectType):
    search = Search.Field()
