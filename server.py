from flask_app import app

#importamos los controladores
from flask_app.controllers import users_controller

#ejecutamos la aplicacion
if __name__=='__main__':
    app.run(debug=True)