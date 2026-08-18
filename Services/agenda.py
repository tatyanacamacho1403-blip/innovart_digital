from flask import Blueprint
from Controllers.agenda_controller import (
    listAgenda,
    getAgenda,
    createAgenda,
    updateAgenda,
    deleteAgenda,
    searchUuidAgenda
)

agenda_bp = Blueprint("agenda", __name__, url_prefix="/agendas")


agenda_bp.route("/", methods=["GET"])(listAgenda)
agenda_bp.route("/<int:id>", methods=["GET"])(getAgenda)
agenda_bp.route("/", methods=["POST"])(createAgenda)
agenda_bp.route("/<int:id>", methods=["PUT"])(updateAgenda)
agenda_bp.route("/<int:id>", methods=["DELETE"])(deleteAgenda)
agenda_bp.route("/uuid/<uuid>", methods=["GET"])(searchUuidAgenda)
