from . import db, ma
from flask_login import UserMixin
from datetime import datetime

ACCESS = {
    'user': 1,
    'admin': 2
}

class User(db.Model, UserMixin):
    
    def __init__(self, username, email, password,category_id, access=ACCESS['user']):
        self.username = username
        self.email = email
        self.password = password
        self.category_id = category_id
        self.access = access
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    access = db.Column(db.Integer,default=1)
    tasks = db.relationship('Task', backref='user', lazy="dynamic")
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def is_admin(self):
        return self.access == ACCESS['admin']
    
    def allowed(self, access_level):
        return self.access >= access_level

class UserSchema(ma.Schema):
  class Meta:
    fields = ['email','username', 'tasks']

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# =======================================

class Task(db.Model):

    def __init__(self, title, description, image, date, user_id):
        self.title = title
        self.description = description
        self.image = image
        self.date = date
        self.user_id = user_id
        self.complete = False
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    complete = db.Column(db.Boolean, nullable=False,default=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class TaskSchema(ma.Schema):
  class Meta:
    fields = ['title','description', 'complete', 'date', 'image', 'user_id']

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


# ======================================

class Category(db.Model):

    def __init__(self, title):
        self.title = title
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='category', lazy="dynamic")

class CategorySchema(ma.Schema):
  class Meta:
    fields = ['title', 'user_id']

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
