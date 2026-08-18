from flask import request, jsonify
from Services.empleado_services import (
    servListEmpleado,
    servGetEmpleado,
    addEmpleado,
    upEmpleado,
    delEmpleado,
    searchByUuidEmpleado
)


def listEmpleado():
    return jsonify(servListEmpleado()), 200


def getEmpleado(id):
    data = servGetEmpleado(id)

    if data is None:
        return jsonify({"error": "empleado no encontrado"}), 404

    return jsonify(data), 200


def createEmpleado():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = addEmpleado(data)
    return jsonify(data), 201


def updateEmpleado(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = upEmpleado(id, data)

    if data is None:
        return jsonify({"error": "empleado no encontrado"}), 404

    return jsonify(data), 200


def deleteEmpleado(id):
    if not delEmpleado(id):
        return jsonify({"error": "empleado no encontrado"}), 404

    return jsonify({"message": "empleado eliminado correctamente"}), 200


def searchUuidEmpleado(uuid):
    data = searchByUuidEmpleado(uuid)

    if data is None:
        return jsonify({"error": "empleado no encontrado"}), 404

    return jsonify(data), 200
