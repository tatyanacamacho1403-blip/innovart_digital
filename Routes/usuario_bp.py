from flask import Blueprint
from Controllers.usuario_controller import (
    listUsuario,
    getUsuario,
    createUsuario,
    updateUsuario,
    deleteUsuario,
    searchUuidUsuario
)

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


usuario_bp.route("/", methods=["GET"])(listUsuario)
usuario_bp.route("/<int:id>", methods=["GET"])(getUsuario)
usuario_bp.route("/", methods=["POST"])(createUsuario)
usuario_bp.route("/<int:id>", methods=["PUT"])(updateUsuario)
usuario_bp.route("/<int:id>", methods=["DELETE"])(deleteUsuario)
usuario_bp.route("/uuid/<uuid>", methods=["GET"])(searchUuidUsuario)
