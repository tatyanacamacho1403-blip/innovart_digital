from flask import Blueprint
from Controllers.usuario_controller import (
    cntListUsuario,
    cntGetUsuario,
    cntCreateUsuario,
    cntUpdateUsuario,
    cntDeleteUsuario
)

usuario_bp = Blueprint('usuario_bp', __name__)


@usuario_bp.route('/', methods=['GET'])
def listUsuario():
    x = cntListUsuario()
    return x


@usuario_bp.route('/<int:id>', methods=['GET'])
def getUsuario(id):
    x = cntGetUsuario(id)
    return x


@usuario_bp.route('/', methods=['POST'])
def createUsuario():
    x = cntCreateUsuario()
    return x


@usuario_bp.route('/<int:id>', methods=['PUT'])
def updateUsuario(id):
    x = cntUpdateUsuario(id)
    return x


@usuario_bp.route('/<int:id>', methods=['DELETE'])
def deleteUsuario(id):
    x = cntDeleteUsuario(id)
    return x
