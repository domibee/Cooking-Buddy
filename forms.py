from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, DataRequired

class UserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max =20)])
    password = PasswordField('Password', validators=[InputRequired()])
    
class SearchForm(FlaskForm):
    search_query = StringField('Search', validators= [DataRequired()])
    

