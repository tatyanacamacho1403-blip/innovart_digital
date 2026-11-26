from flask import Flask, jsonify
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider
from flask_mysqldb import MySQL
from datetime import date, datetime, time
from werkzeug.exceptions import HTTPException

from Config import Config
from Security import protect_request

class ISOJSONProvider(DefaultJSONProvider):
    @staticmethod
    def default(value):
        if isinstance(value, (date, datetime, time)):
            return value.isoformat()
        return DefaultJSONProvider.default(value)


mysql = MySQL()


def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json = ISOJSONProvider(app)

    mysql.init_app(app)
    app.mysql = mysql
    CORS(app)
    app.before_request(protect_request)

    from Routes import loadRoutes
    loadRoutes(app)

    @app.route("/health", methods=["GET"])
    def health():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return jsonify({"status": "ok", "database": "connected"}), 200
        except Exception:
            app.logger.exception("Error verificando la conexión a MySQL")
            return jsonify({"status": "error", "database": "disconnected"}), 503

    @app.route("/")
    def home():
        return {"mensaje": "API Innovart Digital funcionando"}, 200

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        if isinstance(error, HTTPException):
            return error
        app.logger.exception("Error procesando la petición")
        return jsonify({"mensaje": "Error interno del servidor"}), 500

    return app


app = createApp()


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host=app.config["HOST"], port=app.config["PORT"])
