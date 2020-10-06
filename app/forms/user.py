from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models.Model import Category

def get_categories():
    categories_query = Category.query.all()
    categories = []

    for category in categories_query:
        categories.append((category.id,category.title)) 

    return categories


# Register form
class RegisterForm(FlaskForm):
    email = StringField(label="email", validators=[DataRequired(), Email()])
    username = StringField(label="username", validators=[DataRequired()])
    password = PasswordField(label="password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField(label="confirm", validators=[DataRequired(),EqualTo(fieldname='password')])
    category = SelectField('Selectionée une category', validators=[DataRequired()],choices=get_categories())
    submit = SubmitField(label="inscrire")

# login form
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('identifier')
