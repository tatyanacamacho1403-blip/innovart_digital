/// Convierte fechas y horas a texto legible, sin librerías externas.
class DateFormatter {
  DateFormatter._();

  static String date(DateTime d) => '${_two(d.day)}/${_two(d.month)}/${d.year}';

  static String time(DateTime d) => '${_two(d.hour)}:${_two(d.minute)}';

  static String _two(int n) => n.toString().padLeft(2, '0');
}
