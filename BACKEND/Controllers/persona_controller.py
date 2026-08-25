from flask import request, jsonify
from Services.persona_services import (
    servListPersona,
    servGetPersona,
    addPersona,
    upPersona,
    delPersona
)


def cntListPersona():
    return jsonify(servListPersona()), 200


def cntGetPersona(id):
    data = servGetPersona(id)

    if data is None:
        return jsonify({"error": "persona no encontrado"}), 404

    return jsonify(data), 200


def cntCreatePersona():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    result = addPersona(data)
    return jsonify(result), 201


def cntUpdatePersona(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    result = upPersona(id, data)

    if result is None:
        return jsonify({"error": "persona no encontrado"}), 404

    return jsonify(result), 200


def cntDeletePersona(id):
    if not delPersona(id):
        return jsonify({"error": "persona no encontrado"}), 404

    return jsonify({"message": "persona eliminado correctamente"}), 200
