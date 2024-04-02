from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
db = SQLAlchemy(app)
api = Api(app)


from fsea_api.resources import *
api.add_resource(PostClearance, '/clearances')
api.add_resource(GetClearance, '/clearances/<int:clearance_id>')
api.add_resource(PatchClearance, '/clearances/<int:clearance_id>')
api.add_resource(DeleteClearance, '/clearances/<int:clearance_id>')

api.add_resource(PostContainmentStatus, '/containment_statuses')
api.add_resource(GetContainmentStatus, '/containment_statuses/<int:containment_status_id>')
api.add_resource(PatchContainmentStatus, '/containment_statuses/<int:containment_status_id>')
api.add_resource(DeleteContainmentStatus, '/containment_statuses/<int:containment_status_id>')

api.add_resource(PostDepartment, '/departments')
api.add_resource(GetDepartment, '/departments/<int:department_id>')
api.add_resource(PatchDepartment, '/departments/<int:department_id>')
api.add_resource(DeleteDepartment, '/departments/<int:department_id>')

api.add_resource(PostDesignation, '/designations')
api.add_resource(GetDesignation, '/designations/<int:designation_id>')
api.add_resource(PatchDesignation, '/designations/<int:designation_id>')
api.add_resource(DeleteDesignation, '/designations/<int:designation_id>')



