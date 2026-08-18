from flask import Blueprint
from Controllers.empleado_controller import (
    listEmpleado,
    getEmpleado,
    createEmpleado,
    updateEmpleado,
    deleteEmpleado,
    searchUuidEmpleado
)

empleado_bp = Blueprint("empleado", __name__, url_prefix="/empleados")


empleado_bp.route("/", methods=["GET"])(listEmpleado)
empleado_bp.route("/<int:id>", methods=["GET"])(getEmpleado)
empleado_bp.route("/", methods=["POST"])(createEmpleado)
empleado_bp.route("/<int:id>", methods=["PUT"])(updateEmpleado)
empleado_bp.route("/<int:id>", methods=["DELETE"])(deleteEmpleado)
empleado_bp.route("/uuid/<uuid>", methods=["GET"])(searchUuidEmpleado)
