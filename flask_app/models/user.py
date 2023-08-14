from flask_app.config.mysql_connection import connect_To_MySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

DATABASE = 'login_and_reg'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def check_if_login(form_data):
        is_valid = True 
        if len(form_data['email']) == 0:
            is_valid = False
            flash('Please enter a Email.', 'login')
        elif not EMAIL_REGEX.match(form_data['email']):
            is_valid = False
            flash('Invalid Email', 'login'), 'register'

        if len(form_data['password']) == 0:
            is_valid = False        
            flash('Please enter a Password.', 'login')
        elif len(form_data['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters.', 'login')
        return is_valid
    
    @staticmethod
    def check_if_reg(form_data):
        is_valid = True
        if len(form_data['first_name'].strip()) == 0:
            is_valid = False
            flash('Please enter a First Name.', 'register')
        elif len(form_data['first_name'].strip()) < 2:
            is_valid = False
            flash('Please enter a valid First Name.', 'register')

        if len(form_data['last_name']) == 0:
            is_valid = False
            flash('Please enter a Last Name.', 'register')
        elif len(form_data['last_name']) < 2:
            is_valid = False
            flash('Please enter a valid Last Name.', 'register')

        if len(form_data['email']) == 0:
            is_valid = False
            flash('Please enter a Email.', 'register')
        elif not EMAIL_REGEX.match(form_data['email']):
            is_valid = False
            flash('Invalid Email', 'register')

        if len(form_data['password']) == 0:
            is_valid = False        
            flash('Please enter a Password.', 'register')
        elif len(form_data['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters.', 'register')

        elif len(form_data['confirm_password']) == 0:
            is_valid = False        
            flash('Please confirm Password.', 'register')
        elif form_data['confirm_password'] != form_data['password']:
            is_valid = False        
            flash('Passwords do not match.', 'register')

        return is_valid

    @classmethod
    def create(cls, form_data):
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        result = connect_To_MySQL(DATABASE).query_db(query, form_data)
        return result
    
    @classmethod
    def get_by_email(cls, email):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s
                """
        data = {'email': email}
        results = connect_To_MySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return None
        else:
            return User(results[0])
        

    @classmethod
    def get_by_id(cls, user_id):
        query = """
                SELECT * FROM users
                WHERE id = %(user_id)s
                """
        data = {'user_id': user_id}
        results = connect_To_MySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return None
        else:
            return User(results[0])
