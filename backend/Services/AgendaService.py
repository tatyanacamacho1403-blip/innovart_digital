from flask import current_app
from Models.Agenda import Agenda


class AgendaService:
    def list(self):

        sql = "SELECT AGE_ID, AGE_UUID, AGE_FECHA, AGE_HORA, AGE_SER_ID, AGE_USU_ID, AGE_PAG_ID, AGE_DIRECCION, AGE_DESCRIPCION FROM T_AGENDA"

        c = current_app.mysql.connection.cursor()
        c.execute(sql)

        data = c.fetchall()

        lista_l = []

        for u in data:

            objeto = Agenda(
                    u[0],
                    u[1],
                    u[2],
                    u[3],
                    u[4],
                    u[5],
                    u[6], u[7], u[8]
            )

            lista_l.append(objeto.to_dict())

        c.close()

        return lista_l


    def getById(self, id):

        sql = "SELECT AGE_ID, AGE_UUID, AGE_FECHA, AGE_HORA, AGE_SER_ID, AGE_USU_ID, AGE_PAG_ID, AGE_DIRECCION, AGE_DESCRIPCION FROM T_AGENDA WHERE AGE_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))

        data = c.fetchone()

        c.close()

        if data is None:
            return None

        objeto = Agenda(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6], data[7], data[8]
        )

        return objeto.to_dict()


    def create(self, data):

        sql = "INSERT INTO T_AGENDA (AGE_UUID, AGE_FECHA, AGE_HORA, AGE_SER_ID, AGE_USU_ID, AGE_PAG_ID, AGE_DIRECCION, AGE_DESCRIPCION) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        values = (data.get('uuid'), data.get('fecha'), data.get('hora'), data.get('ser_id'), data.get('usu_id'), data.get('pag_id'), data.get('direccion'), data.get('descripcion'),)

        c = current_app.mysql.connection.cursor()
        c.execute(sql, values)
        current_app.mysql.connection.commit()

        new_id = c.lastrowid

        c.close()

        return self.getById(new_id)


    def update(self, id, data):

        sql = "UPDATE T_AGENDA SET AGE_UUID = %s, AGE_FECHA = %s, AGE_HORA = %s, AGE_SER_ID = %s, AGE_USU_ID = %s, AGE_PAG_ID = %s, AGE_DIRECCION = COALESCE(%s, AGE_DIRECCION), AGE_DESCRIPCION = COALESCE(%s, AGE_DESCRIPCION) WHERE AGE_ID = %s"

        values = (data.get('uuid'), data.get('fecha'), data.get('hora'), data.get('ser_id'), data.get('usu_id'), data.get('pag_id'), data.get('direccion'), data.get('descripcion'), id)

        c = current_app.mysql.connection.cursor()
        c.execute(sql, values)
        exists = c.rowcount > 0
        if not exists:
            c.execute("SELECT 1 FROM T_AGENDA WHERE AGE_ID = %s", (id,))
            exists = c.fetchone() is not None
        current_app.mysql.connection.commit()
        c.close()

        if not exists:
            return None

        return self.getById(id)


    def delete(self, id):

        sql = "DELETE FROM T_AGENDA WHERE AGE_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()

        affected = c.rowcount

        c.close()

        return affected > 0
