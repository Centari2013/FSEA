from .config import *
from ..models.sqlalchemy_models import Credential, EmployeeSession
from werkzeug.security import generate_password_hash as hash_password, check_password_hash as verify_password
from datetime import datetime, timezone
from uuid import uuid4

class CredentialType(SQLAlchemyObjectType):
    class Meta:
        model = Credential
        interfaces = (graphene.relay.Node,)

class EmployeeSessionType(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeSession
        interfaces = (graphene.relay.Node,)

class UpdateCredentials(graphene.Mutation):
    class Arguments:
        employee_id = graphene.Int(required=True)
        username = graphene.String()
        password = graphene.String()
        login_attempts = graphene.Int()

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, employee_id, username=None, password=None, login_attempts=None):
        credentials = Credential.query.get(employee_id)
        if not credentials:
            return UpdateCredentials(success=False, message="Credentials not found")

        if username:
            credentials.username = username
        if password:
            credentials.password = hash_password(password)
        if login_attempts is not None:
            credentials.login_attempts = login_attempts

        try:
            credentials.updated = db.func.current_timestamp()
            db.session.commit()
            return UpdateCredentials(success=True, message="Credentials updated successfully")
        except Exception as e:
            db.session.rollback()
            return UpdateCredentials(success=False, message=f"Failed to update credentials. Error: {str(e)}")

class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        employee_id = graphene.String(required=False)

    token = graphene.String()
    message = graphene.String()
    employee_id = graphene.String()

    def mutate(self, info, username, password):
        user = Credential.query.filter_by(username=username).first()
        if user and verify_password(user.password, password):
            if user.login_attempts < 3:
                user.login_attempts = 0
                db.session.commit()
                new_session = EmployeeSession(session_id=str(uuid4()), employee_id=user.employee_id)
                db.session.add(new_session)
                db.session.commit()
                return Login(token=new_session.session_id, message="Login successful.", employee_id=user.employee_id)
            else:
                return Login(message="Account locked. Contact admin.")
        else:
            if user:
                user.login_attempts += 1
                db.session.commit()
            return Login(message="Invalid credentials")

class ValidateToken(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)

    valid = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, token):
        session = EmployeeSession.query.filter_by(session_id=token).first()
        if session and session.expires > datetime.now(tz=timezone.utc):
            return ValidateToken(valid=True, message="Token is valid.")
        else:
            return ValidateToken(valid=False, message="Invalid or expired token")

class AuthQuery(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    validate_token = graphene.Field(ValidateToken, token=graphene.String(required=True))

class AuthMutation(graphene.ObjectType):
    update_credentials = UpdateCredentials.Field()
    login = Login.Field()
    validate_token = ValidateToken.Field()

