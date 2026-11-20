from flask import request, jsonify, g
from MySQLdb import IntegrityError
from Services.PersonaService import PersonaService
from Security import is_admin


class PersonaController:

    service = PersonaService()

    def list(self):
        if is_admin():
            return jsonify(self.service.list()), 200
        person = self.service.getById(g.person_id)
        return jsonify([person] if person else []), 200


    def get(self, id):
        if id != g.person_id and not is_admin():
            return jsonify({"error": "persona no encontrada"}), 404
        data = self.service.getById(id)

        if data is None:
            return jsonify({"error": "persona no encontrado"}), 404

        return jsonify(data), 200


    def create(self):
        data = request.get_json(silent=True)

        if not isinstance(data, dict) or not data:
            return jsonify({
                "mensaje": "El cuerpo de la petición no debe estar vacío o mal formateado"
            }), 400

        camposR = ["cedula", "documento", "primer_nombre", "primer_apellido", "direccion", "fecha_nacimiento"]

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

        data = self._normalize_optional_fields(data)
        result = self.service.create(data)
        return jsonify(result), 201


    def update(self, id):
        if id != g.person_id and not is_admin():
            return jsonify({"error": "persona no encontrada"}), 404
        data = request.get_json(silent=True)

        if not isinstance(data, dict) or not data:
            return jsonify({"mensaje": "Envía un objeto JSON válido"}), 400

        required = ["cedula", "documento", "primer_nombre", "primer_apellido", "direccion", "fecha_nacimiento"]
        missing = [field for field in required if field not in data or data.get(field) is None or str(data.get(field)).strip() == ""]
        if missing:
            return jsonify({"mensaje": "Envía todos los campos requeridos", "campos": missing}), 400

        data = self._normalize_optional_fields(data)
        result = self.service.update(id, data)

        if result is None:
            return jsonify({"error": "persona no encontrado"}), 404

        return jsonify(result), 200

    @staticmethod
    def _normalize_optional_fields(data):
        normalized = data.copy()
        for field in ("segundo_nombre", "segundo_apellido", "correo", "telefono"):
            value = normalized.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                normalized[field] = None
        return normalized


    def delete(self, id):
        if id != g.person_id and not is_admin():
            return jsonify({"error": "persona no encontrada"}), 404
        try:
            deleted = self.service.delete(id)
        except IntegrityError:
            return jsonify({"mensaje": "No se puede eliminar la persona porque tiene registros relacionados"}), 409
        if not deleted:
            return jsonify({"error": "persona no encontrado"}), 404

        return jsonify({"message": "persona eliminado correctamente"}), 200
