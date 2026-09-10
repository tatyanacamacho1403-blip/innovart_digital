class Usuario:

    def __init__(self, id, uuid, contraseña, per_id):
        self.usu_id = id
        self.usu_uuid = uuid
        self.usu_contraseña = contraseña
        self.usu_per_id = per_id

    #covertir el objeto en diccionario
    def to_dict(self):
        return {
            'id': self.usu_id,
            'uuid': self.usu_uuid,
            'contraseña': self.usu_contraseña,
            'per_id': self.usu_per_id
        }