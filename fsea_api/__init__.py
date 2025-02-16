from flask import Flask, Response
from strawberry.flask.views import GraphQLView
import graphdoc
from flask_cors import CORS
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True, expose_headers=['Content-Type'], logs=True)

from .schema import schema 
# Set up the GraphQL endpoint


@app.route('/api/graphql', methods=['GET', 'POST'])
def graphql_server():
    view = GraphQLView.as_view('graphql', schema=schema)
    return view()

@app.route('/api/docs')
def graphql_docs():
    # Generate HTML documentation
    html = graphdoc.to_doc(schema)
    return Response(html, content_type='text/html')

@app.route('/ping')
def ping_api():
    return Response("pong", 200)