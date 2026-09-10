from flask import Blueprint
from Controllers.pago_controller import (
    cntListPago,
    cntGetPago,
    cntCreatePago,
    cntUpdatePago,
    cntDeletePago
)

pago_bp = Blueprint('pago_bp', __name__)


@pago_bp.route('/', methods=['GET'])
def listPago():
    x = cntListPago()
    return x


@pago_bp.route('/<int:id>', methods=['GET'])
def getPago(id):
    x = cntGetPago(id)
    return x


@pago_bp.route('/', methods=['POST'])
def createPago():
    x = cntCreatePago()
    return x


@pago_bp.route('/<int:id>', methods=['PUT'])
def updatePago(id):
    x = cntUpdatePago(id)
    return x


@pago_bp.route('/<int:id>', methods=['DELETE'])
def deletePago(id):
    x = cntDeletePago(id)
    return x
