from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def home():
    if User.is_logged_in():
        return render_template('/login.html')
    return render_template("index.html")

@app.route('/create_user', methods=['POST'])
def create_user():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    if (not User.is_registration_valid(data)):
        return redirect('/dashboard')

    User.saveUser(data)
    return redirect('/login.html')

@app.route('/login', methods=['POST'])
def login():
    data = {'email':request.form['email'],
            'password': request.form['password']}
    if ( not User.is_login_valid(data)):
        return redirect('/')
    return redirect('/dashboard')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')








