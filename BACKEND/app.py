from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS

from config import Config
from Routes import load_routes


mysql = MySQL()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    app.mysql = mysql

    # Permite que un frontend separado consuma la API durante desarrollo.
    CORS(app)

    load_routes(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
