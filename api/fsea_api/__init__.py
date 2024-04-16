from flask import Flask, Response
from flask_graphql import GraphQLView
import graphdoc
from flask_cors import CORS
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from .schema import schema 
# Set up the GraphQL endpoint
app.add_url_rule(
    '/api/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Set to False in production
    )
)

@app.route('/api/docs')
def graphql_docs():
    # Generate HTML documentation
    html = graphdoc.to_doc(schema)
    return Response(html, content_type='text/html')