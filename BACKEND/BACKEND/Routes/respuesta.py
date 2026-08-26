from flask import Blueprint
from Controllers.respuesta_controller import RespuestaController


respuesta_bp = Blueprint("respuesta_bp", __name__)


@respuesta_bp.route("/", methods=["GET"])
def listRespuesta():
    return RespuestaController.cntListRespuesta()


@respuesta_bp.route("/<int:id>", methods=["GET"])
def getRespuesta(id):
    return RespuestaController.cntGetRespuesta(id)


@respuesta_bp.route("/", methods=["POST"])
def createRespuesta():
    return RespuestaController.cntCreateRespuesta()


@respuesta_bp.route("/<int:id>", methods=["PUT"])
def updateRespuesta(id):
    return RespuestaController.cntUpdateRespuesta(id)


@respuesta_bp.route("/<int:id>", methods=["DELETE"])
def deleteRespuesta(id):
    return RespuestaController.cntDeleteRespuesta(id)
