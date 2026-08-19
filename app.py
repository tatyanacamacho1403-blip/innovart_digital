from flask import Flask
from flask_mysqldb import MySQL

from config import Config

from Routes.persona_bp import persona_bp
from Routes.usuario_bp import usuario_bp
from Routes.empleado_bp import empleado_bp
from Routes.servicio_bp import servicio_bp
from Routes.agenda_bp import agenda_bp
from Routes.consulta_bp import consulta_bp
from Routes.pago_bp import pago_bp


app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
app.mysql = mysql
