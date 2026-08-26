from flask import Blueprint
from Controllers.agenda_controller import AgendaController


agenda_bp = Blueprint("agenda_bp", __name__)


@agenda_bp.route("/", methods=["GET"])
def listAgenda():
    return AgendaController.cntListAgenda()


@agenda_bp.route("/<int:id>", methods=["GET"])
def getAgenda(id):
    return AgendaController.cntGetAgenda(id)


@agenda_bp.route("/", methods=["POST"])
def createAgenda():
    return AgendaController.cntCreateAgenda()


@agenda_bp.route("/<int:id>", methods=["PUT"])
def updateAgenda(id):
    return AgendaController.cntUpdateAgenda(id)


@agenda_bp.route("/<int:id>", methods=["DELETE"])
def deleteAgenda(id):
    return AgendaController.cntDeleteAgenda(id)
