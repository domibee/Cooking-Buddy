"""Models for PlantPal app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(100))
    
    def __repr__(self):
        return f"<User {self.username}>"


###DO NOT MODIFY##     

def connect_db(app):
    """Connect to database"""

    db.app = app 
    db.init_app(app)