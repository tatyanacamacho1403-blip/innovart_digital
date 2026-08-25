from flask import Blueprint
from Controllers.pago_controller import (
    cntListPago,
    cntGetPago,
    cntCreatePago,
    cntUpdatePago,
    cntDeletePago
)


pago_bp = Blueprint("pago_bp", __name__)


@pago_bp.route("/", methods=["GET"])
def listPago():
    return cntListPago()


@pago_bp.route("/<int:id>", methods=["GET"])
def getPago(id):
    return cntGetPago(id)


@pago_bp.route("/", methods=["POST"])
def createPago():
    return cntCreatePago()


@pago_bp.route("/<int:id>", methods=["PUT"])
def updatePago(id):
    return cntUpdatePago(id)


@pago_bp.route("/<int:id>", methods=["DELETE"])
def deletePago(id):
    return cntDeletePago(id)
