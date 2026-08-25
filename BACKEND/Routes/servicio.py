from flask import Blueprint
from Controllers.servicio_controller import (
    cntListServicio,
    cntGetServicio,
    cntCreateServicio,
    cntUpdateServicio,
    cntDeleteServicio
)


servicio_bp = Blueprint("servicio_bp", __name__)


@servicio_bp.route("/", methods=["GET"])
def listServicio():
    return cntListServicio()


@servicio_bp.route("/<int:id>", methods=["GET"])
def getServicio(id):
    return cntGetServicio(id)


@servicio_bp.route("/", methods=["POST"])
def createServicio():
    return cntCreateServicio()


@servicio_bp.route("/<int:id>", methods=["PUT"])
def updateServicio(id):
    return cntUpdateServicio(id)


@servicio_bp.route("/<int:id>", methods=["DELETE"])
def deleteServicio(id):
    return cntDeleteServicio(id)
