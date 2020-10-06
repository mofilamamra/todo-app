from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models.Model import Category, ACCESS
from flask import current_app as app
from app import db
from app.utils.utils import requires_access_level
from app.forms.category import CategoryForm

category = Blueprint('category', __name__)

@category.route('/categories')
@login_required
def categories():
    title = "categories"
    categories = Category.query.all()
    return render_template('categories/index.html',title=title, categories=categories)

@category.route('/new-category', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def new_category():
    title = "ajoutée categorie"
    form = CategoryForm()

    if request.method == 'GET':
      return render_template('categories/create_category.html', title=title, form=form)

    if form.validate_on_submit():
        title = request.form.get("title")
        
        category = Category(title)

        db.session.add(category)
        db.session.commit()

        flash('Votre category a été ajoutée!')

        return redirect(url_for('category.new_category'))
    else:
      return render_template("categories/create_category.html", title=title, form=form)

@category.route('/edit-category/<int:id>', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def edit_category(id):
  title = "Edit Category"
  form = CategoryForm()
  category = Category.query.filter_by(id=id).first()

  if request.method == 'GET':

    form.title.data = category.title
    return render_template('categories/edit_category.html', title=title, form=form, category=category)

  if form.validate_on_submit():
    
    title = request.form.get("title")
    
    category.title = title

    db.session.commit()

    flash('Votre category a été modifiée!')
    return redirect(url_for('category.categories'))

  else:
    return render_template('categories/edit_category.html', title=title, form=form, category=category)


@category.route('/delete-category/<int:id>', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def delete(id):
  category = Category.query.filter_by(id=id).delete()
  
  db.session.commit()
  return redirect(url_for('category.categories'))
