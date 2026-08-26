from flask import request, jsonify
from Services.usuario_services import (
    servListUsuario,
    servGetUsuario,
    addUsuario,
    upUsuario,
    delUsuario
)


class UsuarioController:

    @staticmethod
    def cntListUsuario():
        return jsonify(servListUsuario()), 200


    @staticmethod
    def cntGetUsuario(id):
        data = servGetUsuario(id)

        if data is None:
            return jsonify({"error": "usuario no encontrado"}), 404

        return jsonify(data), 200


    @staticmethod
    def cntCreateUsuario():
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = addUsuario(data)
        return jsonify(result), 201


    @staticmethod
    def cntUpdateUsuario(id):
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = upUsuario(id, data)

        if result is None:
            return jsonify({"error": "usuario no encontrado"}), 404

        return jsonify(result), 200


    @staticmethod
    def cntDeleteUsuario(id):
        if not delUsuario(id):
            return jsonify({"error": "usuario no encontrado"}), 404

        return jsonify({"message": "usuario eliminado correctamente"}), 200
