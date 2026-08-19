from flask import request, jsonify
from Services.persona_services import (servListPersona, servGetPersona, addPersona, upPersona, delPersona,)

def cntListPersona():  
    data = servListPersona()
    return jsonify(data), 200

def cntGetPersona(id):
    data = servGetPersona(id)

    if data is None:
        return jsonify({"error": "persona no encontrado"}), 404
    return jsonify(data), 200


def cntCreatePersona():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = addPersona(data)
    return jsonify(data), 201


def cntUpdatePersona(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = upPersona(id, data)

    if data is None:
        return jsonify({"error": "persona no encontrado"}), 404

    return jsonify(data), 200


def cntDeletePersona(id):
    if not delPersona(id):
        return jsonify({"error": "persona no encontrado"}), 404
    return jsonify({"message": "persona eliminado correctamente"}), 200

