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


def addusuario():

    #validar que los campos extisten
    campos_r = ["primer_nombre", "segundo_nombre", "primer_apellido", "segundo_apellido", ]
    
    campos_f = [for x in campos_r if x not in request.json]        
    return jsonify({"campos": campos_f})
    if len (campos_f) > 0:
        return jsonify("campos": f"campos faltantes {campos_f}"}), 400    #damos los codigos de respuesta


    # validar que no esten vacios 

    nompre = resquest.json["nombre"]
    apellido = resquest.jsdon["apellido"]


   x = user_service.adduser(nombre, apellido, tipo_documento, fecha_nacimiento)
   return jsonfity({"messege":x}), 201



