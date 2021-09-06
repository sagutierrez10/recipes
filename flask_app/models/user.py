from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def get_users_with_email(cls, data):
        query='SELECT * FROM users WHERE email =%(email)s;'
        results= connectToMySQL('recipes').query_db(query, data)
        users= []
        for item in results:
            users.append(User(item))
        return users

    @classmethod
    def saveUser(cls, data):
        query= "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"
        return connectToMySQL('recipes').query_db( query, data )

    @staticmethod
    def is_registration_valid(data):
        is_valid = True
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        word_regex = re.compile(r'[a-zA-Z]')
        first_name = data["first_name"] 
        last_name = data["last_name"]
        email = data["email"]
        pw = data["password"] 

        if len(first_name) <= 2: 
            is_valid = False
            flash("First name must contain at least three letters")
        elif not word_regex.match(first_name): 
            is_valid = False
            flash("First name must only contain letters")

        if len(last_name) <= 2: 
            is_valid = False
            flash("Last name must contain at least three letters")
        elif not word_regex.match(last_name): 
            is_valid = False
            flash("Last name must only contain letters")

        if not email_regex.match(email):
            is_valid = False
            flash("Invalid email")
        
        if len(pw) < 8:
            is_valid = False
            flash("Password must be at least 8 characters")
        if pw != pw : 
            is_valid = False
            flash("Password must match")
        if len(User.get_users_with_email({'email':data['email']})) != 0:
            is_valid = False
            flash('This email address is already taken')

        return is_valid

    @staticmethod
    def is_login_valid(data):
        is_valid = True

        users =  User.get_users_with_email({'email':data['email']})
        if len(users) == 0:
            flash('password or email is incorrect') 
            return False
        if not bcrypt.check_password_hash(users[0].password, data['password']):
            flash('password or email is incorrect')
            return False
        session['user_id'] = users[0].id
        session['user_first_name'] = users[0].first_name
        return is_valid

    @staticmethod
    def is_logged_in():
        if 'user_id' not in session:
            return False
        return True
        




