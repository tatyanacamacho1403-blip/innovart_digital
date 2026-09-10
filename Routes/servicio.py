from flask import Blueprint
from Controllers.servicio_controller import (
    cntListServicio,
    cntGetServicio,
    cntCreateServicio,
    cntUpdateServicio,
    cntDeleteServicio
)

servicio_bp = Blueprint('servicio_bp', __name__)


@servicio_bp.route('/', methods=['GET'])
def listServicio():
    x = cntListServicio()
    return x


@servicio_bp.route('/<int:id>', methods=['GET'])
def getServicio(id):
    x = cntGetServicio(id)
    return x


@servicio_bp.route('/', methods=['POST'])
def createServicio():
    x = cntCreateServicio()
    return x


@servicio_bp.route('/<int:id>', methods=['PUT'])
def updateServicio(id):
    x = cntUpdateServicio(id)
    return x


@servicio_bp.route('/<int:id>', methods=['DELETE'])
def deleteServicio(id):
    x = cntDeleteServicio(id)
    return x
