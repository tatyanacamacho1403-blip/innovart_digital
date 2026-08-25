from flask import request, jsonify
from Services.pago_services import (
    servListPago,
    servGetPago,
    addPago,
    upPago,
    delPago
)

class pago:
    def cntListPago():
        return jsonify(servListPago()), 200


    def cntGetPago(id):
        data = servGetPago(id)

        if data is None:
            return jsonify({"error": "pago no encontrado"}), 404

        return jsonify(data), 200


    def cntCreatePago():
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = addPago(data)
        return jsonify(result), 201


    def cntUpdatePago(id):
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Debe enviar un JSON"}), 400

        result = upPago(id, data)

        if result is None:
            return jsonify({"error": "pago no encontrado"}), 404

        return jsonify(result), 200


    def cntDeletePago(id):
        if not delPago(id):
            return jsonify({"error": "pago no encontrado"}), 404

        return jsonify({"message": "pago eliminado correctamente"}), 200

