from flask import Flask

app = Flask(__name__) #inicializamos la app

app.secret_key = "llave secret"