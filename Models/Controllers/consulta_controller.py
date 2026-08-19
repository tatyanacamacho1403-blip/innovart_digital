from flask import request, jsonify
from Services.consulta_services import (
    servListConsulta,
    servGetConsulta,
    addConsulta,
    upConsulta,
    delConsulta,
)

def cntListConsulta():
    return jsonify(servListConsulta()), 200


def cntGetConsulta(id):
    data = servGetConsulta(id)

    if data is None:
        return jsonify({"error": "consulta no encontrada"}), 404

    return jsonify(data), 200


def cntCreateConsulta():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = addConsulta(data)
    return jsonify(data), 201


def cntUpdateConsulta(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = upConsulta(id, data)

    if data is None:
        return jsonify({"error": "consulta no encontrado"}), 404

    return jsonify(data), 200


def cntDeleteConsulta(id):
    if not delConsulta(id):
        return jsonify({"error": "consulta no encontrado"}), 404

    return jsonify({"message": "consulta eliminado correctamente"}), 200
