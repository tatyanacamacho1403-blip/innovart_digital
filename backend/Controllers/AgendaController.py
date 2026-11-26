from flask import current_app, g, jsonify, request
import uuid


class AgendaController:
    def list(self):
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT AGE_ID, AGE_UUID, AGE_FECHA, AGE_HORA, AGE_USU_ID, AGE_SER_ID, AGE_PAG_ID,
                      AGE_DIRECCION, AGE_DESCRIPCION
               FROM T_AGENDA WHERE AGE_USU_ID = %s ORDER BY AGE_FECHA, AGE_HORA""",
            (g.user_id,),
        )
        agendas = cursor.fetchall()
        cursor.close()
        return jsonify([{
            "id": row[0], "uuid": str(row[1]), "fecha": str(row[2]),
            "hora": str(row[3]), "usuario_id": row[4],
            "servicio_id": row[5], "pago_id": row[6],
            "direccion": row[7], "descripcion": row[8],
        } for row in agendas]), 200

    def get(self, id):
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT AGE_ID, AGE_UUID, AGE_FECHA, AGE_HORA, AGE_USU_ID, AGE_SER_ID,
                      AGE_PAG_ID, AGE_DIRECCION, AGE_DESCRIPCION
               FROM T_AGENDA WHERE AGE_ID = %s AND AGE_USU_ID = %s""",
            (id, g.user_id),
        )
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return jsonify({"mensaje": "Agenda no encontrada"}), 404
        return jsonify({
            "id": row[0], "uuid": str(row[1]), "fecha": str(row[2]),
            "hora": str(row[3]), "usuario_id": row[4], "servicio_id": row[5],
            "pago_id": row[6], "direccion": row[7], "descripcion": row[8],
        }), 200

    def create(self):
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"mensaje": "Envía un objeto JSON válido"}), 400
        fecha, hora, servicio_id = data.get("fecha"), data.get("hora"), data.get("servicio_id")
        direccion = data.get("direccion")
        descripcion = data.get("descripcion")
        if not fecha or not hora or not servicio_id or not direccion or not descripcion:
            return jsonify({"mensaje": "Fecha, hora, servicio, dirección y descripción son obligatorios"}), 400
        if not isinstance(direccion, str) or not isinstance(descripcion, str):
            return jsonify({"mensaje": "Dirección y descripción deben ser texto"}), 400
        direccion, descripcion = direccion.strip(), descripcion.strip()
        if not direccion or len(direccion) > 255 or not descripcion:
            return jsonify({"mensaje": "La dirección debe tener entre 1 y 255 caracteres y la descripción no puede estar vacía"}), 400
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        agenda_uuid = str(uuid.uuid4())
        try:
            cursor.execute(
                "INSERT INTO T_AGENDA (AGE_UUID, AGE_FECHA, AGE_HORA, AGE_USU_ID, AGE_SER_ID, AGE_DIRECCION, AGE_DESCRIPCION) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (agenda_uuid, fecha, hora, g.user_id, servicio_id, direccion, descripcion),
            )
            mysql.connection.commit()
            new_id = cursor.lastrowid
        except Exception:
            mysql.connection.rollback()
            raise
        finally:
            cursor.close()
        return jsonify({"mensaje": "Agenda creada correctamente", "id": new_id, "uuid": agenda_uuid}), 201

    def update(self, id):
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"mensaje": "Envía un objeto JSON válido"}), 400
        fecha, hora, servicio_id = data.get("fecha"), data.get("hora"), data.get("servicio_id")
        if not fecha or not hora or not servicio_id:
            return jsonify({"mensaje": "Fecha, hora y servicio son obligatorios"}), 400
        direccion = data.get("direccion")
        descripcion = data.get("descripcion")
        if direccion is not None and (not isinstance(direccion, str) or not direccion.strip() or len(direccion.strip()) > 255):
            return jsonify({"mensaje": "La dirección debe tener entre 1 y 255 caracteres"}), 400
        if descripcion is not None and (not isinstance(descripcion, str) or not descripcion.strip()):
            return jsonify({"mensaje": "La descripción no puede estar vacía"}), 400
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE T_AGENDA SET AGE_FECHA = %s, AGE_HORA = %s, AGE_SER_ID = %s, AGE_DIRECCION = COALESCE(%s, AGE_DIRECCION), AGE_DESCRIPCION = COALESCE(%s, AGE_DESCRIPCION) WHERE AGE_ID = %s AND AGE_USU_ID = %s",
            (fecha, hora, servicio_id, direccion.strip() if direccion is not None else None, descripcion.strip() if descripcion is not None else None, id, g.user_id),
        )
        changed = cursor.rowcount
        if changed == 0:
            cursor.execute("SELECT AGE_ID FROM T_AGENDA WHERE AGE_ID = %s AND AGE_USU_ID = %s", (id, g.user_id))
            exists = cursor.fetchone() is not None
        else:
            exists = True
        mysql.connection.commit()
        cursor.close()
        if not exists:
            return jsonify({"mensaje": "Agenda no encontrada"}), 404
        return jsonify({"mensaje": "Agenda actualizada correctamente"}), 200

    def delete(self, id):
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM T_AGENDA WHERE AGE_ID = %s AND AGE_USU_ID = %s", (id, g.user_id))
        mysql.connection.commit()
        changed = cursor.rowcount
        cursor.close()
        if changed == 0:
            return jsonify({"mensaje": "Agenda no encontrada"}), 404
        return jsonify({"mensaje": "Agenda eliminada correctamente"}), 200
