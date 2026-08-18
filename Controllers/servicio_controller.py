from flask import request, jsonify
from Services.servicio_services import (
    servListServicio,
    servGetServicio,
    addServicio,
    upServicio,
    delServicio,
    searchByUuidServicio
)


def listServicio():
    return jsonify(servListServicio()), 200


def getServicio(id):
    data = servGetServicio(id)

    if data is None:
        return jsonify({"error": "servicio no encontrado"}), 404

    return jsonify(data), 200


def createServicio():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = addServicio(data)
    return jsonify(data), 201


def updateServicio(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = upServicio(id, data)

    if data is None:
        return jsonify({"error": "servicio no encontrado"}), 404

    return jsonify(data), 200


def deleteServicio(id):
    if not delServicio(id):
        return jsonify({"error": "servicio no encontrado"}), 404

    return jsonify({"message": "servicio eliminado correctamente"}), 200


def searchUuidServicio(uuid):
    data = searchByUuidServicio(uuid)

    if data is None:
        return jsonify({"error": "servicio no encontrado"}), 404

    return jsonify(data), 200
