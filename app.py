import os 

from flask import Flask, jsonify, request, render_template, session, g, flash, redirect
import requests, urllib.request, json
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User
from forms import UserForm, SearchForm


#The test API KEY is 1 which is provided for developers for are using it for educational use
API_URL_BASE = "https://api.spoonacular.com"
API_KEY = "ac045d2e287c43db9ee60e514bfa0d9d"

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cookingbuddy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()
############################
#Homepage and error page
@app.route('/')
def index():
    """Show homepage"""

    return redirect ('/search')

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND PAGE"""

    return render_template('404.html'), 404
##################################################################
#Registration and login routes:
@app.route('/user/register', methods = ['GET', 'POST'])
def register():
    """User Register Form"""

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data,
        password = form.password.data

        try: 
            new_user = User.register(username = username, password= password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful', 'success')
            return redirect('/login')
        
        ##Check if the username is already taken
        except IntegrityError:
            db.session.rollback()
            flash("Username already taken", 'danger')
            return render_template('/user/register.html', form = form)   

    return render_template('/user/register.html', form = form)
    

@app.route('/user/login', methods = ["GET", "POST"])
def login():
    """Handle user login"""
    form = UserForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect('/search')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('/user/login.html', form = form )

@app.route('/logout')
def logout():
    """Handle logout of user"""
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')


#####################################
#General user routes:

@app.route('/user/<int:user_id>')
def show_user(user_id):
    """Show user profile"""

    user = User.query.get_or_404(user_id)

    return render_template('/user/profile.html')
#####################################
# Search bar    
@app.route('/search', methods = ["GET","POST"])
def search():
    """Show search bar for recipes"""

    form = SearchForm()

    if form.validate_on_submit():

        search_query = form.search_query.data
        #construct the API request URL with search_query parameter
        url = f"{API_URL_BASE}/recipes/complexSearch?apiKey={API_KEY}&query={search_query}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            search_results = data['results']

        else:
            #Handle API error if needed
            flash('Failed to fetch recipe data from API', 'error')
            return redirect('/search') #redirect to search page on error
        
        return render_template('/recipes/search_results.html', search_query = search_query, search_results = search_results)
    
    return render_template('search.html', form = form)
            

@app.route('/recipes/<int:id>')
def show_recipe(id):

    """Show Recipe"""

    url = f"https://api.spoonacular.com/recipes/{id}/information?apiKey={API_KEY}"

    response = requests.get(url)
    
    if response.status_code == 200:
            data = response.json()
            recipe_info = {
                "title": data["title"],
                "image": data.get("image"),
                "extendedIngredients":data.get("extendedIngredients"),
                "instructions": data.get("analyzedInstructions"),
                "sourceUrl": data.get("sourceUrl")
            }
    else:
         #Handle API error if needed
            flash('Failed to fetch recipe data from API', 'error')
            return redirect('/search') #redirect to search page on error

    return render_template('/recipes/show_recipe.html', recipe_info = recipe_info)


