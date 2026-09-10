from flask import Blueprint
from Controllers.empleado_controller import (
    cntListEmpleado,
    cntGetEmpleado,
    cntCreateEmpleado,
    cntUpdateEmpleado,
    cntDeleteEmpleado
)

empleado_bp = Blueprint('empleado_bp', __name__)


@empleado_bp.route('/', methods=['GET'])
def listEmpleado():
    x = cntListEmpleado()
    return x


@empleado_bp.route('/<int:id>', methods=['GET'])
def getEmpleado(id):
    x = cntGetEmpleado(id)
    return x


@empleado_bp.route('/', methods=['POST'])
def createEmpleado():
    x = cntCreateEmpleado()
    return x


@empleado_bp.route('/<int:id>', methods=['PUT'])
def updateEmpleado(id):
    x = cntUpdateEmpleado(id)
    return x


@empleado_bp.route('/<int:id>', methods=['DELETE'])
def deleteEmpleado(id):
    x = cntDeleteEmpleado(id)
    return x
