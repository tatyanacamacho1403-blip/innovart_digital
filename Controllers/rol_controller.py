from flask import request, jsonify
from Services.rol_services import (servListRol, servGetRol, addRol, upRol, delRol)


def cntListRol():

    data = servListRol()

    return jsonify(data), 200


def cntGetRol(id):

    data = servGetRol(id)

    if data is None:
        return jsonify({
            "error": "rol no encontrado"
        }), 404

    return jsonify(data), 200


def cntCreateRol():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Debe enviar un JSON"
        }), 400

    data = addRol(data)

    return jsonify(data), 201


def cntUpdateRol(id):

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Debe enviar un JSON"
        }), 400

    data = upRol(id, data)

    if data is None:
        return jsonify({
            "error": "rol no encontrado"
        }), 404

    return jsonify(data), 200


def cntDeleteRol(id):

    if not delRol(id):
        return jsonify({
            "error": "rol no encontrado"
        }), 404

    return jsonify({
        "message": "rol eliminado correctamente"
    }), 200
