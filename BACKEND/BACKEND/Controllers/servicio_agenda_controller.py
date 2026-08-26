from flask import request, jsonify
from Services.servicio_agenda_services import (
    servListServicioAgenda,
    servGetServicioAgenda,
    addServicioAgenda,
    upServicioAgenda,
    delServicioAgenda
)


class ServicioAgendaController:

    @staticmethod
    def cntListServicioAgenda():
        return jsonify(servListServicioAgenda()), 200


    @staticmethod
    def cntGetServicioAgenda(id):
        data = servGetServicioAgenda(id)

        if data is None:
            return jsonify({"error": "servicioAgenda no encontrado"}), 404

        return jsonify(data), 200


    @staticmethod
    def cntCreateServicioAgenda():
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = addServicioAgenda(data)
        return jsonify(result), 201


    @staticmethod
    def cntUpdateServicioAgenda(id):
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = upServicioAgenda(id, data)

        if result is None:
            return jsonify({"error": "servicioAgenda no encontrado"}), 404

        return jsonify(result), 200


    @staticmethod
    def cntDeleteServicioAgenda(id):
        if not delServicioAgenda(id):
            return jsonify({"error": "servicioAgenda no encontrado"}), 404

        return jsonify({"message": "servicioAgenda eliminado correctamente"}), 200
