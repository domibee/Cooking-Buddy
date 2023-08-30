import os 

from flask import Flask, render_template, session, g, flash, redirect, request, url_for
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Recipe, UserFavorite
from forms import UserForm,LoginForm, SearchForm

CURR_USER_KEY = "curr_user"

#The test API KEY is 1 which is provided for developers for are using it for educational use
API_URL_BASE = "https://api.spoonacular.com"
API_KEY = "ac045d2e287c43db9ee60e514bfa0d9d"

app = Flask(__name__)
app.app_context().push()
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")



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
        display_name = form.display_name.data
        username = form.username.data
        password = form.password.data

        try: 
            new_user = User.register(display_name = display_name, username = username, password= password)
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
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        
        if user:
            do_login(user)
            flash(f"Welcome Back, {user.display_name}!", "primary")
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

@app.route('/user/<int:id>/favorites', methods=["GET","POST"])
def favorites(id):
    """Show user favorites"""

    if not g.user:
        flash("You must login first or create an account.", "danger")
        return redirect('/user/login')

    user = User.query.get_or_404(id)
    favorited_recipes_info = []

    for favorited_recipe in user.favorites:
        url = f"https://api.spoonacular.com/recipes/{favorited_recipe.recipe_api_id}/information?apiKey={API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            recipe_info = {
                "title": data["title"],
                "image": data.get("image"),
                "recipe_api_id": favorited_recipe.recipe_api_id
            }
            favorited_recipes_info.append(recipe_info)
        else:
            flash('Sorry, we are experiencing some technical difficulties. Please try again later or contact support for assistance.', 'danger')
            return redirect('/search')

    return render_template('/user/profile.html', user=user, favorited_recipes_info=favorited_recipes_info)


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
            # Save the search results to the database
            for result in search_results:
                 # Check if the recipe already exists in the database
                existing_recipe = Recipe.query.filter_by(recipe_api_id=result['id']).first()

                # If the recipe already exists, skip adding it again
                if existing_recipe:
                    continue

                recipe = Recipe(
                    recipe_api_id = result.get('id'),
                    title =result['title'],
                    default_image =result.get('image', None),
                    
                )
                db.session.add(recipe)
            db.session.commit()
            
        else:
            #Handle API error if needed
            flash('Sorry, we are experiencing some technical difficulties. Please try again later or contact support for assistance.', 'danger')
            return redirect('/search') #redirect to search page on error
        
        return redirect(url_for('search_results', query=search_query))
    
    return render_template('search.html', form = form)

@app.route('/search_results')
def search_results():
    
    form = SearchForm()

    search_query = request.args.get('query', '')
    page = request.args.get('page',1, type=int)
    items_per_page = 12 # Number of items to show per page
   
    url = f"{API_URL_BASE}/recipes/complexSearch?apiKey={API_KEY}&query={search_query}&offset={(page - 1) * items_per_page}&number={items_per_page}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        search_results = data['results']  # Extract the 'results' key 
        total_results = data['totalResults'] # Extract the total number of results 
            
    else:
        flash('Sorry, we are experiencing some technical difficulties. Please try again later or contact support for assistance.', 'danger')
        return redirect('/search')
    
    # Calculate the total number of pages needed for pagination
    total_pages = (total_results + items_per_page - 1) // items_per_page
        
    current_page_results = search_results
        
    return render_template('/recipes/search_results.html', 
                        search_query=search_query, 
                        current_page_results=current_page_results, 
                        total_pages=total_pages, current_page=page, form=form)
    


@app.route('/recipes/<int:recipe_api_id>', methods = ["GET","POST"])
def show_recipe(recipe_api_id):

    """Show Recipe"""

    url = f"https://api.spoonacular.com/recipes/{recipe_api_id}/information?apiKey={API_KEY}"

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
        flash('Sorry, we are experiencing some technical difficulties. Please try again later or contact support for assistance.', 'danger')
        return redirect('/search') #redirect to search page on error
        
    if g.user:    
    # Get the favorite recipe IDs for the user
        user_favorite_recipe_ids = [fav.recipe_api_id for fav in g.user.favorites]

        is_favorite = recipe_api_id in user_favorite_recipe_ids

        return render_template('/recipes/show_recipe.html', recipe_info  = recipe_info, recipe_api_id = recipe_api_id, is_favorite = is_favorite)
    
    return render_template('/recipes/show_recipe.html', recipe_info  = recipe_info, recipe_api_id = recipe_api_id)

@app.route('/recipes/<int:recipe_api_id>/favorite', methods=["POST"])
def add_favorite(recipe_api_id):
    """Toggle a favorited recipe for the currently-logged-in user"""

    if not g.user:
        flash("You must login first or create an account.", "danger")
        return redirect('/user/login')

    favorited_recipe = Recipe.query.get_or_404(recipe_api_id)
    # filter the user_id and recipe id from UserFavorite table
    user_favorite = UserFavorite.query.filter_by(user_id=g.user.id, recipe_id=favorited_recipe.recipe_api_id).first()
    
    if user_favorite:
        db.session.delete(user_favorite)
        db.session.commit()

    else:
        user_favorite = UserFavorite(user_id=g.user.id, recipe_id=favorited_recipe.recipe_api_id)
        db.session.add(user_favorite)
        db.session.commit()    
        
    # Redirect back to the same page
    return redirect(url_for('show_recipe', recipe_api_id = recipe_api_id))


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req    

