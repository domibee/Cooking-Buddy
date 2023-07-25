"""Models for PlantPal app."""

from flask_bcrypt import Bcrypt, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

###DO NOT MODIFY##     

def connect_db(app):
    """Connect to database"""

    db.app = app 
    db.init_app(app)

class User(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(100))
    
    def __repr__(self):
        return f"<User {self.username}>"

    @classmethod
    def register(cls, username, password):
        """Registers user. Hashes password and adds user to system"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(
            username = username,
            password = hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """FInd a user name with `username` and `password`
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


