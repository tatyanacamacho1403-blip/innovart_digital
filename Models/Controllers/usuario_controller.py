from flask import request, jsonify
from Services.usuario_services import (
    servListUsuario,
    servGetUsuario,
    addUsuario,
    upUsuario,
    delUsuario,
)


def cntListUsuario():
    return jsonify(servListUsuario()), 200


def cntGetUsuario(id):
    data = servGetUsuario(id)

    if data is None:
        return jsonify({"error": "usuario no encontrado"}), 404

    return jsonify(data), 200


def cntCreateUsuario():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = addUsuario(data)
    return jsonify(data), 201


def cntUpdateUsuario(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    data = upUsuario(id, data)

    if data is None:
        return jsonify({"error": "usuario no encontrado"}), 404

    return jsonify(data), 200


def cntDeleteUsuario(id):
    if not delUsuario(id):
        return jsonify({"error": "usuario no encontrado"}), 404

    return jsonify({"message": "usuario eliminado correctamente"}), 200
