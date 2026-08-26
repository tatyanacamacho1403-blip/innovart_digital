from flask import Blueprint
from Controllers.persona_controller import PersonaController


persona_bp = Blueprint("persona_bp", __name__)


@persona_bp.route("/", methods=["GET"])
def listPersona():
    return PersonaController.cntListPersona()


@persona_bp.route("/<int:id>", methods=["GET"])
def getPersona(id):
    return PersonaController.cntGetPersona(id)


@persona_bp.route("/", methods=["POST"])
def createPersona():
    return PersonaController.cntCreatePersona()


@persona_bp.route("/<int:id>", methods=["PUT"])
def updatePersona(id):
    return PersonaController.cntUpdatePersona(id)


@persona_bp.route("/<int:id>", methods=["DELETE"])
def deletePersona(id):
    return PersonaController.cntDeletePersona(id)
