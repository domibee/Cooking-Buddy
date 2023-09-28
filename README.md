# [CookingBuddy](https://cookingbuddy.onrender.com/)

Cooking Buddy is a web application that allows users to search for, save, and share their favorite recipes. It is built using Flask and incorporates elements from the Springboard curriculum, providing a platform to practice various programming concepts and skills.

## API: [Spoonacular API](https://spoonacular.com/food-api/docs)

## Database Schema: 

![Cooking Buddy Database](https://github.com/domibee/Cooking-Buddy/blob/main/CookingBuddy.png)

## Setup

~~~
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
(venv) $ createdb cookingbdb
(venv) $ python3 -m flask run
~~~

The app will be accessible at `http://localhost:5000`.

### Features: 

- User registration and authentication

![Searching for burgers](https://github.com/domibee/Cooking-Buddy/blob/main/static/favorite-burger.gif)

- Search for recipes using an external API

![Prepare the  ingredients](https://github.com/domibee/Cooking-Buddy/blob/main/static/ingredient-check.gif)

- View detailed recipe information including image, ingredients, and instructions
- Save and remove recipes to/from favorites list


