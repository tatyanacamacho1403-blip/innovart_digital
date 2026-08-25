from flask import request, jsonify
from Services.agenda_services import agenda


def cntListAgenda():
    return jsonify(servListAgenda()), 200


def cntGetAgenda(id):
    data = servGetAgenda(id)

    if data is None:
        return jsonify({"error": "agenda no encontrado"}), 404

    return jsonify(data), 200


def cntCreateAgenda():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    result = addAgenda(data)
    return jsonify(result), 201


def cntUpdateAgenda(id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Debe enviar un JSON"}), 400

    result = upAgenda(id, data)

    if result is None:
        return jsonify({"error": "agenda no encontrado"}), 404

    return jsonify(result), 200


def cntDeleteAgenda(id):
    if not delAgenda(id):
        return jsonify({"error": "agenda no encontrado"}), 404

    return jsonify({"message": "agenda eliminado correctamente"}), 200
