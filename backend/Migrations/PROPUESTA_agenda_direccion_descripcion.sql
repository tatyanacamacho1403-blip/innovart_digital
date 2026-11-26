-- Propuesta únicamente. Inspeccionar T_AGENDA y confirmar que ambas columnas
-- no existen antes de ejecutar este ALTER en el entorno autorizado.
-- No se ha ejecutado desde el proceso de desarrollo.
ALTER TABLE T_AGENDA
    ADD COLUMN AGE_DIRECCION VARCHAR(255) NULL,
    ADD COLUMN AGE_DESCRIPCION TEXT NULL;
