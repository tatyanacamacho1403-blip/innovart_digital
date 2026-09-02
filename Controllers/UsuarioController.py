from flask import jsonify, request
from Services.UsuarioService import UsuarioService


class UsuarioController:

    def list(self):
        data = UsuarioService().list()
        return jsonify(data), 200

    def get(self, id):
        data = UsuarioService().getById(id)

        if data is None:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404

        return jsonify(data), 200

    def create(self):
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "mensaje": "El cuerpo de la petición no debe estar vacío o mal formateado"
            }), 400

        camposR = ["uuid", "correo", "contrasena", "per_id"]

        camposF = [x for x in camposR if x not in data]

        if len(camposF) > 0:
            return jsonify({
                "campos": f"Campos faltantes {camposF}"
            }), 400

        camposV = [
            x for x in camposR
            if data.get(x) is None or str(data.get(x)).strip() == ""
        ]

        if len(camposV) > 0:
            return jsonify({
                "campos": f"Campos vacíos {camposV}"
            }), 400

        usuario = UsuarioService().create(data)

        return jsonify(usuario), 201

    def update(self, id):
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "mensaje": "El cuerpo de la petición no debe estar vacío o mal formateado"
            }), 400

        usuario = UsuarioService().update(id, data)

        if usuario is None:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404

        return jsonify(usuario), 200

    def delete(self, id):
        eliminado = UsuarioService().delete(id)

        if not eliminado:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404

        return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200