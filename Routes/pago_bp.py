from flask import Blueprint
from Controllers.pago_controller import (
    listPago,
    getPago,
    createPago,
    updatePago,
    deletePago,
    searchUuidPago
)

pago_bp = Blueprint("pago", __name__, url_prefix="/pagos")


pago_bp.route("/", methods=["GET"])(listPago)
pago_bp.route("/<int:id>", methods=["GET"])(getPago)
pago_bp.route("/", methods=["POST"])(createPago)
pago_bp.route("/<int:id>", methods=["PUT"])(updatePago)
pago_bp.route("/<int:id>", methods=["DELETE"])(deletePago)
pago_bp.route("/uuid/<uuid>", methods=["GET"])(searchUuidPago)
