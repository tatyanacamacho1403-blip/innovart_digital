from flask import request, jsonify
from Services.empleado_services import (
    servListEmpleado,
    servGetEmpleado,
    addEmpleado,
    upEmpleado,
    delEmpleado
)


class EmpleadoController:

    @staticmethod
    def cntListEmpleado():
        return jsonify(servListEmpleado()), 200


    @staticmethod
    def cntGetEmpleado(id):
        data = servGetEmpleado(id)

        if data is None:
            return jsonify({"error": "empleado no encontrado"}), 404

        return jsonify(data), 200


    @staticmethod
    def cntCreateEmpleado():
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = addEmpleado(data)
        return jsonify(result), 201


    @staticmethod
    def cntUpdateEmpleado(id):
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = upEmpleado(id, data)

        if result is None:
            return jsonify({"error": "empleado no encontrado"}), 404

        return jsonify(result), 200


    @staticmethod
    def cntDeleteEmpleado(id):
        if not delEmpleado(id):
            return jsonify({"error": "empleado no encontrado"}), 404

        return jsonify({"message": "empleado eliminado correctamente"}), 200
