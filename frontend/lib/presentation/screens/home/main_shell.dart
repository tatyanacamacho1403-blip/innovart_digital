import 'package:flutter/material.dart';

import '../../../logic/auth_service.dart';
import '../../../logic/service_controller.dart';
import 'appointments_screen.dart';
import 'private_area_shell.dart';
import 'profile_screen.dart';
import 'services_screen.dart';

/// Estructura común del área privada y navegación entre sus tres secciones.
class MainShell extends StatefulWidget {
  const MainShell({
    super.key,
    this.initialIndex = 0,
    this.developmentCatalogOnly = false,
  });

  final int initialIndex;
  final bool developmentCatalogOnly;

  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {
  late int _index = widget.initialIndex.clamp(0, 2).toInt();

  @override
  void initState() {
    super.initState();
    final user = AuthService.instance.currentUser;
    if (widget.developmentCatalogOnly) {
      ServiceController.instance.loadCatalog();
    } else if (user != null) {
      ServiceController.instance.loadFor(user);
    }
  }

  List<Widget> get _screens => [
    ServicesScreen(
      onViewAppointments: () => setState(() => _index = 2),
      onSelectSection: (index) => setState(() => _index = index),
    ),
    const ProfileScreen(),
    const AppointmentsScreen(),
  ];

  @override
  Widget build(BuildContext context) => PrivateAreaShell(
    currentIndex: _index,
    onSelect: (index) => setState(() => _index = index),
    child: IndexedStack(index: _index, children: _screens),
  );
}
