from flask import Blueprint
from Controllers.servicio_controller import (
    listServicio,
    getServicio,
    createServicio,
    updateServicio,
    deleteServicio,
    searchUuidServicio
)

servicio_bp = Blueprint("servicio", __name__, url_prefix="/servicios")


servicio_bp.route("/", methods=["GET"])(listServicio)
servicio_bp.route("/<int:id>", methods=["GET"])(getServicio)
servicio_bp.route("/", methods=["POST"])(createServicio)
servicio_bp.route("/<int:id>", methods=["PUT"])(updateServicio)
servicio_bp.route("/<int:id>", methods=["DELETE"])(deleteServicio)
servicio_bp.route("/uuid/<uuid>", methods=["GET"])(searchUuidServicio)
