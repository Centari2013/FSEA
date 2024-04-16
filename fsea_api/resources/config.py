import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

engine = create_engine(os.getenv("DATABASE_URI"))
from .. import db  