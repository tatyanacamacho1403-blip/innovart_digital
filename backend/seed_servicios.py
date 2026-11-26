"""Carga controlada e idempotente del catálogo de servicios.

Por defecto solo simula. Use --apply para escribir en la base configurada.
"""
import argparse
import sys
import unicodedata
import uuid

from App import app


SERVICES = (
    {
        "nombre": "Mantenimiento eléctrico",
        "tipo": "Eléctrico",
        "resumen": "Instalación, inspección y mantenimiento de sistemas eléctricos empresariales.",
        "descripcion": "Mantenimiento preventivo y correctivo de instalaciones eléctricas para identificar riesgos, corregir fallas y mantener en buen estado los sistemas de su empresa.",
        "actividades": [
            "Revisión de tableros y protecciones eléctricas",
            "Inspección de conexiones, circuitos y puntos de consumo",
            "Detección y corrección de fallas eléctricas",
            "Mantenimiento de instalaciones y componentes",
        ],
        "beneficios": [
            "Mayor seguridad para las personas y las instalaciones",
            "Menos interrupciones por fallas eléctricas",
            "Mejor conservación de los equipos",
        ],
    },
    {
        "nombre": "Sistemas de refrigeración",
        "tipo": "Refrigeración",
        "resumen": "Mantenimiento preventivo y correctivo de refrigeración y aire acondicionado.",
        "descripcion": "Revisión, mantenimiento y reparación de equipos y sistemas de refrigeración empresarial para apoyar su funcionamiento y eficiencia.",
        "actividades": [
            "Inspección de equipos y componentes",
            "Limpieza y mantenimiento preventivo",
            "Revisión de conexiones y controles",
            "Diagnóstico y corrección de fallas",
        ],
        "beneficios": [
            "Funcionamiento confiable de los equipos",
            "Detección oportuna de fallas",
            "Mejor conservación de los espacios y productos",
        ],
    },
    {
        "nombre": "Sistemas hidrosanitarios",
        "tipo": "Hidrosanitario",
        "resumen": "Instalación y mantenimiento de redes hidráulicas y sanitarias.",
        "descripcion": "Atención de redes de suministro y evacuación de agua en instalaciones empresariales, con revisión de tuberías, conexiones y puntos hidráulicos.",
        "actividades": [
            "Inspección de tuberías y conexiones",
            "Reparación de fugas y obstrucciones",
            "Mantenimiento de redes hidráulicas y sanitarias",
            "Revisión de puntos de suministro y evacuación",
        ],
        "beneficios": [
            "Reducción de fugas y daños por humedad",
            "Continuidad en el suministro y evacuación de agua",
            "Conservación de la infraestructura",
        ],
    },
    {
        "nombre": "Servicios constructivos",
        "tipo": "Constructivo",
        "resumen": "Adecuación de infraestructura y reparaciones locativas empresariales.",
        "descripcion": "Mantenimiento y adecuación de infraestructura empresarial mediante reparaciones locativas y trabajos de conservación de instalaciones.",
        "actividades": [
            "Reparaciones locativas",
            "Adecuación de espacios e instalaciones",
            "Mantenimiento de acabados y elementos constructivos",
            "Trabajos de conservación de infraestructura",
        ],
        "beneficios": [
            "Espacios de trabajo funcionales y conservados",
            "Atención oportuna del deterioro",
            "Adecuaciones acordes con las necesidades del negocio",
        ],
    },
    {
        "nombre": "Metalmecánica",
        "tipo": "Metalmecánica",
        "resumen": "Mantenimiento, reparación y fabricación de elementos metálicos.",
        "descripcion": "Soluciones de mantenimiento y fabricación de elementos metálicos relacionados con la infraestructura y operación empresarial.",
        "actividades": [
            "Reparación de elementos y estructuras metálicas",
            "Fabricación de componentes según requerimiento",
            "Mantenimiento de piezas y soportes",
            "Inspección de elementos metálicos instalados",
        ],
        "beneficios": [
            "Recuperación de elementos metálicos",
            "Soluciones adaptadas a la infraestructura",
            "Mayor vida útil de componentes y soportes",
        ],
    },
)


def normalize_name(value):
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(char for char in value if not unicodedata.combining(char))
    return " ".join(value.split())


def service_description(service):
    activities = "\n".join("- " + item for item in service["actividades"])
    benefits = "\n".join("- " + item for item in service["beneficios"])
    return "Resumen: {0}\n\nDescripción: {1}\n\nActividades:\n{2}\n\nBeneficios:\n{3}".format(
        service["resumen"], service["descripcion"], activities, benefits
    )


def main():
    parser = argparse.ArgumentParser(description="Carga controlada de T_SERVICIO")
    parser.add_argument(
        "--apply", action="store_true", help="inserta los servicios que falten"
    )
    args = parser.parse_args()

    connection = None
    cursor = None
    try:
        with app.app_context():
            database = app.config.get("MYSQL_DB", "(no configurada)")
            print("Base de datos configurada: {0}".format(database))
            connection = app.mysql.connection
            cursor = connection.cursor()
            cursor.execute("SELECT SER_NOMBRE FROM T_SERVICIO")
            existing_names = {normalize_name(row[0]) for row in cursor.fetchall()}

            existing = []
            pending = []
            for service in SERVICES:
                if normalize_name(service["nombre"]) in existing_names:
                    existing.append(service["nombre"])
                else:
                    pending.append(
                        dict(service, uuid=str(uuid.uuid4()), precio=0, estado="Activo")
                    )

            print("\nServicios ya existentes ({0}):".format(len(existing)))
            for name in existing:
                print("  - " + name)
            print("\nServicios pendientes ({0}):".format(len(pending)))
            for service in pending:
                action = "registrado" if args.apply else "se registraría"
                print("  - {0}: {1} (precio 0, estado Activo)".format(service["nombre"], action))

            registered = 0
            if args.apply and pending:
                statement = (
                    "INSERT INTO T_SERVICIO "
                    "(SER_UUID, SER_NOMBRE, SER_DESCRIPCION, SER_PRECIO, SER_TIPO, SER_ESTADO) "
                    "VALUES (%s, %s, %s, %s, %s, %s)"
                )
                for service in pending:
                    cursor.execute(
                        statement,
                        (
                            service["uuid"], service["nombre"], service_description(service),
                            service["precio"], service["tipo"], service["estado"],
                        ),
                    )
                    registered += 1
                connection.commit()

            print(
                "\nResumen: existentes={0}, pendientes={1}, registrados={2}, modo={3}".format(
                    len(existing), len(pending), registered,
                    "aplicar" if args.apply else "simulación",
                )
            )
    except Exception as error:
        if connection is not None:
            try:
                connection.rollback()
            except Exception:
                # Flask-MySQLdb cierra esta conexión al finalizar el contexto.
                pass
        print(
            "Error en la carga de servicios: {0}: {1}".format(
                type(error).__name__, error
            ),
            file=sys.stderr,
        )
        return 1
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                # Un error limpiando el cursor no debe reemplazar el resultado
                # de la consulta; Flask administra y cierra la conexión.
                pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
