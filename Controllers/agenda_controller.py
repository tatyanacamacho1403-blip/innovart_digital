from flask import request, jsonify
from Services.agenda_services import (
    servListAgenda,
    servGetAgenda,
    addAgenda,
    upAgenda,
    delAgenda,
    searchByUuidAgenda
)


def listAgenda():
    return jsonify(servListAgenda()), 200


def getAgenda(id):
    data = servGetAgenda(id)

    if data is None:
        return jsonify({"error": "agenda no encontrado"}), 404

    return jsonify(data), 200


def createAgenda():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = addAgenda(data)
    return jsonify(data), 201


def updateAgenda(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = upAgenda(id, data)

    if data is None:
        return jsonify({"error": "agenda no encontrado"}), 404

    return jsonify(data), 200


def deleteAgenda(id):
    if not delAgenda(id):
        return jsonify({"error": "agenda no encontrado"}), 404

    return jsonify({"message": "agenda eliminado correctamente"}), 200


def searchUuidAgenda(uuid):
    data = searchByUuidAgenda(uuid)

    if data is None:
        return jsonify({"error": "agenda no encontrado"}), 404

    return jsonify(data), 200
