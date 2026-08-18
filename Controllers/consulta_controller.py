from flask import request, jsonify
from Services.consulta_services import (
    servListConsulta,
    servGetConsulta,
    addConsulta,
    upConsulta,
    delConsulta,
    searchByUuidConsulta
)


def listConsulta():
    return jsonify(servListConsulta()), 200


def getConsulta(id):
    data = servGetConsulta(id)

    if data is None:
        return jsonify({"error": "consulta no encontrado"}), 404

    return jsonify(data), 200


def createConsulta():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = addConsulta(data)
    return jsonify(data), 201


def updateConsulta(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = upConsulta(id, data)

    if data is None:
        return jsonify({"error": "consulta no encontrado"}), 404

    return jsonify(data), 200


def deleteConsulta(id):
    if not delConsulta(id):
        return jsonify({"error": "consulta no encontrado"}), 404

    return jsonify({"message": "consulta eliminado correctamente"}), 200


def searchUuidConsulta(uuid):
    data = searchByUuidConsulta(uuid)

    if data is None:
        return jsonify({"error": "consulta no encontrado"}), 404

    return jsonify(data), 200
