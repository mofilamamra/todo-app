from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import current_user, login_required
from app.models.Model import User, Task,Category , ACCESS
from app.forms.task import TaskForm
from werkzeug.utils import secure_filename
import os
from flask import current_app as app
from app import db
from datetime import datetime
from app.utils.utils import requires_access_level

task = Blueprint('task', __name__)

def convert(date_time): 
    format = '%d/%m/%Y'
    datetime_str = datetime.strptime(date_time, format) 
    return datetime_str

@task.route('/tasks')
@login_required
def tasks():
    title = "Taches"
    category = Category.query.filter_by(id=current_user.category_id).first()
    users = category.users.all()

    if current_user.is_admin():
      tasks = Task.query.order_by(Task.date.asc()).all()
    else:
      tasks = []
      for user in users:
        for task in user.tasks.order_by(Task.date.asc()).all():
          tasks.append(task)

    return render_template('tasks/index.html',title=title, tasks=tasks)

@task.route('/new-task', methods=['GET', 'POST'])
@login_required
#@requires_access_level(ACCESS['admin'])
def new_task():
    title = "Ajouter Tache"
    form = TaskForm()
    if request.method == 'GET':
      return render_template('tasks/create_task.html', title=title, form=form)

    if form.validate_on_submit():
        title = request.form.get("title")
        description = request.form.get("description")
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.instance_path, 'photos', filename))
        date = request.form.get("date")
        user_id = request.form.get("user")
        
        task = Task(title,description,filename,convert(date),user_id)

        user = User.query.filter_by(id=user_id).first()

        user.tasks.append(task)

        db.session.add(task)
        db.session.commit()

        flash('Votre tâche a été ajoutée!')

        return redirect(url_for('task.new_task'))
    else:
      return render_template("tasks/create_task.html", title=title, form=form)

@task.route('/download/<int:id>')
@login_required
def download(id):
    task = Task.query.filter_by(id=id).first()
    title = task.title
    filename = task.image
    file = os.path.join(app.instance_path, "photos" ,filename)
    return send_file(file)

@task.route('/complete/<int:id>')
@login_required
def complete(id):
  task = Task.query.filter_by(id=id).first()
  task.complete = True
  db.session.commit()
  return redirect(url_for('task.tasks'))

@task.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
  task = Task.query.filter_by(id=id).delete()
  
  db.session.commit()
  return redirect(url_for('task.tasks'))

@task.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
  title = "Edit Tache"
  form = TaskForm()
  task = Task.query.filter_by(id=id).first()

  if request.method == 'GET':
    form.user.default = task.user.id
    form.process()

    form.description.data = task.description
    form.date.data = task.date
    return render_template('tasks/edit_task.html', title=title, form=form, task=task)

  if form.validate_on_submit():
    f = form.image.data
    filename = secure_filename(f.filename)
    if filename != task.image:
      f.save(os.path.join(app.instance_path, 'photos', filename))
    
    title = request.form.get("title")
    description = request.form.get("description")
    date = request.form.get("date")
    user_id = request.form.get("user")

    task = Task(title,description,filename,convert(date),user_id)

    user = User.query.filter_by(id=user_id).first()

    if user != task.user:
      user.tasks.append(task)
    
    db.session.commit()

    flash('Votre tâche a été modifiée!')
    return redirect(url_for('task.tasks'))

  else:
    return render_template('tasks/edit_task.html', title=title, form=form, task=task)
