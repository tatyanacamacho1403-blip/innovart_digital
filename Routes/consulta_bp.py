from flask import Blueprint
from Controllers.consulta_controller import (
    listConsulta,
    getConsulta,
    createConsulta,
    updateConsulta,
    deleteConsulta,
    searchUuidConsulta
)

consulta_bp = Blueprint("consulta", __name__, url_prefix="/consultas")


consulta_bp.route("/", methods=["GET"])(listConsulta)
consulta_bp.route("/<int:id>", methods=["GET"])(getConsulta)
consulta_bp.route("/", methods=["POST"])(createConsulta)
consulta_bp.route("/<int:id>", methods=["PUT"])(updateConsulta)
consulta_bp.route("/<int:id>", methods=["DELETE"])(deleteConsulta)
consulta_bp.route("/uuid/<uuid>", methods=["GET"])(searchUuidConsulta)
