class Persona:

    def __init__(self, id, uuid, cedula, documento, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, fecha_nacimiento,  direccion, telefono, correo_electronico):
        self.per_id = id
        self.per_uuid = uuid
        self.per_cedula = cedula
        self.per_documento = documento
        self.per_primer_nombre = primer_nombre
        self.per_segundo_nombre = segundo_nombre
        self.per_primer_apellido = primer_apellido
        self.per_segundo_apellido = segundo_apellido
        self.per_fecha_nacimiento = fecha_nacimiento
        self.per_direccion = direccion
        self.per_telefono = telefono
        self.per_correo_electronico = correo_electronico

    #covertir el objeto en diccionario
    def to_dict(self):
        return {
            'id': self.per_id,
            'uuid': self.per_uuid,
            'cedula': self.per_cedula,
            'documento': self.per_documento,
            'primer_nombre': self.per_primer_nombre,
            'segundo_nombre': self.per_segundo_nombre,
            'primer_apellido': self.per_primer_apellido,
            'segundo_apellido': self.per_segundo_apellido,
            'fecha_nacimiento': self.per_fecha_nacimiento,
            'direccion': self.per_direccion,
            'telefono': self.per_telefono,
            'correo_electronico': self.per_correo_electronico
        }