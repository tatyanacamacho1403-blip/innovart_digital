from flask import Blueprint
from Controllers.persona_controller import (
    cntListPersona,
    cntGetPersona,
    cntCreatePersona,
    cntUpdatePersona,
    cntDeletePersona
)


persona_bp = Blueprint("persona_bp", __name__)


@persona_bp.route("/", methods=["GET"])
def listPersona():
    return cntListPersona()


@persona_bp.route("/<int:id>", methods=["GET"])
def getPersona(id):
    return cntGetPersona(id)


@persona_bp.route("/", methods=["POST"])
def createPersona():
    return cntCreatePersona()


@persona_bp.route("/<int:id>", methods=["PUT"])
def updatePersona(id):
    return cntUpdatePersona(id)


@persona_bp.route("/<int:id>", methods=["DELETE"])
def deletePersona(id):
    return cntDeletePersona(id)
