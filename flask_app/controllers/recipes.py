from flask import flash, session, redirect, render_template, request
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/dashboard')
def show_recipes():
    if 'user_id' not in session:
        flash('Please log in to view this page.')
        return redirect('/')
    recipes = Recipe.get_all_recipes()
    print(recipes)
    return render_template('dashboard.html', recipes = recipes, user_first_name= session['user_first_name'])

@app.route('/recipes/new')
def new_recipe():
    return render_template('new_recipe.html')

@app.route('/recipe/create', methods=['POST'])
def Add_recipe():

    if Recipe.validate_recipe(request.form):

        data = {
            'name': request.form['name'],
            'under_30': request.form['under_30'],
            'instructions': request.form['instructions'],
            'description': request.form['description'],
            'date': request.form['date'],
            'users_id': session['user_id']
        }
        Recipe.add_recipe(data)
        print('recipe valid')
        return redirect('/dashboard')
    print('recipe invalid')
    return redirect('/recipes/new')

@app.route('/recipes/<int:recipe_id>')
def recipe_info(recipe_id):

    recipe = Recipe.get_recipe_by_id({'id': recipe_id})

    return render_template('recipe_info.html', recipe = recipe, user_first_name= session['user_first_name'])

@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):

    recipe = Recipe.get_recipe_by_id({'id': recipe_id})

    if session['user_id'] != recipe.users_id:
        return redirect(f'/recipes/{recipe_id}')

    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):

    if Recipe.validate_recipe(request.form):
        data = {
            'name': request.form['name'],
            'date': request.form['date'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'id': recipe_id
        }
        Recipe.update_recipe(data)
        return redirect(f'/recipes/{recipe_id}')

    return redirect(f'/recipes/{recipe_id}/edit')


@app.route('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    recipe= Recipe.get_recipe_by_id({'id':recipe_id})
    if session['user_id'] != recipe.user.id:
        return redirect(f'/recipes/{recipe_id}')

    Recipe.delete_recipe({'id': recipe_id})


    return redirect('/dashboard')

