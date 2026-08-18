from flask import Blueprint
from Controllers.persona_controller import (
    listPersona,
    getPersona,
    createPersona,
    updatePersona,
    deletePersona,
    searchUuidPersona
)

persona_bp = Blueprint("persona", __name__, url_prefix="/personas")


persona_bp.route("/", methods=["GET"])(listPersona)
persona_bp.route("/<int:id>", methods=["GET"])(getPersona)
persona_bp.route("/", methods=["POST"])(createPersona)
persona_bp.route("/<int:id>", methods=["PUT"])(updatePersona)
persona_bp.route("/<int:id>", methods=["DELETE"])(deletePersona)
persona_bp.route("/uuid/<uuid>", methods=["GET"])(searchUuidPersona)
