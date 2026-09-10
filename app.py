from flask import Flask
from flask_mysqldb import MySQL

# from config import Config

from Routes.usuario import usuario_bp
from Routes.empleado import empleado_bp
from Routes.persona import persona_bp
from Routes.servicio import servicio_bp
from Routes.agenda import agenda_bp
from Routes.consulta import consulta_bp
from Routes.pago import pago_bp


app = Flask(__name__)
app.register_blueprint(agenda_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(consulta_bp)
app.config.from_object(pago_bp)
app.config.from_object(empleado_bp)
app.config.from_object(persona_bp)
app.config.from_object(servicio_bp)

mysql = MySQL(app)
app.mysql = mysql