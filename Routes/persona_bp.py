from flask import Blueprint
from Controllers.persona_controller import (cntListPersona, cntGetPersona, cntCreatePersona, cntUpdatePersona, cntDeletePersona)

persona_bp = Blueprint('persona_bp', __name__)


@persona_bp.route('/', methods=['GET'])
def listPersona():
    x = cntListPersona()
    return x


@persona_bp.route('/<int:id>', methods=['GET'])
def getPersona(id):
    x = cntGetPersona(id)
    return x


@persona_bp.route('/', methods=['POST'])
def createPersona():
    x = cntCreatePersona()
    return x


@persona_bp.route('/<int:id>', methods=['PUT'])
def updatePersona(id):
    x = cntUpdatePersona(id)
    return x


@persona_bp.route('/<int:id>', methods=['DELETE'])
def deletePersona(id):
    x = cntDeletePersona(id)
    return x
