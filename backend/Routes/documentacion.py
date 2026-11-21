from flask import Blueprint, current_app, jsonify, render_template_string


documentacion_bp = Blueprint("documentacion", __name__)


@documentacion_bp.route("/swagger.json")
@documentacion_bp.route("/openapi.json")
def swagger_json():
    paths = {}
    public = {
        ("/api/usuarios/login", "post"), ("/api/usuarios/registro", "post"),
        ("/api/servicios", "get"), ("/api/servicios/{id}", "get"),
    }
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint == "static" or rule.rule.startswith("/api/documentacion") or rule.rule == "/":
            continue
        path = (rule.rule.rstrip("/") or "/").replace("<int:", "{").replace("<string:", "{").replace(">", "}")
        operations = paths.setdefault(path, {})
        for method in sorted(rule.methods - {"HEAD", "OPTIONS"}):
            operation = {"summary": f"{method} {path}", "responses": {"200": {"description": "Operación exitosa"}}}
            if "id" in rule.arguments:
                operation["parameters"] = [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}]
            if method in {"POST", "PUT", "PATCH"}:
                operation["requestBody"] = {"required": True, "content": {"application/json": {"schema": {"type": "object"}}}}
            if (path, method.lower()) not in public:
                operation["security"] = [{"BearerAuth": []}]
            operations[method.lower()] = operation
    return jsonify({
        "openapi": "3.0.3",
        "info": {"title": "Agenda de servicios API", "version": "1.0.0"},
        "servers": [{"url": "/"}],
        "components": {"securitySchemes": {"BearerAuth": {"type": "http", "scheme": "bearer"}}},
        "paths": paths,
    })


@documentacion_bp.route("/")
def swagger_ui():
    return render_template_string("""<!DOCTYPE html><html><head><title>API Agenda</title>
<link href="/static/swagger-ui/swagger-ui.css" rel="stylesheet" /></head>
<body><div id="swagger-ui"></div><script src="/static/swagger-ui/swagger-ui-bundle.js"></script>
<script>SwaggerUIBundle({url: "./openapi.json", dom_id: '#swagger-ui'});</script></body></html>""")
