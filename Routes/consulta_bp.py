from flask import Blueprint
from Controllers.consulta_controller import (
    cntListConsulta,
    cntGetConsulta,
    cntCreateConsulta,
    cntUpdateConsulta,
    cntDeleteConsulta
)

consulta_bp = Blueprint('consulta_bp', __name__)


@consulta_bp.route('/', methods=['GET'])
def listConsulta():
    x = cntListConsulta()
    return x


@consulta_bp.route('/<int:id>', methods=['GET'])
def getConsulta(id):
    x = cntGetConsulta(id)
    return x


@consulta_bp.route('/', methods=['POST'])
def createConsulta():
    x = cntCreateConsulta()
    return x


@consulta_bp.route('/<int:id>', methods=['PUT'])
def updateConsulta(id):
    x = cntUpdateConsulta(id)
    return x


@consulta_bp.route('/<int:id>', methods=['DELETE'])
def deleteConsulta(id):
    x = cntDeleteConsulta(id)
    return x
