from flask import Blueprint
from Controllers.servicio_agenda_controller import ServicioAgendaController


servicio_agenda_bp = Blueprint("servicio_agenda_bp", __name__)


@servicio_agenda_bp.route("/", methods=["GET"])
def listServicioAgenda():
    return ServicioAgendaController.cntListServicioAgenda()


@servicio_agenda_bp.route("/<int:id>", methods=["GET"])
def getServicioAgenda(id):
    return ServicioAgendaController.cntGetServicioAgenda(id)


@servicio_agenda_bp.route("/", methods=["POST"])
def createServicioAgenda():
    return ServicioAgendaController.cntCreateServicioAgenda()


@servicio_agenda_bp.route("/<int:id>", methods=["PUT"])
def updateServicioAgenda(id):
    return ServicioAgendaController.cntUpdateServicioAgenda(id)


@servicio_agenda_bp.route("/<int:id>", methods=["DELETE"])
def deleteServicioAgenda(id):
    return ServicioAgendaController.cntDeleteServicioAgenda(id)
