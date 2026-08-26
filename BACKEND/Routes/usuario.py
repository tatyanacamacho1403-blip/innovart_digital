from flask import Blueprint
from Controllers.usuario_controller import UsuarioController


usuario_bp = Blueprint("usuario_bp", __name__)


@usuario_bp.route("/", methods=["GET"])
def listUsuario():
    return UsuarioController.cntListUsuario()


@usuario_bp.route("/<int:id>", methods=["GET"])
def getUsuario(id):
    return UsuarioController.cntGetUsuario(id)


@usuario_bp.route("/", methods=["POST"])
def createUsuario():
    return UsuarioController.cntCreateUsuario()


@usuario_bp.route("/<int:id>", methods=["PUT"])
def updateUsuario(id):
    return UsuarioController.cntUpdateUsuario(id)


@usuario_bp.route("/<int:id>", methods=["DELETE"])
def deleteUsuario(id):
    return UsuarioController.cntDeleteUsuario(id)
