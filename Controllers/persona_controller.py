from flask import request, jsonify
from Services.persona_services import (
    servListPersona,
    servGetPersona,
    addPersona,
    upPersona,
    delPersona,
    searchByUuidPersona
)


def listPersona():
    return jsonify(servListPersona()), 200


def getPersona(id):
    data = servGetPersona(id)

    if data is None:
        return jsonify({"error": "persona no encontrado"}), 404

    return jsonify(data), 200


def createPersona():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = addPersona(data)
    return jsonify(data), 201


def updatePersona(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = upPersona(id, data)

    if data is None:
        return jsonify({"error": "persona no encontrado"}), 404

    return jsonify(data), 200


def deletePersona(id):
    if not delPersona(id):
        return jsonify({"error": "persona no encontrado"}), 404

    return jsonify({"message": "persona eliminado correctamente"}), 200


def searchUuidPersona(uuid):
    data = searchByUuidPersona(uuid)

    if data is None:
        return jsonify({"error": "persona no encontrado"}), 404

    return jsonify(data), 200
