from flask import Blueprint
from Controllers.servicio_controller import ServicioController


servicio_bp = Blueprint("servicio_bp", __name__)


@servicio_bp.route("/", methods=["GET"])
def listServicio():
    return ServicioController.cntListServicio()


@servicio_bp.route("/<int:id>", methods=["GET"])
def getServicio(id):
    return ServicioController.cntGetServicio(id)


@servicio_bp.route("/", methods=["POST"])
def createServicio():
    return ServicioController.cntCreateServicio()


@servicio_bp.route("/<int:id>", methods=["PUT"])
def updateServicio(id):
    return ServicioController.cntUpdateServicio(id)


@servicio_bp.route("/<int:id>", methods=["DELETE"])
def deleteServicio(id):
    return ServicioController.cntDeleteServicio(id)
