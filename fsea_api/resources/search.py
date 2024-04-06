from .imports import *
from sqlalchemy import text


def format_tsquery(search_input):
    """
    Takes a user input string intended for search, tokenizes it,
    and formats it as a tsquery string for PostgreSQL.
    """
    tokens = search_input.split()
    
    # Escape single quotes (basic SQL injection prevention)
    escaped_tokens = [token.replace("'", "''") for token in tokens]
    
    # Join tokens with the '&' operator for tsquery
    tsquery = ' & '.join(escaped_tokens)
    
    # Return the formatted tsquery string
    return tsquery


# Assuming 'engine' is already created and imported from your configuration

def search_employee_details(search_query):
    with engine.connect() as connection:
        sql = text("SELECT * FROM search_employee_details(:query)")
        result = connection.execute(sql, {'query': search_query}).mappings().all()
    return [{
            'employee_id': row['employee_id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'department': row['department'],
            'designations': row['designations'],
            'relevancy': row['relevancy']
        } for row in result]

def search_department_details(search_query):
    with engine.connect() as connection:
        sql = text("SELECT * FROM search_department_details(:query)")
        result = connection.execute(sql, {'query': search_query}).mappings().all()
    return [{
        'department_id': row['department_id'],
        'department_name': row['department_name'],
        'director': row['director'],
        'description': row['description'],
        'relevancy': row['relevancy']
    } for row in result]

def search_origin_details(search_query):
    with engine.connect() as connection:
        sql = text("SELECT * FROM search_origin_details(:query)")
        result = connection.execute(sql, {'query': search_query}).mappings().all()
    return [{
        'origin_id': row['origin_id'],
        'origin_name': row['origin_name'],
        'discovery_date': row['discovery_date'].isoformat() if row['discovery_date'] else None,
        'description': row['description'],
        'relevancy': row['relevancy']
    } for row in result]

def search_mission_details(search_query):
    with engine.connect() as connection:
        sql = text("SELECT * FROM search_mission_details(:query)")
        result = connection.execute(sql, {'query': search_query}).mappings().all()
    return [{
        'mission_id': row['mission_id'],
        'mission_name': row['mission_name'],
        'start_date': row['start_date'].isoformat() if row['start_date'] else None,
        'end_date': row['end_date'].isoformat() if row['end_date'] else None,
        'description': row['description'],
        'relevancy': row['relevancy']
    } for row in result]

def search_specimen_details(search_query):
    with engine.connect() as connection:
        sql = text("SELECT * FROM search_specimen_details(:query)")
        result = connection.execute(sql, {'query': search_query}).mappings().all()
    return [{
        'specimen_id': row['specimen_id'],
        'specimen_name': row['specimen_name'],
        'threat_level': row['threat_level'],
        'acquisition_date': row['acquisition_date'].isoformat() if row['acquisition_date'] else None,
        'relevancy': row['relevancy']
    } for row in result]

   

def sort_and_consolidate_results(results):
    # Step 1: Fill relevancy_temp with all relevancy values for each ID
    relevancy_temp = {}
    for r in results:
        id_key = next((key for key in r if key.endswith('_id')), None)
        if id_key:
            id_value = r[id_key]
            relevancy_temp.setdefault(id_value, []).append(r['relevancy'])
    
    # Step 2: Remove duplicates from results based on unique IDs
    seen_ids = set()
    unique_results = []
    for r in results:
        id_key = next((key for key in r if key.endswith('_id')), None)
        if id_key:
            id_value = r[id_key]
            if id_value not in seen_ids:
                unique_results.append(r)
                seen_ids.add(id_value)
    
    # Step 3: Fill consolidated_results using the de-duplicated list and relevancy_temp
    consolidated_results = []
    for r in unique_results:
        id_key = next((key for key in r if key.endswith('_id')), None)
        if id_key:
            id_value = r[id_key]
            avg_relevancy = sum(relevancy_temp[id_value]) / len(relevancy_temp[id_value])
            # Create a new dictionary for the consolidated result
            new_entry = r.copy()
            new_entry['relevancy'] = avg_relevancy
            consolidated_results.append(new_entry)

    return sorted(consolidated_results, key=lambda x: x['relevancy']) # sort by relevancy


class SearchAllDetails(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str, required=True, help="Search query cannot be blank.")
        args = parser.parse_args()

        search_query = format_tsquery(args['query'])

        try:
            employees = search_employee_details(search_query)
            departments = search_department_details(search_query)
            origins = search_origin_details(search_query)
            missions = search_mission_details(search_query)
            specimens = search_specimen_details(search_query)

            for employee in employees:
                employee['type'] = 'E'  # E for Employee

            for department in departments:
                department['type'] = 'D'  # D for Department

            for origin in origins:
                origin['type'] = 'O'  # O for Origin

            for mission in missions:
                mission['type'] = 'M'  # M for Mission

            for specimen in specimens:
                specimen['type'] = 'S'  # S for Specimen
                        
            raw_results = employees + departments + origins + missions + specimens

            sorted_results = sort_and_consolidate_results(raw_results)

            if sorted_results:
                return {'results': sorted_results}, 200
            else:
                return {'message': 'No results found for the given search query.'}, 404
            
        except Exception as e:
            print(e)
            return {'message': f'Query failed. Error: {str(e)}'}, 500
                


        
        