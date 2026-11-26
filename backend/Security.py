from flask import current_app, g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer


def _serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="agenda-access-v1")


def create_access_token(user_id, person_id):
    return _serializer().dumps({"user_id": int(user_id), "person_id": int(person_id)})


def read_access_token():
    header = request.headers.get("Authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    try:
        data = _serializer().loads(
            token, max_age=current_app.config["ACCESS_TOKEN_MAX_AGE"]
        )
        return data if isinstance(data, dict) and "user_id" in data and "person_id" in data else None
    except (BadSignature, SignatureExpired, TypeError, ValueError):
        return None


def is_admin():
    return getattr(g, "user_id", None) in current_app.config["ADMIN_USER_IDS"]


def protect_request():
    if request.method == "OPTIONS":
        return "", 204

    path = request.path.rstrip("/") or "/"
    if path == "/health":
        return None
    if path == "/" or path.startswith("/static/") or path == "/api/documentacion" or path.startswith("/api/documentacion/"):
        return None
    if path == "/api/usuarios/login" and request.method == "POST":
        return None
    if path == "/api/usuarios/registro" and request.method == "POST":
        return None
    is_service_path = path == "/api/servicios" or path.startswith("/api/servicios/")
    if is_service_path and request.method == "GET":
        return None

    payload = read_access_token()
    if payload is None:
        return jsonify({"mensaje": "Inicia sesión para continuar"}), 401
    try:
        g.user_id = int(payload["user_id"])
        g.person_id = int(payload["person_id"])
    except (TypeError, ValueError, KeyError):
        return jsonify({"mensaje": "Token inválido"}), 401

    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT USU_PER_ID FROM T_USUARIO WHERE USU_ID = %s", (g.user_id,))
    account = cursor.fetchone()
    cursor.close()
    if account is None or int(account[0]) != g.person_id:
        return jsonify({"mensaje": "La sesión ya no es válida"}), 401

    admin_prefixes = (
        "/api/roles", "/api/empleados", "/api/respuestas",
        "/api/servicios-agenda", "/api/pagos", "/api/consultas",
    )
    admin_only = any(path == prefix or path.startswith(prefix + "/") for prefix in admin_prefixes)
    if is_service_path and request.method != "GET":
        admin_only = True
    if (path == "/api/personas" or path.startswith("/api/personas/")) and request.method in {"POST", "DELETE"}:
        admin_only = True
    if admin_only and not is_admin():
        return jsonify({"mensaje": "No tienes permisos para esta operación"}), 403
    return None
