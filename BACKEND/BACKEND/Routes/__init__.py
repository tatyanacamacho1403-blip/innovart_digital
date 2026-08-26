from .empleado import empleado_bp
from .persona import persona_bp
from .usuario import usuario_bp
from .servicio import servicio_bp
from .agenda import agenda_bp
from .consulta import consulta_bp
from .pago import pago_bp
from .rol import rol_bp
from .respuesta import respuesta_bp
from .servicio_agenda import servicio_agenda_bp


def load_routes(app):

    app.register_blueprint(persona_bp, url_prefix="/api/personas")
    app.register_blueprint(usuario_bp, url_prefix="/api/usuarios")
    app.register_blueprint(empleado_bp, url_prefix="/api/empleados")
    app.register_blueprint(servicio_bp, url_prefix="/api/servicios")
    app.register_blueprint(agenda_bp, url_prefix="/api/agendas")
    app.register_blueprint(consulta_bp, url_prefix="/api/consultas")
    app.register_blueprint(pago_bp, url_prefix="/api/pagos")
    app.register_blueprint(rol_bp, url_prefix="/api/roles")
    app.register_blueprint(respuesta_bp, url_prefix="/api/respuestas")
    app.register_blueprint(servicio_agenda_bp, url_prefix="/api/servicios-agenda")
