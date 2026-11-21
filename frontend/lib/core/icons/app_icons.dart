import 'package:flutter/material.dart';

/// Todos los iconos de la app centralizados.
/// Si quieres cambiar un icono, lo cambias aquí y se actualiza en todas las pantallas.
class AppIcons {
  AppIcons._();

  // Formularios
  static const IconData email = Icons.email_outlined;
  static const IconData lock = Icons.lock_outline;
  static const IconData person = Icons.person_outline;
  static const IconData visibility = Icons.visibility_outlined;
  static const IconData visibilityOff = Icons.visibility_off_outlined;

  // Navegación inferior
  static const IconData home = Icons.home_outlined;
  static const IconData homeSelected = Icons.home;
  static const IconData services = Icons.event_note_outlined;
  static const IconData servicesSelected = Icons.event_note;
  static const IconData profile = Icons.account_circle_outlined;
  static const IconData profileSelected = Icons.account_circle;

  // Acciones y datos
  static const IconData add = Icons.add;
  static const IconData delete = Icons.delete_outline;
  static const IconData logout = Icons.logout;
  static const IconData calendar = Icons.calendar_today_outlined;
  static const IconData clock = Icons.access_time;
}
