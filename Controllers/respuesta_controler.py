from flask import request, jsonify

from Services.respuesta_services import (
    servListRespuesta,
    servGetRespuesta,
    addRespuesta,
    upRespuesta,
    delRespuesta
)


def cntListRespuesta():

    data = servListRespuesta()

    return jsonify(data), 200


def cntGetRespuesta(id):

    data = servGetRespuesta(id)

    if data is None:
        return jsonify({
            "error": "respuesta no encontrada"
        }), 404

    return jsonify(data), 200


def cntCreateRespuesta():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Debe enviar un JSON"
        }), 400

    data = addRespuesta(data)

    return jsonify(data), 201


def cntUpdateRespuesta(id):

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Debe enviar un JSON"
        }), 400

    data = upRespuesta(id, data)

    if data is None:
        return jsonify({
            "error": "respuesta no encontrada"
        }), 404

    return jsonify(data), 200


def cntDeleteRespuesta(id):

    if not delRespuesta(id):
        return jsonify({
            "error": "respuesta no encontrada"
        }), 404

    return jsonify({
        "message": "respuesta eliminada correctamente"
    }), 200