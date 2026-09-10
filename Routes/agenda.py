from flask import Blueprint
from Controllers.agenda_controller import (
    cntListAgenda,
    cntGetAgenda,
    cntCreateAgenda,
    cntUpdateAgenda,
    cntDeleteAgenda
)

agenda_bp = Blueprint('agenda_bp', __name__)


@agenda_bp.route('/', methods=['GET'])
def listAgenda():
    x = cntListAgenda()
    return x


@agenda_bp.route('/<int:id>', methods=['GET'])
def getAgenda(id):
    x = cntGetAgenda(id)
    return x


@agenda_bp.route('/', methods=['POST'])
def createAgenda():
    x = cntCreateAgenda()
    return x


@agenda_bp.route('/<int:id>', methods=['PUT'])
def updateAgenda(id):
    x = cntUpdateAgenda(id)
    return x


@agenda_bp.route('/<int:id>', methods=['DELETE'])
def deleteAgenda(id):
    x = cntDeleteAgenda(id)
    return x
