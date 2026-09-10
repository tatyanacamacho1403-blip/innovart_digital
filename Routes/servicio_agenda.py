from flask import Blueprint
from Controllers.servicio_agenda_controller import (
    cntListServicioAgenda,
    cntGetServicioAgenda,
    cntCreateServicioAgenda,
    cntUpdateServicioAgenda,
    cntDeleteServicioAgenda
)

servicio_agenda_bp = Blueprint('servicio_agenda_bp', __name__)


@servicio_agenda_bp.route('/', methods=['GET'])
def listServicioAgenda():
    x = cntListServicioAgenda()
    return x


@servicio_agenda_bp.route('/<int:id>', methods=['GET'])
def getServicioAgenda(id):
    x = cntGetServicioAgenda(id)
    return x


@servicio_agenda_bp.route('/', methods=['POST'])
def createServicioAgenda():
    x = cntCreateServicioAgenda()
    return x


@servicio_agenda_bp.route('/<int:id>', methods=['PUT'])
def updateServicioAgenda(id):
    x = cntUpdateServicioAgenda(id)
    return x


@servicio_agenda_bp.route('/<int:id>', methods=['DELETE'])
def deleteServicioAgenda(id):
    x = cntDeleteServicioAgenda(id)
    return x
