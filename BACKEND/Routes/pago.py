from flask import Blueprint
from Controllers.pago_controller import PagoController


pago_bp = Blueprint("pago_bp", __name__)


@pago_bp.route("/", methods=["GET"])
def listPago():
    return PagoController.cntListPago()


@pago_bp.route("/<int:id>", methods=["GET"])
def getPago(id):
    return PagoController.cntGetPago(id)


@pago_bp.route("/", methods=["POST"])
def createPago():
    return PagoController.cntCreatePago()


@pago_bp.route("/<int:id>", methods=["PUT"])
def updatePago(id):
    return PagoController.cntUpdatePago(id)


@pago_bp.route("/<int:id>", methods=["DELETE"])
def deletePago(id):
    return PagoController.cntDeletePago(id)
