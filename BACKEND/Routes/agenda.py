from flask import Blueprint
from Controllers.agenda_controller import (
    cntListAgenda,
    cntGetAgenda,
    cntCreateAgenda,
    cntUpdateAgenda,
    cntDeleteAgenda
)


agenda_bp = Blueprint("agenda_bp", __name__)


@agenda_bp.route("/", methods=["GET"])
def listAgenda():
    return cntListAgenda()


@agenda_bp.route("/<int:id>", methods=["GET"])
def getAgenda(id):
    return cntGetAgenda(id)


@agenda_bp.route("/", methods=["POST"])
def createAgenda():
    return cntCreateAgenda()


@agenda_bp.route("/<int:id>", methods=["PUT"])
def updateAgenda(id):
    return cntUpdateAgenda(id)


@agenda_bp.route("/<int:id>", methods=["DELETE"])
def deleteAgenda(id):
    return cntDeleteAgenda(id)
