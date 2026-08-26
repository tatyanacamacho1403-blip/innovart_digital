USE InnovartDigital;

-- t_respusta ES la tabla que debe permanecer:
-- t_empleado.EMP_RES_ID -> t_respusta.RES_ID
--
-- t_respuesta es la tabla duplicada/no utilizada.
-- Ejecuta este script DESPUES de importar el dump de la BD.

DROP TABLE IF EXISTS t_respuesta;

SHOW TABLES;
