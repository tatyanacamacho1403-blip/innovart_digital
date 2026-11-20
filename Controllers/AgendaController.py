from flask import g, jsonify, request
from App import mysql
import uuid


class AgendaController:
    def list(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT AGE_ID, AGE_UUID, AGE_FECHA, AGE_HORA, AGE_USU_ID, AGE_SER_ID, AGE_PAG_ID
               FROM T_AGENDA WHERE AGE_USU_ID = %s ORDER BY AGE_FECHA, AGE_HORA""",
            (g.user_id,),
        )
        agendas = cursor.fetchall()
        cursor.close()
        return jsonify([{
            "id": row[0], "uuid": str(row[1]), "fecha": str(row[2]),
            "hora": str(row[3]), "usuario_id": row[4],
            "servicio_id": row[5], "pago_id": row[6],
        } for row in agendas]), 200

    def get(self, id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT AGE_ID, AGE_UUID, AGE_FECHA, AGE_HORA, AGE_USU_ID, AGE_SER_ID
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
        }), 200

    def create(self):
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"mensaje": "Envía un objeto JSON válido"}), 400
        fecha, hora, servicio_id = data.get("fecha"), data.get("hora"), data.get("servicio_id")
        if not fecha or not hora or not servicio_id:
            return jsonify({"mensaje": "Fecha, hora y servicio son obligatorios"}), 400
        cursor = mysql.connection.cursor()
        agenda_uuid = str(uuid.uuid4())
        try:
            cursor.execute(
                "INSERT INTO T_AGENDA (AGE_UUID, AGE_FECHA, AGE_HORA, AGE_USU_ID, AGE_SER_ID) VALUES (%s, %s, %s, %s, %s)",
                (agenda_uuid, fecha, hora, g.user_id, servicio_id),
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
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE T_AGENDA SET AGE_FECHA = %s, AGE_HORA = %s, AGE_SER_ID = %s WHERE AGE_ID = %s AND AGE_USU_ID = %s",
            (fecha, hora, servicio_id, id, g.user_id),
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
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM T_AGENDA WHERE AGE_ID = %s AND AGE_USU_ID = %s", (id, g.user_id))
        mysql.connection.commit()
        changed = cursor.rowcount
        cursor.close()
        if changed == 0:
            return jsonify({"mensaje": "Agenda no encontrada"}), 404
        return jsonify({"mensaje": "Agenda eliminada correctamente"}), 200
