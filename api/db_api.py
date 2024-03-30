from flask import Flask
from flask_restful import Api, Resource
from psycopg2 import connect, extensions, sql
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Flask and Flask-RESTful API
app = Flask(__name__)
api = Api(app)

# Database connection parameters
db_params = {
    "database": os.getenv("DATABASE_NAME"),
    "user": os.getenv("DATABASE_USER"),
    "password": os.getenv("DATABASE_PASSWORD"),
    "host": os.getenv("DATABASE_HOST"),
    "port": os.getenv("DATABASE_PORT")
}

# Example Resource
class Employee(Resource):
    def get(self, employee_id):
        # Connect to the database
        conn = connect(**db_params)
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Execute a query
        cur.execute(sql.SQL("SELECT * FROM employees WHERE employee_id = %s"), (employee_id,))
        
        # Fetch one result
        employee = cur.fetchone()
        cur.close()
        conn.close()
        
        if employee:
            return {"employee": employee}, 200
        return {"message": "Employee not found"}, 404

# Add the resource to the API
api.add_resource(Employee, '/employees/<string:employee_id>')

if __name__ == "__main__":
    app.run(debug=True)
