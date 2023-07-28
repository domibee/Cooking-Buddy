import os 

from flask import Flask, jsonify, render_template, session, g, flash, redirect
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Recipe, UserFavorite
from forms import UserForm, SearchForm
CURR_USER_KEY = "curr_user"

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


##################################################################
#Registration and login routes:

#decorator that will run before any view function route and is used for tasks that need to be executed on every request

#g global object that is used to store data that is specifc to thee current request 
# and is accessible throughout the lifetime of that request 
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr_user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user"""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/user/register', methods = ['GET', 'POST'])
def register():
    """User Register Form
    
    Create new user and add to DB. Redirect to homepage.
    
    If for not valid, present form.
    
    If the user already exists with that username: flash message and re-present form"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        try: 
            new_user = User.register(username = username, password= password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful', 'success')
            return redirect('/user/login')
        
        ##Check if the username is already taken
        except IntegrityError:
            db.session.rollback()
            flash("Oops! Something went wrong while submitting the form. Please try again or contact support for help.", 'danger')
            return render_template('/user/register.html', form = form)   
    
    else: 
        return render_template('/user/register.html', form = form)
    

@app.route('/user/login', methods = ["GET", "POST"])
def login():
    """Handle user login"""
    form = UserForm()
    
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        
        if user:
            do_login(user)
            flash(f"Welcome Back, {user.username}!", "primary")
            return redirect('/search')
        
        flash("Invalid username or password. Please double-check your login credentials and try again.", 'danger')

    return render_template('/user/login.html', form = form )

@app.route('/logout')
def logout():
    """Handle logout of user"""
    
    do_logout()

    flash("Goodbye!", "info")
    return redirect('/')

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

#####################################
#General user routes:

@app.route('/user/<int:id>')
def show_user(id):
    """Show user profile"""

    user = User.query.get_or_404(id)
    
    return render_template('/user/profile.html', user = user)

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
            flash('Sorry, we are experiencing some technical difficulties. Please try again later or contact support for assistance.', 'danger')
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


# @app.route('/recipes/<int:id>/favorite', methods = ['POST'])
# def add_favorite( recipe_id):
#     """Toggle a favorited recipe for the currently-logged-in user"""

#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect('/')
    
#     favorited_recipe = Recipe.query.get_or_404(recipe_id)

#     # Check if the user has already favorited the recipe
#     if favorited_recipe in g.user.favorites:
#         g.user.favorites.remove(favorited_recipe) # Remove the favorite
#     else:
#         g.user.favorites.append(favorited_recipe) # Add the favorite
    
#     db.session.commit()
#     return redirect("/")

