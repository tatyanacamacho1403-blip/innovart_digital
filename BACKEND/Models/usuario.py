class Usuario:
    def __init__(self, id, uuid, contrasena, per_id):
        self.usu_id = id
        self.usu_uuid = uuid
        self.usu_contrasena = contrasena
        self.usu_per_id = per_id

    def to_dict(self):
        return {
            "id": self.usu_id,
            "uuid": self.usu_uuid,
            "contrasena": self.usu_contrasena,
            "per_id": self.usu_per_id
        }
