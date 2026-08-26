from flask import Blueprint
from Controllers.empleado_controller import EmpleadoController


empleado_bp = Blueprint("empleado_bp", __name__)


@empleado_bp.route("/", methods=["GET"])
def listEmpleado():
    return EmpleadoController.cntListEmpleado()


@empleado_bp.route("/<int:id>", methods=["GET"])
def getEmpleado(id):
    return EmpleadoController.cntGetEmpleado(id)


@empleado_bp.route("/", methods=["POST"])
def createEmpleado():
    return EmpleadoController.cntCreateEmpleado()


@empleado_bp.route("/<int:id>", methods=["PUT"])
def updateEmpleado(id):
    return EmpleadoController.cntUpdateEmpleado(id)


@empleado_bp.route("/<int:id>", methods=["DELETE"])
def deleteEmpleado(id):
    return EmpleadoController.cntDeleteEmpleado(id)
