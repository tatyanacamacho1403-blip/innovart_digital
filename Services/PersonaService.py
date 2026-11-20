from flask import current_app
from Models.Persona import Persona
import uuid
from MySQLdb import IntegrityError

class PersonaService:
    def list(self):

        sql = """SELECT PER_ID, PER_UUID, PER_CEDULA, PER_DOCUMENTO, PER_PRIMER_NOMBRE, PER_SEGUNDO_NOMBRE, 
        PER_PRIMER_APELLIDO, PER_SEGUNDO_APELLIDO, PER_CORREO, PER_DIRECCION, PER_TELEFONO, PER_FECHA_NACIMIENTO FROM 
        T_PERSONA"""

        c = current_app.mysql.connection.cursor()
        try:
            c.execute(sql)
            data = c.fetchall()
        finally:
            c.close()

        lista_l = []

        for u in data:

            objeto = Persona(
                    u[0],
                    u[1],
                    u[2],
                    u[3],
                    u[4],
                    u[5],
                    u[6],
                    u[7],
                    u[8],
                    u[9],
                    u[10],
                    u[11]
            )

            lista_l.append(objeto.to_dict())

        return lista_l


    def getById(self, id):

        sql = """SELECT PER_ID, PER_UUID, PER_CEDULA, PER_DOCUMENTO, PER_PRIMER_NOMBRE, 
        PER_SEGUNDO_NOMBRE, PER_PRIMER_APELLIDO, PER_SEGUNDO_APELLIDO,
          PER_CORREO, PER_DIRECCION, PER_TELEFONO, PER_FECHA_NACIMIENTO FROM T_PERSONA WHERE PER_ID = %s"""

        c = current_app.mysql.connection.cursor()
        try:
            c.execute(sql, (id,))
            data = c.fetchone()
        finally:
            c.close()

        if data is None:
            return None

        objeto = Persona(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11]
        )

        return objeto.to_dict()


    def create(self, data):
        UUID_P = uuid.uuid4().hex  # Generar un UUID único para la persona
        sql = """INSERT INTO T_PERSONA (PER_UUID, PER_CEDULA, PER_DOCUMENTO, PER_PRIMER_NOMBRE, PER_SEGUNDO_NOMBRE,
          PER_PRIMER_APELLIDO, PER_SEGUNDO_APELLIDO, PER_CORREO, PER_DIRECCION, PER_TELEFONO, PER_FECHA_NACIMIENTO) 
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (UUID_P, data.get('cedula'), 
                  data.get('documento'), data.get('primer_nombre'), data.get('segundo_nombre'), data.get('primer_apellido'), 
                  data.get('segundo_apellido'), data.get('correo'), data.get('direccion'), data.get('telefono'), data.get('fecha_nacimiento'),)

        connection = current_app.mysql.connection
        c = connection.cursor()
        try:
            c.execute(sql, values)
            new_id = c.lastrowid
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            c.close()

        return self.getById(new_id)


    def update(self, id, data):

        sql = """UPDATE T_PERSONA SET PER_CEDULA = %s, PER_DOCUMENTO = %s, PER_PRIMER_NOMBRE = %s, PER_SEGUNDO_NOMBRE = %s,
          PER_PRIMER_APELLIDO = %s, PER_SEGUNDO_APELLIDO = %s, PER_CORREO = %s, PER_DIRECCION = %s, PER_TELEFONO = %s, PER_FECHA_NACIMIENTO = %s 
          WHERE PER_ID = %s"""

        values = (data.get('cedula'), data.get('documento'), data.get('primer_nombre'), data.get('segundo_nombre'),
                   data.get('primer_apellido'), data.get('segundo_apellido'), data.get('correo'), data.get('direccion'), data.get('telefono'), 
                   data.get('fecha_nacimiento'), id)

        connection = current_app.mysql.connection
        c = connection.cursor()
        try:
            c.execute(sql, values)
            c.execute("SELECT 1 FROM T_PERSONA WHERE PER_ID = %s", (id,))
            exists = c.fetchone() is not None
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            c.close()

        if not exists:
            return None

        return self.getById(id)


    def delete(self, id):

        sql = "DELETE FROM T_PERSONA WHERE PER_ID = %s"

        connection = current_app.mysql.connection
        c = connection.cursor()
        try:
            c.execute(sql, (id,))
            affected = c.rowcount
            connection.commit()
        except IntegrityError:
            connection.rollback()
            raise
        except Exception:
            connection.rollback()
            raise
        finally:
            c.close()

        return affected > 0
