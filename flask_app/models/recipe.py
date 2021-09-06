from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.under_30 = data['under_30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @classmethod
    def add_recipe(cls, data):
        query = 'INSERT INTO recipes (name, under_30, description, instructions, date, users_id) VALUES (%(name)s, %(under_30)s, %(description)s, %(instructions)s, %(date)s, %(users_id)s);'
        result = connectToMySQL('recipes').query_db(query, data)
        return result
    
    @classmethod
    def get_all_recipes(cls):
        query='SELECT * FROM recipes;'
        results= connectToMySQL('recipes').query_db(query)
        recipes= []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.users_id = users.id WHERE recipes.id = %(id)s;"

        result = connectToMySQL('recipes').query_db(query, data)

        recipe = cls(result[0])
        user_data = {
            'id': result[0]['users.id'],
            'first_name': result[0]['first_name'],
            'last_name': result[0]['last_name'],
            'email': result[0]['email'],
            'password': result[0]['password'],
            'created_at': result[0]['users.created_at'],
            'updated_at': result[0]['users.updated_at']
        }
        recipe.user = User(user_data)

        return recipe

    @classmethod
    def update_recipe(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date = %(date)s WHERE id = %(id)s;'

        connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):

        query = 'DELETE FROM recipes WHERE id = %(id)s;'

        connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def validate_recipe(data):

        is_valid = True

        if len(data['name']) < 2 or len(data['name']) > 45:
            flash("Recipe name should be 2 to 45 characters.")
            is_valid = False

        if len(data['description']) < 2 or len(data['description']) > 255:
            flash("Recipe description should be 2 to 255 characters.")
            is_valid = False

        if len(data['instructions']) < 2 or len(data['instructions']) > 255:
            flash("Recipe instructions should be 2 to 255 characters.")
            is_valid = False

        if len(data['date']) == 0:
            flash("Please provide a date.")
            is_valid = False

        # if len(data['under_30']) == 0:
        #     flash("Please check yes or no.")
        #     is_valid = False

        return is_valid
