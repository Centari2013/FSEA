from uuid import uuid4

from flask import jsonify
from .imports import *
from ..models.sqlalchemy_models import Credential, EmployeeSession
from werkzeug.security import generate_password_hash as hash_password, check_password_hash as verify_password





class UpdateCredentials(Resource):
    def patch(self, employee_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, store_missing=False)
        parser.add_argument('password', type=str, store_missing=False)
        parser.add_argument('login_attempts', type=int, store_missing=False)
        data = parser.parse_args()

        credentials = Credential.query.get(employee_id)
        if not credentials:
            return {'message': 'Credentials not found'}, 404

        if 'username' in data:
            credentials.username = data['username']
        if 'password' in data:
            credentials.password = hash_password(data['password'])
        if 'login_attempts' in data:
            credentials.login_attempts = data['login_attempts']

        try:
            credentials.updated = db.func.current_timestamp()
            db.session.commit()
            return {'message': 'Credentials updated successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Failed to update credentials. Error: {str(e)}'}, 500


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username cannot be blank.")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank.")
        data = parser.parse_args()

        # Assuming the Credential model has a username field
        user = Credential.query.filter_by(username=data['username']).first()
        print(user.password)
        if user:
            if verify_password(user.password, data['password']):
                if user.login_attempts < 3:
                    user.login_attempts = 0
                    db.session.commit()
                    # User is authenticated; create a session
                    new_session = EmployeeSession(
                        session_id=str(uuid4()),
                        employee_id=user.employee_id
                    )
                    db.session.add(new_session)
                    db.session.commit()

                    # Return the session ID as the token
                    return jsonify({'token': new_session.session_id})
                else:
                    return {'message': 'Account Locked. Contact admin.'}, 429
            else:
                user.login_attempts += 1
                db.session.commit()
                return {'message': 'Invalid credentials'}, 401

        else:
            return {'message': 'Invalid credentials'}, 401
        
        #E7449700