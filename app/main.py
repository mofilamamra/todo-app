from . import db
from app.models import User, Task

from flask import Blueprint, render_template, redirect, url_for, request, flash,abort,Response
from flask_login import current_user, login_required
from io import BytesIO
from werkzeug.utils import secure_filename


# @main.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', name=current_user.name)


@main.route('/new')
@login_required
def new_workout():
    return render_template('create_workout.html')

@main.route('/new', methods=['POST'])
@login_required
def new_workout_post():
    pushups = request.form.get('pushups')
    comment = request.form.get('comment')
    title = request.form.get("title")
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

   # img = Todo(img=pic.read(),title=title, name=filename, mimetype=mimetype)
    # new_todo = Todo(title=title, complete=False)

    task = Task(img=pic.read(),title=title, name=filename, mimetype=mimetype,pushups=pushups, comment=comment, author=current_user)
    db.session.add(task)
    db.session.commit()

    flash('Your task has been added!')

    return redirect(url_for('main.user_workouts'))

@main.route('/all')
@login_required
def user_workouts():
    user = User.query.filter_by(email=current_user.email).first_or_404()
  #  user = User.query.all()

    workouts = user.workouts
    return render_template('all_workouts.html', workouts=workouts, user=user)


@main.route('/update/<int:workout_id>')
def update(workout_id):
    task = Task.query.filter_by(id=workout_id).first()
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('main.user_workouts'))


@main.route('/download/<int:workout_id>')
@login_required
def get_img(workout_id):
    task = Task.query.filter_by(id=workout_id).first()
    if not task:
        return 'Img Not Found!', 404
    try:
        return Response(task.img,mimetype=task.mimetype)
    except Exception as e:
        return str(e)

###############################
#@app.route("/")
@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    todolist = Todo.query.paginate(page=page, per_page=5)
    return render_template("base1.html", todolist=todolist)


@main.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form.get("title")

    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Todo(img=pic.read(),title=title, name=filename, mimetype=mimetype)
    # new_todo = Todo(title=title, complete=False)
    db.session.add(img)
    db.session.commit()
    return redirect(url_for("home"))
    # return redirect(url_for("get_img",id = img.id))

    #return 'Img Uploaded!', 200

@main.route('/thread/<int:page_num>')
@login_required
def thread(page_num):
    page = request.args.get('page', 1, type=int)
    threads = Todo.query.paginate(per_page=5,page=page_num,error_out=True)
    return render_template('base.html',threads=threads)






@main.route("/delete/<int:todo_id>")
@login_required
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))
