from flask import Blueprint
from Controllers.consulta_controller import ConsultaController


consulta_bp = Blueprint("consulta_bp", __name__)


@consulta_bp.route("/", methods=["GET"])
def listConsulta():
    return ConsultaController.cntListConsulta()


@consulta_bp.route("/<int:id>", methods=["GET"])
def getConsulta(id):
    return ConsultaController.cntGetConsulta(id)


@consulta_bp.route("/", methods=["POST"])
def createConsulta():
    return ConsultaController.cntCreateConsulta()


@consulta_bp.route("/<int:id>", methods=["PUT"])
def updateConsulta(id):
    return ConsultaController.cntUpdateConsulta(id)


@consulta_bp.route("/<int:id>", methods=["DELETE"])
def deleteConsulta(id):
    return ConsultaController.cntDeleteConsulta(id)
