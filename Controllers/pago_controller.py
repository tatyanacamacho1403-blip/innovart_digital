from flask import request, jsonify
from Services.pago_services import (
    servListPago,
    servGetPago,
    addPago,
    upPago,
    delPago,
    searchByUuidPago
)


def listPago():
    return jsonify(servListPago()), 200


def getPago(id):
    data = servGetPago(id)

    if data is None:
        return jsonify({"error": "pago no encontrado"}), 404

    return jsonify(data), 200


def createPago():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = addPago(data)
    return jsonify(data), 201


def updatePago(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = upPago(id, data)

    if data is None:
        return jsonify({"error": "pago no encontrado"}), 404

    return jsonify(data), 200


def deletePago(id):
    if not delPago(id):
        return jsonify({"error": "pago no encontrado"}), 404

    return jsonify({"message": "pago eliminado correctamente"}), 200


def searchUuidPago(uuid):
    data = searchByUuidPago(uuid)

    if data is None:
        return jsonify({"error": "pago no encontrado"}), 404

    return jsonify(data), 200
