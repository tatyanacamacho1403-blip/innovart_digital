from flask import Flask
from flask_mysqldb import MySQL
#from flask_cors import CORS

from Config import Config
from Routes import loadRoutes





def createApp():

    app = Flask(__name__)

    app.config.from_object(Config)
    mysql = MySQL(app)

    #mysql.init_app(app)

    app.mysql = mysql

    #CORS(app)

    loadRoutes(app)

    return app


app = createApp()


#if __name__ == "__main__":
 #app.run(debug=True, host="0.0.0.0", port=5000)
