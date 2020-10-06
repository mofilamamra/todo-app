from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Required
from wtforms.widgets import TextArea
from datetime import datetime
from app.models.Model import User

def get_users():
    users_query = User.query.all()
    users = []

    for user in users_query:
        users.append((user.id,user.username)) 

    return users

# Task form
class TaskForm(FlaskForm):

    title = StringField(label="Titre", validators=[DataRequired()])
    description = StringField(label="Description", validators=[DataRequired()], widget=TextArea())
    image = FileField(validators=[FileRequired()])
    date = DateField('Date de la tache', validators=[Required()], format='%d/%m/%Y', default=datetime.today)
    user = SelectField('Attribuez la tâche à', validators=[DataRequired()],choices=get_users())
    submit = SubmitField(label="Créer Tache")
