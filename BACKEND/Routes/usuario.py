from flask import Blueprint
from Controllers.usuario_controller import (
    cntListUsuario,
    cntGetUsuario,
    cntCreateUsuario,
    cntUpdateUsuario,
    cntDeleteUsuario
)


usuario_bp = Blueprint("usuario_bp", __name__)


@usuario_bp.route("/", methods=["GET"])
def listUsuario():
    return cntListUsuario()


@usuario_bp.route("/<int:id>", methods=["GET"])
def getUsuario(id):
    return cntGetUsuario(id)


@usuario_bp.route("/", methods=["POST"])
def createUsuario():
    return cntCreateUsuario()


@usuario_bp.route("/<int:id>", methods=["PUT"])
def updateUsuario(id):
    return cntUpdateUsuario(id)


@usuario_bp.route("/<int:id>", methods=["DELETE"])
def deleteUsuario(id):
    return cntDeleteUsuario(id)
