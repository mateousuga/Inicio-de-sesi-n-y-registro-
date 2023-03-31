from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash # es el encargado de mostrar mensajes/errores

import re #importando expresiones regulares

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    
    #validar todos los datos del usuario
    @staticmethod
    def valida_usuario(formulario):
        #formulario = diccionario con todos los names y valores que el usuario va a ingresar
        es_valido = True
        
        #validar que el nombre del usuario tenga almenos 3 caracteres
        if len(formulario['first_name']) < 3:
            es_valido = False
            flash("Nombre debe de tener almenos 3 caracteres", "registro")
        
        #validar que el apellido del usuario tenga almenos 3 caracteres
        if len(formulario['last_name']) < 3:
            es_valido = False
            flash("Appelido debe de tener almenos 3 caracteres", "registro")
        
        #validar que el password del usuario tenga almenos 6 caracteres
        if len(formulario['password']) < 6:
            es_valido = False
            flash("Contraseña debe de tener almenos 6 caracteres", "registro")
        
        #verificamos que las contraseñas coincidan
        if formulario['password'] != formulario['confirm_password']:
            es_valido = False
            flash("Las contraseñas deben coincidir", "registro")
        
        #revisamos que el email tengo el formato correcto con las expresiones regulares
        if not EMAIL_REGEX.match(formulario['email']):
            es_valido = False
            flash("Email invalido", "registro")
        
        #consultamos si exite el email 
        query = "SELECT * FROM users WHERE email = %(email)s" 
        results = connectToMySQL('login_registro').query_db(query, formulario)
        if len(results) >= 1:
            es_valido = False
            flash("Email registrado previamente", "registro")
        return es_valido
            
    #registramos al usuario
    @classmethod
    def save(cls, formulario):
        #formulario = {first_name: 'helena', last_name: 'de troya', email: 'helena@gmail.com', password: "jaksksosks"}
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('login_registro').query_db(query, formulario)
        return result #el ID del nuevo registro que se realizo
    
    #funcion que reciba un diccionario con un correo y me regrese si el usuario existe o no
    @classmethod
    def get_by_email(cls, formulario):
        #formulario = {email: 'helena@gmail.com', password: 123}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('login_registro').query_db(query, formulario) #SELECT me regresa una lista
        if len(result) < 1: #significa que lista esta vacia
            return False
        else:
            #me regresa una lista con un solo registro 
            #result = [{id: 1, first_name: 'helena', last_name: 'de troy',..... }] ->posicion cero
            user = cls(result[0]) #crea una instancia en base a lo que se recibio en la lista 
            return user
    
    @classmethod
    def get_by_id(cls, formulario):
        #formulario = {id: 1}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('login_registro').query_db(query, formulario)
        #me regresa una lista con un solo registro 
        #result = [{id: 1, first_name: 'helena', last_name: 'de troy',..... }] ->posicion cero
        user = cls(result[0]) #crea una instancia del usuario 
        return user