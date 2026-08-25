from flask import request, jsonify
from Services.consulta_services import (
    servListConsulta,
    servGetConsulta,
    addConsulta,
    upConsulta,
    delConsulta
)

class consulta:
    def cntListConsulta():
        return jsonify(servListConsulta()), 200


    def cntGetConsulta(id):
        data = servGetConsulta(id)

        if data is None:
            return jsonify({"error": "consulta no encontrado"}), 404

        return jsonify(data), 200


    def cntCreateConsulta():
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = addConsulta(data)
        return jsonify(result), 201


    def cntUpdateConsulta(id):
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = upConsulta(id, data)

        if result is None:
            return jsonify({"error": "consulta no encontrado"}), 404

        return jsonify(result), 200


    def cntDeleteConsulta(id):
        if not delConsulta(id):
            return jsonify({"error": "consulta no encontrado"}), 404

        return jsonify({"message": "consulta eliminado correctamente"}), 200
