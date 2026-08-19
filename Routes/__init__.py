from .agenda_bp import agenda_bp
from .consulta_bp import consulta_bp
from .empleado_bp import empleado_bp
from .pago_bp import pago_bp
from .persona_bp import persona_bp
from .servicio_bp import servicio_bp
from .usuario_bp import usuario_bp
from .respuesta_bp import respuesta_bp
from .rol_bp import rol_bp
from .servicio_agenda_bp import servicio_agenda_bp


def load_routes(app):

    app.register_blueprint(persona_bp, url_prefix='/personas')
    app.register_blueprint(usuario_bp, url_prefix='/usuarios')
    app.register_blueprint(empleado_bp, url_prefix='/empleados')
    app.register_blueprint(servicio_bp, url_prefix='/servicios')
    app.register_blueprint(agenda_bp, url_prefix='/agendas')
    app.register_blueprint(consulta_bp, url_prefix='/consultas')
    app.register_blueprint(pago_bp, url_prefix='/pagos')
    app.register_blueprint(respuesta_bp, url_prefix='/respuestas')
    app.register_blueprint(rol_bp, url_prefix='/roles')
    app.register_blueprint(servicio_agenda_bp, url_prefix='/servicios-agenda')
