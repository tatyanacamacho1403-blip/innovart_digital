from flask import Flask
from flask_mysqldb import MySQL
from Config import Config
from Routes import loadRoutes

def createApp():

    app = Flask(__name__)

    #cargar configuración 
    app.config.from_object(Config)

    #crear conexión con mysql
    mysql = MySQL(app)

    #guardar mysql dentro de la app
    app.mysql = mysql

    #carga todas las rutas
    loadRoutes(app)

    return app

app = createApp()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
