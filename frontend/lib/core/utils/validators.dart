/// Funciones de validación para los formularios.
/// Cada una devuelve null si todo está bien, o el mensaje de error.
class Validators {
  Validators._();

  static String? required(String? value, {String field = 'Este campo'}) {
    if (value == null || value.trim().isEmpty) return '$field es obligatorio';
    return null;
  }

  static String? email(String? value) {
    final base = required(value, field: 'El correo');
    if (base != null) return base;
    final ok = RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch(value!.trim());
    return ok ? null : 'Correo no válido';
  }

  static String? password(String? value) {
    final base = required(value, field: 'La contraseña');
    if (base != null) return base;
    return value!.length < 8 ? 'Mínimo 8 caracteres' : null;
  }

  static String? date(String? value) {
    final base = required(value, field: 'La fecha de nacimiento');
    if (base != null) return base;
    final parsed = DateTime.tryParse(value!.trim());
    return parsed == null ||
            !RegExp(r'^\d{4}-\d{2}-\d{2}$').hasMatch(value.trim())
        ? 'Usa el formato AAAA-MM-DD'
        : null;
  }

  static String? Function(String?) confirmPassword(String Function() original) {
    return (value) =>
        value == original() ? null : 'Las contraseñas no coinciden';
  }
}
