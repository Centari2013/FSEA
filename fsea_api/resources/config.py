from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import strawberry
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper

mapper = StrawberrySQLAlchemyMapper()

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URI"))
SessionLocal = sessionmaker(bind=engine)

from .access_control import has_permission, has_permissions_and, has_permissions_or
from .. import db  