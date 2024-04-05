from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from .. import db  
from dotenv import load_dotenv
import os


load_dotenv()

engine = create_engine(os.getenv("DATABASE_URI"))