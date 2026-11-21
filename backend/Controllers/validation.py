from flask import jsonify


def validate_complete_payload(data, fields):
    if not isinstance(data, dict) or not data:
        return jsonify({"mensaje": "Envía un objeto JSON válido"}), 400
    missing = [field for field in fields if field not in data or data.get(field) is None or str(data.get(field)).strip() == ""]
    if missing:
        return jsonify({"mensaje": "Envía todos los campos requeridos", "campos": missing}), 400
    return None
