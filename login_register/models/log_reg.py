from login_register.config.mysqlconnection import connectToMySQL
from login_register.controllers import log_regs
from flask import flash 
import re
from flask_bcrypt import Bcrypt
from login_register import app
bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX= re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")


class User: 
    base_datos="recetas_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def entry(cls,data):
        query = "INSERT INTO users (first_name, last_name, age, email, password) VALUES (%(first_name)s, %(last_name)s, %(age)s,%(email)s, %(password)s);"
        return connectToMySQL(cls.base_datos).query_db(query,data)
    
    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.base_datos).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email_1)s;"
        result = connectToMySQL(cls.base_datos).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validation(user):
        print(user, 'QUE CONTIENEEEEEEEEEEEEEEEEE')
        is_valid = True 
        if user['first_name']=="":
            flash("The first name field cannot be empty!", 'register')
        elif len(user['first_name']) < 3:
            flash("Name must be at least 3 characters!", 'register')
            is_valid = False
        if user['last_name']=="":
            flash(" The last name field cannot be empty!", 'register')
        elif len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", 'register')
            is_valid = False
        if  user['age'] =="":
            flash("The age field cannot be empty!", 'register')
            is_valid = False
        elif int(user['age']) < 18:
            flash("You must be 18 or older to register!", 'register')
            is_valid = False
        if user['email']=="":
            flash(" The email field cannot be empty!", 'register')
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False
        if user['password']=="":
            flash(" Password field cannot be empty!", 'register')
        elif not PASSWORD_REGEX.match(user['password']): 
            flash("Password must be minimum 8 characters, at least one letter and one number!", 'register')
        #if len(user['password']) < 5:
            #flash("Password must be at least 5 characters", 'register')
            is_valid = False
        if user['confirm']=="":
            flash(" Confirm Password field cannot be empty!", 'register')
        elif user['password'] != user['confirm']:
            flash("Passwords do not match!", 'register')
            is_valid = False
        #if user['first_name', 'last_name','age','email','password']==0:
            #flash("All form fields are required for register!")
            #is_valid = False
        return is_valid

    @staticmethod
    def validate_login(login_form):
        is_valid = True
        get_one_user= User.get_email(login_form)
        if get_one_user == False:
            flash("The email adress doesn't exist!", "login")
            is_valid = False
        elif not bcrypt.check_password_hash(get_one_user.password, login_form['password_1']):
        # si obtenemos False después de verificar la contraseña
            flash("Invalid Email/Password", "login")
            is_valid=False
        return is_valid, get_one_user
