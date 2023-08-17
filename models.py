"""Models for CookingBuddy app."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy, Pagination

bcrypt = Bcrypt()
db = SQLAlchemy()

###DO NOT MODIFY##     

def connect_db(app):
    """Connect to database"""

    db.app = app 
    db.init_app(app)


DEFAULT_IMAGE = "/static/default_image.png"

class User(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(100))
    display_name = db.Column(db.String(50))
    img_url = db.Column(db.String(200), default = DEFAULT_IMAGE)

    favorites = db.relationship('Recipe', secondary='user_recipe_favorites', backref='users')

    def __repr__(self):
        return f"<User {self.username}>"

    @classmethod
    def register(cls, display_name, username, password):
        """Registers user. Hashes password and adds user to system"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(
            display_name = display_name,
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

class Recipe(db.Model):
    """Recipe Model."""

    __tablename__ = "recipes"

    recipe_api_id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    default_image= db.Column(db.String())
    ingredients = db.Column(db.String())
    instructions = db.Column(db.String())

    # Define the relationship with UserFavorite model
    favorites = db.relationship('UserFavorite', backref='recipe')


class UserFavorite(db.Model):
    """Favorites Recipes of User"""

    __tablename__= "user_recipe_favorites"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_api_id', ondelete='CASCADE'), nullable=False)

