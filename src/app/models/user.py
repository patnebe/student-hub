from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature,  SignatureExpired)
from src.app.models.base import Base
from flask_login import UserMixin
from src.app import db, login



class User(UserMixin, Base):
    __tablename__ = 'auth_user'

    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)

    # Identification data
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(192), nullable=False)

    # Authorization data
    # role = db.Column(db.SmallInteger, nullable=False)
    # status = db.Column(db.SmallInteger, nullable=False)

    # Initialization procedure for new instances
    # def __init__(self, first_name, last_name, email, password):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.email = email
    #     self.password_hash = password_hash

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    
    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return s.dumps({'id': self.id})

    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        
        try:
            data = s.loads(token)
            user = User.query.get(data['id'])
            return user
        
        except SignatureExpired:
            return None
        
        except BadSignature:
            return None


    def __repr__(self):
        return f'<User {self.first_name} {self.email}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))