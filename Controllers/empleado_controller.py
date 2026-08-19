from flask import request, jsonify
from Services.empleado_services import (
    servListEmpleado,
    servGetEmpleado,
    addEmpleado,
    upEmpleado,
    delEmpleado,
)


def cntListEmpleado():
    return jsonify(servListEmpleado()), 200


def cntGetEmpleado(id):
    data = servGetEmpleado(id)

    if data is None:
        return jsonify({"error": "empleado no encontrado"}), 404

    return jsonify(data), 200


def cntCreateEmpleado():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = addEmpleado(data)
    return jsonify(data), 201


def cntUpdateEmpleado(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = upEmpleado(id, data)

    if data is None:
        return jsonify({"error": "empleado no encontrado"}), 404

    return jsonify(data), 200


def cntDeleteEmpleado(id):
    if not delEmpleado(id):
        return jsonify({"error": "empleado no encontrado"}), 404

    return jsonify({"message": "empleado eliminado correctamente"}), 200