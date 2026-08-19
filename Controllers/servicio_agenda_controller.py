from flask import request, jsonify
from Services.servicio_agenda_services import (servListServicioAgenda, servGetServicioAgenda, addServicioAgenda, upServicioAgenda, delServicioAgenda)


def cntListServicioAgenda():

    data = servListServicioAgenda()

    return jsonify(data), 200


def cntGetServicioAgenda(id):

    data = servGetServicioAgenda(id)

    if data is None:
        return jsonify({
            "error": "servicio agenda no encontrado"
        }), 404

    return jsonify(data), 200


def cntCreateServicioAgenda():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Debe enviar un JSON"
        }), 400

    data = addServicioAgenda(data)

    return jsonify(data), 201


def cntUpdateServicioAgenda(id):

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Debe enviar un JSON"
        }), 400

    data = upServicioAgenda(id, data)

    if data is None:
        return jsonify({
            "error": "servicio agenda no encontrado"
        }), 404

    return jsonify(data), 200


def cntDeleteServicioAgenda(id):

    if not delServicioAgenda(id):
        return jsonify({
            "error": "servicio agenda no encontrado"
        }), 404

    return jsonify({
        "message": "servicio agenda eliminado correctamente"
    }), 200
