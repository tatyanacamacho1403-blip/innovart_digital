# Backend de Agenda de Servicios

API REST Flask y MySQL. Ejecuta desde esta carpeta:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r Requirements.txt
cp .env.example .env
python run.py
```

En Windows activa el entorno con `.venv\Scripts\activate`. La base de datos `InnovartDigital` y sus tablas deben existir antes de iniciar la API; el repositorio no incluye un script SQL de creación.

## Flutter

- Emulador Android: `http://10.0.2.2:5000` (valor predeterminado del frontend).
- Navegador/escritorio: `http://localhost:5000` o `http://127.0.0.1:5000`.
- Dispositivo físico: usa `flutter run --dart-define=API_BASE_URL=http://IP_DEL_COMPUTADOR:5000`; ambos deben estar en la misma red.

## Administración

El login entrega un token Bearer con vencimiento configurable. Define `SECRET_KEY` con un secreto aleatorio antes de producción. En desarrollo el token predeterminado es solo para facilitar la ejecución local.

Las operaciones administrativas (usuarios globales, roles, empleados, catálogo de servicios, pagos, consultas y respuestas) exigen que el ID de usuario esté incluido en `ADMIN_USER_IDS`, separado por comas. Configúralo en `.env` después de crear la cuenta administradora. Un usuario normal solo puede leer el catálogo y consultar o gestionar sus propias citas y perfil.

`FLASK_DEBUG=1` activa depuración local. Déjalo desactivado fuera del desarrollo.
