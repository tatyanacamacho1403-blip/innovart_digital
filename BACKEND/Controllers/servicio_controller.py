from flask import request, jsonify
from Services.servicio_services import (
    servListServicio,
    servGetServicio,
    addServicio,
    upServicio,
    delServicio
)


class ServicioController:

    @staticmethod
    def cntListServicio():
        return jsonify(servListServicio()), 200


    @staticmethod
    def cntGetServicio(id):
        data = servGetServicio(id)

        if data is None:
            return jsonify({"error": "servicio no encontrado"}), 404

        return jsonify(data), 200


    @staticmethod
    def cntCreateServicio():
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = addServicio(data)
        return jsonify(result), 201


    @staticmethod
    def cntUpdateServicio(id):
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = upServicio(id, data)

        if result is None:
            return jsonify({"error": "servicio no encontrado"}), 404

        return jsonify(result), 200


    @staticmethod
    def cntDeleteServicio(id):
        if not delServicio(id):
            return jsonify({"error": "servicio no encontrado"}), 404

        return jsonify({"message": "servicio eliminado correctamente"}), 200
