BASE DE DATOS ESPERADA

La API está preparada para estas 10 tablas:

t_agenda
t_consulta
t_empleado
t_pago
t_persona
t_respusta
t_rol
t_servicio
t_servicio_agenda
t_usuario

NO se utiliza t_respuesta.

Importante:
- t_respusta se conserva porque t_empleado.EMP_RES_ID referencia
  t_respusta.RES_ID.
- t_respuesta es la tabla duplicada/no utilizada y se elimina con
  ELIMINAR_T_RESPUESTA.sql.

Primero importa el dump de InnovartDigital.
Después ejecuta ELIMINAR_T_RESPUESTA.sql.
Finalmente ejecuta VERIFICAR_INNOVARTDIGITAL.sql para comprobar
tablas, columnas y llaves foráneas.
