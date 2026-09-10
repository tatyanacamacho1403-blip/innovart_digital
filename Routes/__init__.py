from .agenda import agenda_bp
from .consulta import consulta_bp
from .empleado import empleado_bp
from .pago import pago_bp
from .persona import persona_bp
from .servicio import servicio_bp
from .usuario import usuario_bp
from .respuesta import respuesta_bp
from .rol import rol_bp
from .servicio_agenda import servicio_agenda_bp


def load_routes(app):

    app.register_blueprint(persona, url_prefix='/personas')
    app.register_blueprint(usuario, url_prefix='/usuarios')
    app.register_blueprint(empleado, url_prefix='/empleados')
    app.register_blueprint(servicio, url_prefix='/servicios')
    app.register_blueprint(agenda, url_prefix='/agendas')
    app.register_blueprint(consulta, url_prefix='/consultas')
    app.register_blueprint(pago, url_prefix='/pagos')
    app.register_blueprint(respuesta, url_prefix='/respuestas')
    app.register_blueprint(rol, url_prefix='/roles')
    app.register_blueprint(servicio_agenda, url_prefix='/servicios-agenda')
