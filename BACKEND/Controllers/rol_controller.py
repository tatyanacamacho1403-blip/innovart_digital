from flask import request, jsonify
from Services.rol_services import (
    servListRol,
    servGetRol,
    addRol,
    upRol,
    delRol
)


class RolController:

    @staticmethod
    def cntListRol():
        return jsonify(servListRol()), 200


    @staticmethod
    def cntGetRol(id):
        data = servGetRol(id)

        if data is None:
            return jsonify({"error": "rol no encontrado"}), 404

        return jsonify(data), 200


    @staticmethod
    def cntCreateRol():
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = addRol(data)
        return jsonify(result), 201


    @staticmethod
    def cntUpdateRol(id):
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = upRol(id, data)

        if result is None:
            return jsonify({"error": "rol no encontrado"}), 404

        return jsonify(result), 200


    @staticmethod
    def cntDeleteRol(id):
        if not delRol(id):
            return jsonify({"error": "rol no encontrado"}), 404

        return jsonify({"message": "rol eliminado correctamente"}), 200
