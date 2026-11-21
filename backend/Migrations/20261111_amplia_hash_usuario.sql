-- Amplía el campo para almacenar hashes Werkzeug completos.
ALTER TABLE T_USUARIO
    MODIFY USU_CONTRASEÑA VARCHAR(255) NULL;
