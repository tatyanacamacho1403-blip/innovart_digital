class rol:

    def __init__(self, uuid, tipo):
        self.roluuid = uuid
        self.roltipo = tipo

    def to_dict(self): 
        return {
            'uuid': self.rol_uuid,
            'contraseña': self.rol_contraseña,
            'tipo': self.rol_tipo
        }