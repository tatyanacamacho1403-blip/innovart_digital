from flask import request, jsonify
from Services.usuario_services import usuarios_services

class user_contoller:

    def cntlistUsuario():
        data = usuarios_services.servListUsuario
        return jsonify(data), 200


    def getUsuario(id):
       data = servGetUsuario(id)

       if data is None:
        return jsonify({"error": "usuario no encontrado"}), 404

       return jsonify(data), 200


    def createUsuario():

        nombre = request.json["nombre"]
        apellido = request.json["apellido"]
        tipo_doc= request.json["tipo_doc"]
        documento=request.json["documento"]
        fecha_nac= request.json["fecha_nac"]

        data = usuarios_services.addUsuario(nombre, apellido, tipo_doc, documento, fecha_nac)
        return jsonify({"message": data }), 201
        


    def updateUsuario(id):
        data = request.get_json(silent=True)

        if data is None:
         return jsonify({"error": "Debe enviar un JSON"}), 400

        data = upUsuario(id, data)

        if data is None:
          return jsonify({"error": "usuario no encontrado"}), 404

        return jsonify(data), 200


    def deleteUsuario(id):
       if not delUsuario(id):
        return jsonify({"error": "usuario no encontrado"}), 404

       return jsonify({"message": "usuario eliminado correctamente"}), 200


    def searchUuidUsuario(uuid):
       data = searchByUuidUsuario(uuid)

       if data is None:
        return jsonify({"error": "usuario no encontrado"}), 404

       return jsonify(data), 200



