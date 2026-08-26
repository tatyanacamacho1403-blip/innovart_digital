from flask import request, jsonify
from Services.respuesta_services import (
    servListRespuesta,
    servGetRespuesta,
    addRespuesta,
    upRespuesta,
    delRespuesta
)


class RespuestaController:

    @staticmethod
    def cntListRespuesta():
        return jsonify(servListRespuesta()), 200


    @staticmethod
    def cntGetRespuesta(id):
        data = servGetRespuesta(id)

        if data is None:
            return jsonify({"error": "respuesta no encontrado"}), 404

        return jsonify(data), 200


    @staticmethod
    def cntCreateRespuesta():
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = addRespuesta(data)
        return jsonify(result), 201


    @staticmethod
    def cntUpdateRespuesta(id):
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = upRespuesta(id, data)

        if result is None:
            return jsonify({"error": "respuesta no encontrado"}), 404

        return jsonify(result), 200


    @staticmethod
    def cntDeleteRespuesta(id):
        if not delRespuesta(id):
            return jsonify({"error": "respuesta no encontrado"}), 404

        return jsonify({"message": "respuesta eliminado correctamente"}), 200
