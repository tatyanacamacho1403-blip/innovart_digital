from flask import Blueprint
from Controllers.rol_controller import RolController


rol_bp = Blueprint("rol_bp", __name__)


@rol_bp.route("/", methods=["GET"])
def listRol():
    return RolController.cntListRol()


@rol_bp.route("/<int:id>", methods=["GET"])
def getRol(id):
    return RolController.cntGetRol(id)


@rol_bp.route("/", methods=["POST"])
def createRol():
    return RolController.cntCreateRol()


@rol_bp.route("/<int:id>", methods=["PUT"])
def updateRol(id):
    return RolController.cntUpdateRol(id)


@rol_bp.route("/<int:id>", methods=["DELETE"])
def deleteRol(id):
    return RolController.cntDeleteRol(id)
