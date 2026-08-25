from flask import Blueprint
from Controllers.consulta_controller import (
    cntListConsulta,
    cntGetConsulta,
    cntCreateConsulta,
    cntUpdateConsulta,
    cntDeleteConsulta
)


consulta_bp = Blueprint("consulta_bp", __name__)


@consulta_bp.route("/", methods=["GET"])
def listConsulta():
    return cntListConsulta()


@consulta_bp.route("/<int:id>", methods=["GET"])
def getConsulta(id):
    return cntGetConsulta(id)


@consulta_bp.route("/", methods=["POST"])
def createConsulta():
    return cntCreateConsulta()


@consulta_bp.route("/<int:id>", methods=["PUT"])
def updateConsulta(id):
    return cntUpdateConsulta(id)


@consulta_bp.route("/<int:id>", methods=["DELETE"])
def deleteConsulta(id):
    return cntDeleteConsulta(id)
