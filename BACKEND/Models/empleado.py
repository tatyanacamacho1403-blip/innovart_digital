class Empleado:
    def __init__(self, id, uuid):
        self.emp_id = id
        self.emp_uuid = uuid

    def to_dict(self):
        return {
            "id": self.emp_id,
            "uuid": self.emp_uuid
        }
