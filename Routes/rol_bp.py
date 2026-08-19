from flask import Blueprint
from Controllers.rol_controller import (
    cntListRol,
    cntGetRol,
    cntCreateRol,
    cntUpdateRol,
    cntDeleteRol
)

rol_bp = Blueprint('rol_bp', __name__)


@rol_bp.route('/', methods=['GET'])
def listRol():
    x = cntListRol()
    return x


@rol_bp.route('/<int:id>', methods=['GET'])
def getRol(id):
    x = cntGetRol(id)
    return x


@rol_bp.route('/', methods=['POST'])
def createRol():
    x = cntCreateRol()
    return x


@rol_bp.route('/<int:id>', methods=['PUT'])
def updateRol(id):
    x = cntUpdateRol(id)
    return x


@rol_bp.route('/<int:id>', methods=['DELETE'])
def deleteRol(id):
    x = cntDeleteRol(id)
    return x
