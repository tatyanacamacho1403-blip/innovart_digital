import 'package:flutter/material.dart';

class InnovartService {
  const InnovartService({
    required this.name,
    required this.summary,
    required this.description,
    required this.activities,
    required this.benefits,
    required this.icon,
    required this.tint,
    required this.accent,
  });

  final String name;
  final String summary;
  final String description;
  final List<String> activities;
  final List<String> benefits;
  final IconData icon;
  final Color tint;
  final Color accent;
}

const innovartServices = <InnovartService>[
  InnovartService(
    name: 'Mantenimiento eléctrico',
    summary: 'Instalación, inspección y mantenimiento de sistemas eléctricos empresariales.',
    description: 'Mantenimiento preventivo y correctivo de instalaciones eléctricas para identificar riesgos, corregir fallas y mantener en buen estado los sistemas de su empresa.',
    activities: [
      'Revisión de tableros y protecciones eléctricas',
      'Inspección de conexiones, circuitos y puntos de consumo',
      'Detección y corrección de fallas eléctricas',
      'Mantenimiento de instalaciones y componentes',
    ],
    benefits: [
      'Mayor seguridad para las personas y las instalaciones',
      'Menos interrupciones por fallas eléctricas',
      'Mejor conservación de los equipos',
    ],
    icon: Icons.bolt_rounded,
    tint: Color(0xFFF0EAFF),
    accent: Color(0xFF5537E8),
  ),
  InnovartService(
    name: 'Sistemas de refrigeración',
    summary: 'Mantenimiento preventivo y correctivo de refrigeración y aire acondicionado.',
    description: 'Revisión, mantenimiento y reparación de equipos y sistemas de refrigeración empresarial para apoyar su funcionamiento y eficiencia.',
    activities: [
      'Inspección de equipos y componentes',
      'Limpieza y mantenimiento preventivo',
      'Revisión de conexiones y controles',
      'Diagnóstico y corrección de fallas',
    ],
    benefits: [
      'Funcionamiento confiable de los equipos',
      'Detección oportuna de fallas',
      'Mejor conservación de los espacios y productos',
    ],
    icon: Icons.ac_unit_rounded,
    tint: Color(0xFFE9F3FF),
    accent: Color(0xFF1870D5),
  ),
  InnovartService(
    name: 'Sistemas hidrosanitarios',
    summary: 'Instalación y mantenimiento de redes hidráulicas y sanitarias.',
    description: 'Atención de redes de suministro y evacuación de agua en instalaciones empresariales, con revisión de tuberías, conexiones y puntos hidráulicos.',
    activities: [
      'Inspección de tuberías y conexiones',
      'Reparación de fugas y obstrucciones',
      'Mantenimiento de redes hidráulicas y sanitarias',
      'Revisión de puntos de suministro y evacuación',
    ],
    benefits: [
      'Reducción de fugas y daños por humedad',
      'Continuidad en el suministro y evacuación de agua',
      'Conservación de la infraestructura',
    ],
    icon: Icons.water_drop_outlined,
    tint: Color(0xFFE8F2FF),
    accent: Color(0xFF2476D2),
  ),
  InnovartService(
    name: 'Servicios constructivos',
    summary:
        'Adecuación de infraestructura y reparaciones locativas empresariales.',
    description: 'Mantenimiento y adecuación de infraestructura empresarial mediante reparaciones locativas y trabajos de conservación de instalaciones.',
    activities: [
      'Reparaciones locativas',
      'Adecuación de espacios e instalaciones',
      'Mantenimiento de acabados y elementos constructivos',
      'Trabajos de conservación de infraestructura',
    ],
    benefits: [
      'Espacios de trabajo funcionales y conservados',
      'Atención oportuna del deterioro',
      'Adecuaciones acordes con las necesidades del negocio',
    ],
    icon: Icons.construction_rounded,
    tint: Color(0xFFFFF2D8),
    accent: Color(0xFFE0A000),
  ),
  InnovartService(
    name: 'Metalmecánica',
    summary: 'Mantenimiento, reparación y fabricación de elementos metálicos.',
    description: 'Soluciones de mantenimiento y fabricación de elementos metálicos relacionados con la infraestructura y operación empresarial.',
    activities: [
      'Reparación de elementos y estructuras metálicas',
      'Fabricación de componentes según requerimiento',
      'Mantenimiento de piezas y soportes',
      'Inspección de elementos metálicos instalados',
    ],
    benefits: [
      'Recuperación de elementos metálicos',
      'Soluciones adaptadas a la infraestructura',
      'Mayor vida útil de componentes y soportes',
    ],
    icon: Icons.settings_outlined,
    tint: Color(0xFFF0F1F4),
    accent: Color(0xFF53617B),
  ),
];

String normalizeServiceName(String value) {
  const from = 'áéíóúüñ';
  const to = 'aeiouun';
  var normalized = value.toLowerCase();
  for (var index = 0; index < from.length; index++) {
    normalized = normalized.replaceAll(from[index], to[index]);
  }
  return normalized.replaceAll(RegExp(r'[^a-z0-9]+'), ' ').trim();
}
