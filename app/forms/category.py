from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired


# Category form
class CategoryForm(FlaskForm):

    title = StringField(label="Titre", validators=[DataRequired()])
    submit = SubmitField(label="Créer Category")
