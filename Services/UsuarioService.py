from flask import current_app
from Models.Usuario import Usuario
import uuid

from werkzeug.security import generate_password_hash, check_password_hash


class UsuarioService:

    def list(self):

        sql = "SELECT USU_ID, USU_UUID, USU_CORREO, USU_PER_ID FROM T_USUARIO"

        c = current_app.mysql.connection.cursor()
        c.execute(sql)

        data = c.fetchall()

        lista_l = []

        for u in data:

            objeto = Usuario(
                    u[0],
                    u[1],
                    u[2],
                    None,
                    u[3]
            )

            lista_l.append(objeto.to_dict())

        c.close()

        return lista_l


    def getById(self, id):

        sql = "SELECT USU_ID, USU_UUID, USU_CORREO, USU_PER_ID FROM T_USUARIO WHERE USU_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))

        data = c.fetchone()

        c.close()

        if data is None:
            return None

        objeto = Usuario(
                data[0],
                data[1],
                data[2],
                None,
                data[3]
        )

        return objeto.to_dict()

    @staticmethod
    def create(mysql, correo, contrasena, per_id):
         
        cursor = mysql.connection.cursor()

        # Verificar si el correo ya existe
        sql_buscar: str = """
            SELECT USU_ID
            FROM T_USUARIO
            WHERE USU_CORREO = %s
        """

        cursor.execute(sql_buscar, (correo,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            cursor.close()

            return None, "El correo ya está registrado"

        # Crear UUID
        usuario_uuid = str(uuid.uuid4())

        # Convertir contraseña en HASH
        contrasena_hash = generate_password_hash(contrasena)

        # Insertar usuario
        sql = """
            INSERT INTO T_USUARIO
            (
                USU_UUID,
                USU_CORREO,
                USU_CONTRASEÑA,
                USU_PER_ID
            )
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                usuario_uuid,
                correo,
                contrasena_hash,
                per_id
            )
        )

        mysql.connection.commit()

        nuevo_id = cursor.lastrowid

        cursor.close()

        usuario = Usuario(
            id=nuevo_id,
            uuid=usuario_uuid,
            correo=correo,
            contrasena=None,
            per_id=per_id
        )

        return usuario, None


    @staticmethod
    def buscar_por_correo(mysql, correo):

        cursor = mysql.connection.cursor()

        sql = """
            SELECT
                USU_ID,
                USU_UUID,
                USU_CORREO,
                USU_CONTRASEÑA,
                USU_PER_ID
            FROM T_USUARIO
            WHERE USU_CORREO = %s
        """

        cursor.execute(sql, (correo,))

        datos = cursor.fetchone()

        cursor.close()

        if datos is None:
            return None

        return Usuario(
            id=datos[0],
            uuid=datos[1],
            correo=datos[2],
            contrasena=datos[3],
            per_id=datos[4]
        )

    @staticmethod
    def validar_login(mysql, correo, contrasena):

        usuario = UsuarioService.buscar_por_correo(
            mysql,
            correo
        )

        if usuario is None:
            return None

        # Comparar contraseña escrita con el HASH
        contraseña_correcta = check_password_hash(
            usuario.usu_contrasena,
            contrasena
        )

        if not contraseña_correcta:
            return None

        return usuario


    def update(self, id, data):
        connection = current_app.mysql.connection
        cursor = connection.cursor()
        cursor.execute(
            "SELECT USU_UUID, USU_CONTRASEÑA, USU_PER_ID, USU_CORREO FROM T_USUARIO WHERE USU_ID = %s",
            (id,),
        )
        current = cursor.fetchone()
        if current is None:
            cursor.close()
            return None

        password = data.get("contrasena")
        password_hash = generate_password_hash(password) if password else current[1]
        correo = str(data.get("correo", current[3])).strip().lower()
        person_id = data.get("per_id", current[2])
        try:
            cursor.execute(
                "UPDATE T_USUARIO SET USU_UUID = %s, USU_CORREO = %s, USU_CONTRASEÑA = %s, USU_PER_ID = %s WHERE USU_ID = %s",
                (data.get("uuid", current[0]), correo, password_hash, person_id, id),
            )
            if correo != current[3]:
                cursor.execute("UPDATE T_PERSONA SET PER_CORREO = %s WHERE PER_ID = %s", (correo, current[2]))
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
        return self.getById(id)

    def delete(self, id):

        sql = "DELETE FROM T_USUARIO WHERE USU_ID = %s"

        c = current_app.mysql.connection.cursor()
        c.execute(sql, (id,))
        current_app.mysql.connection.commit()

        affected = c.rowcount

        c.close()

        return affected > 0
