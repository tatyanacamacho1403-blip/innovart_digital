import re
import uuid

from flask import current_app, g, jsonify, request
from MySQLdb import IntegrityError
from werkzeug.security import generate_password_hash

from Models.Usuario import Usuario
from Security import create_access_token, is_admin
from Services.UsuarioService import UsuarioService


class UsuarioController:
    service = UsuarioService()
    person_fields = (
        "cedula", "documento", "primer_nombre", "primer_apellido",
        "direccion", "fecha_nacimiento",
    )

    def list(self):
        if is_admin():
            return jsonify(self.service.list()), 200
        user = self.service.getById(g.user_id)
        return jsonify([user] if user else []), 200

    def get(self, id):
        if id != g.user_id and not is_admin():
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
        data = self.service.getById(id)
        if data is None:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
        return jsonify(data), 200

    def create(self):
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"mensaje": "Envía un objeto JSON válido"}), 400

        correo = str(data.get("correo", "")).strip().lower()
        contrasena = data.get("contrasena")
        missing = [
            field for field in self.person_fields
            if data.get(field) is None or not str(data.get(field)).strip()
        ]
        if not correo or not contrasena or missing:
            return jsonify({"mensaje": "Completa correo, contraseña y todos los datos personales", "campos": missing}), 400
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            return jsonify({"mensaje": "Correo no válido"}), 400
        if not isinstance(contrasena, str) or len(contrasena) < 8:
            return jsonify({"mensaje": "La contraseña debe tener mínimo 8 caracteres"}), 400

        optional_fields = ("segundo_nombre", "segundo_apellido", "telefono")
        for field in optional_fields:
            value = data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                data[field] = None

        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        person_uuid = uuid.uuid4().hex
        user_uuid = str(uuid.uuid4())
        try:
            cursor.execute("SELECT USU_ID FROM T_USUARIO WHERE LOWER(USU_CORREO) = %s", (correo,))
            if cursor.fetchone():
                return jsonify({"mensaje": "El correo ya está registrado"}), 409

            cursor.execute(
                """INSERT INTO T_PERSONA
                (PER_UUID, PER_CEDULA, PER_DOCUMENTO, PER_PRIMER_NOMBRE,
                 PER_SEGUNDO_NOMBRE, PER_PRIMER_APELLIDO, PER_SEGUNDO_APELLIDO,
                 PER_CORREO, PER_DIRECCION, PER_TELEFONO, PER_FECHA_NACIMIENTO)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (person_uuid, data["cedula"], data["documento"], data["primer_nombre"],
                 data["segundo_nombre"], data["primer_apellido"], data["segundo_apellido"],
                 correo, data["direccion"], data["telefono"], data["fecha_nacimiento"]),
            )
            person_id = cursor.lastrowid
            cursor.execute(
                """INSERT INTO T_USUARIO (USU_UUID, USU_CORREO, USU_CONTRASEÑA, USU_PER_ID)
                VALUES (%s, %s, %s, %s)""",
                (user_uuid, correo, generate_password_hash(contrasena), person_id),
            )
            user_id = cursor.lastrowid
            mysql.connection.commit()
        except IntegrityError:
            mysql.connection.rollback()
            return jsonify({"mensaje": "El correo o documento ya existe"}), 409
        except Exception:
            mysql.connection.rollback()
            raise
        finally:
            cursor.close()

        usuario = Usuario(user_id, user_uuid, correo, None, person_id)
        token = create_access_token(user_id, person_id)
        return jsonify({
            "mensaje": "Usuario registrado correctamente",
            "usuario": usuario.to_dict(),
            "token": token,
        }), 201

    def login(self):
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"mensaje": "Envía un objeto JSON válido"}), 400
        correo = str(data.get("correo", "")).strip().lower()
        contrasena = data.get("contrasena")
        if not correo or not isinstance(contrasena, str) or not contrasena:
            return jsonify({"mensaje": "Correo y contraseña son obligatorios"}), 400
        usuario = UsuarioService.validar_login(current_app.mysql, correo, contrasena)
        if usuario is None:
            return jsonify({"mensaje": "Correo o contraseña incorrectos"}), 401
        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "usuario": usuario.to_dict(),
            "token": create_access_token(usuario.usu_id, usuario.usu_per_id),
        }), 200

    def update(self, id):
        if id != g.user_id and not is_admin():
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not data:
            return jsonify({"mensaje": "Envía un objeto JSON válido"}), 400
        if "per_id" in data:
            return jsonify({"mensaje": "El perfil asociado no se puede cambiar"}), 400
        if "correo" in data and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", str(data["correo"]).strip()):
            return jsonify({"mensaje": "Correo no válido"}), 400
        if "contrasena" in data and (not isinstance(data["contrasena"], str) or len(data["contrasena"]) < 8):
            return jsonify({"mensaje": "La contraseña debe tener mínimo 8 caracteres"}), 400
        usuario = self.service.update(id, data)
        if usuario is None:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
        return jsonify(usuario), 200

    def delete(self, id):
        if id != g.user_id and not is_admin():
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
        if not self.service.delete(id):
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
        return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200
