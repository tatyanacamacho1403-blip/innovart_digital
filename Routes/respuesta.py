from flask import Blueprint
from Controllers.respuesta_controller import (
    cntListRespuesta,
    cntGetRespuesta,
    cntCreateRespuesta,
    cntUpdateRespuesta,
    cntDeleteRespuesta
)

respuesta_bp = Blueprint('respuesta_bp', __name__)


@respuesta_bp.route('/', methods=['GET'])
def listRespuesta():
    x = cntListRespuesta()
    return x


@respuesta_bp.route('/<int:id>', methods=['GET'])
def getRespuesta(id):
    x = cntGetRespuesta(id)
    return x


@respuesta_bp.route('/', methods=['POST'])
def createRespuesta():
    x = cntCreateRespuesta()
    return x


@respuesta_bp.route('/<int:id>', methods=['PUT'])
def updateRespuesta(id):
    x = cntUpdateRespuesta(id)
    return x


@respuesta_bp.route('/<int:id>', methods=['DELETE'])
def deleteRespuesta(id):
    x = cntDeleteRespuesta(id)
    return x
