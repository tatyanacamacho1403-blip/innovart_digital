from flask import Blueprint
from Controllers.empleado_controller import (
    cntListEmpleado,
    cntGetEmpleado,
    cntCreateEmpleado,
    cntUpdateEmpleado,
    cntDeleteEmpleado
)


empleado_bp = Blueprint("empleado_bp", __name__)


@empleado_bp.route("/", methods=["GET"])
def listEmpleado():
    return cntListEmpleado()


@empleado_bp.route("/<int:id>", methods=["GET"])
def getEmpleado(id):
    return cntGetEmpleado(id)


@empleado_bp.route("/", methods=["POST"])
def createEmpleado():
    return cntCreateEmpleado()


@empleado_bp.route("/<int:id>", methods=["PUT"])
def updateEmpleado(id):
    return cntUpdateEmpleado(id)


@empleado_bp.route("/<int:id>", methods=["DELETE"])
def deleteEmpleado(id):
    return cntDeleteEmpleado(id)
