from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, DataRequired

class UserForm(FlaskForm):
    display_name = StringField('Your Display Name',validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max =20)])
    password = PasswordField('Password', validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max =20)])
    password = PasswordField('Password', validators=[InputRequired()])
    
class SearchForm(FlaskForm):
    search_query = StringField('', validators= [DataRequired()])
    
class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    display_name = StringField('Your Display Name')
    image_url = StringField('(Optional) Image URL')