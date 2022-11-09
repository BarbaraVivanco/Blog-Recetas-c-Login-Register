from login_register.config.mysqlconnection import connectToMySQL
from login_register.models.log_reg import User
from flask import flash 


class Recipe: 
    base_datos="recetas_schema"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.under = data['under']
        self.date_made = data['date_made']
        self.description = data['description']
        self.instruction = data['instruction']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.usuario = []

    @classmethod
    def crear_receta(cls, data):
        query = " INSERT INTO recipes (name, under, date_made,description,instruction, user_id ) VALUES( %(name)s, %(under)s, %(date_made)s,%(description)s, %(instruction)s, %(usuario_id)s);"
        resultado = connectToMySQL('recetas_schema').query_db(query, data)
        return resultado

    @classmethod
    def todas_recetas(cls):
        query = "SELECT * FROM recipes;"
        resultado = connectToMySQL('recetas_schema').query_db(query)
        todas_las_recetas = []
        for receta in resultado:
            todas_las_recetas.append(cls(receta))
        return todas_las_recetas
    
    @classmethod
    def recetas_con_usuarios(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        resultado = connectToMySQL('recetas_schema').query_db(query)
        todas_las_recetas_con_usuarios = []
        for receta in resultado:
            objeto_receta = cls(receta)
            objeto_receta.usuario.append(User(receta))
            todas_las_recetas_con_usuarios.append(objeto_receta)
        return todas_las_recetas_con_usuarios 
    

    @classmethod
    def receta_de_un_usuario(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id=%(id)s;"
        resultado = connectToMySQL('recetas_schema').query_db(query, data)
        una_receta_con_usuario = cls(resultado[0])
        una_receta_con_usuario.usuario.append(User(resultado[0]))
        return una_receta_con_usuario
    

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description= %(description)s,  date_made=%(date_made)s, under= %(under)s,instruction=%(instruction)s  WHERE id= %(receta_id)s;"
        return connectToMySQL('recetas_schema').query_db(query,data)

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('recetas_schema').query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recetas_schema').query_db(query,data)

    @staticmethod
    def validation(recipe):
        is_valid = True 
        if len(recipe['name']) < 3:
            flash("Name must be not blank and must be at least 3 characters!",'crear_receta')
            is_valid = False
        #if len(recipe['under']) == 0:
            #flash("under field must be at least one option.",'crear_receta')
            #is_valid = False
        if len(recipe['date_made']) == 0:
            flash("date_made field must be not blank","crear_receta")
            is_valid = False
        if len(recipe['description']) == 0:
            flash("description field must be not blank","crear_receta")
        if len(recipe['instruction']) == 0:
            flash("instruction field must be not blank","crear_receta")    
            is_valid = False
        return is_valid

    @staticmethod
    def validate_edit(recipe):
        is_valid = True 
        if len(recipe['name']) <3:
            flash("Name must be not blank and must be at least 3 characters!",'update')
            is_valid = False
        #if len(recipe['under']) == "":
            #flash("under field must be at least one option.",'update')
            #is_valid = False
        if len(recipe['date_made']) == 0:
            flash("date_made field must be not blank","update")
            is_valid = False
        if len(recipe['description']) == 0:
            flash("description field must be not blank","update")
        if len(recipe['instruction']) == 0:
            flash("instruction field must be not blank","update")    
            is_valid = False
        return is_valid