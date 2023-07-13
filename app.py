from flask import Flask, jsonify, request, render_template, sessions, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegistrationForm


app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///plantpal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

@app.route('/')
def index():
    """Show homepage"""
    return render_template('home.html')
    
@app.route('/user/register', methods = ['GET', 'POST'])
def register():
    """User Register Form"""

    form = RegistrationForm()




    