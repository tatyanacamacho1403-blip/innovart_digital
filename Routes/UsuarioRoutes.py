from flask import Blueprint
from Controllers.UsuarioController import UsuarioController


UsuarioRoutes = Blueprint("UsuarioRoutes", __name__)

controller = UsuarioController()


@UsuarioRoutes.route("/", methods=["GET"])
def list():
    return controller.list()


@UsuarioRoutes.route("/<int:id>", methods=["GET"])
def get(id):
    return controller.get(id)


@UsuarioRoutes.route(
    "/registro",
    methods=["POST"]
)
def registrar_usuario():

    from App import app

    return UsuarioController.registrar(
        app.mysql
    )


@UsuarioRoutes.route(
    "/login",
    methods=["POST"]
)
def login_usuario():

    from App import app

    return UsuarioController.login(
        app.mysql
    )


@UsuarioRoutes.route("/<int:id>", methods=["PUT"])
def update(id):
    return controller.update(id)


@UsuarioRoutes.route("/<int:id>", methods=["DELETE"])
def delete(id):
    return controller.delete(id)
