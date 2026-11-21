import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../logic/auth_service.dart';

class PrivateAreaShell extends StatelessWidget {
  const PrivateAreaShell({
    super.key,
    required this.currentIndex,
    required this.onSelect,
    required this.child,
    this.onBack,
  });

  final int currentIndex;
  final ValueChanged<int> onSelect;
  final Widget child;
  final VoidCallback? onBack;

  @override
  Widget build(BuildContext context) {
    final user = AuthService.instance.currentUser;
    final wide = MediaQuery.sizeOf(context).width >= 900;
    final initials = user?.name.trim().isNotEmpty == true
        ? user!.name.trim()[0].toUpperCase()
        : '?';

    return Scaffold(
      backgroundColor: AppColors.navy,
      drawer: wide
          ? null
          : _WorkspaceDrawer(currentIndex: currentIndex, onSelect: onSelect),
      body: SafeArea(
        child: Column(
          children: [
            SizedBox(
              height: 76,
              child: Row(
                children: [
                  if (!wide)
                    Builder(
                      builder: (context) => IconButton(
                        onPressed: () => Scaffold.of(context).openDrawer(),
                        color: AppColors.white,
                        icon: const Icon(Icons.menu_rounded),
                      ),
                    ),
                  if (onBack != null)
                    IconButton(
                      onPressed: onBack,
                      color: AppColors.white,
                      icon: const Icon(Icons.arrow_back_rounded),
                    ),
                  const SizedBox(width: 22),
                  const Icon(Icons.hexagon_rounded, color: AppColors.violet),
                  const SizedBox(width: 10),
                  const Text(
                    'INNOVART',
                    style: TextStyle(
                      color: AppColors.white,
                      fontSize: 17,
                      fontWeight: FontWeight.w900,
                      letterSpacing: 1.5,
                    ),
                  ),
                  const SizedBox(width: 6),
                  const Text(
                    'DIGITAL',
                    style: TextStyle(
                      color: AppColors.violet,
                      fontSize: 11,
                      fontWeight: FontWeight.w800,
                      letterSpacing: 1.4,
                    ),
                  ),
                  const Spacer(),
                  if (user != null) ...[
                    if (wide)
                      Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Text(
                            user.name,
                            style: const TextStyle(
                              color: AppColors.white,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                          Text(
                            user.email,
                            style: const TextStyle(
                              color: AppColors.secondaryText,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    const SizedBox(width: 12),
                    CircleAvatar(
                      radius: 19,
                      backgroundColor: AppColors.purple,
                      child: Text(
                        initials,
                        style: const TextStyle(
                          color: AppColors.white,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                    ),
                  ] else
                    const Text(
                      'Modo de prueba',
                      style: TextStyle(color: AppColors.secondaryText),
                    ),
                  const SizedBox(width: 24),
                ],
              ),
            ),
            Expanded(
              child: Row(
                children: [
                  if (wide)
                    _WorkspaceNavigation(
                      currentIndex: currentIndex,
                      onSelect: onSelect,
                    ),
                  Expanded(
                    child: Stack(
                      children: [
                        Positioned.fill(child: child),
                        const Positioned(
                          right: -70,
                          top: -100,
                          child: IgnorePointer(
                            child: _DiagonalAccent(size: 290, angle: -.5),
                          ),
                        ),
                        const Positioned(
                          left: 150,
                          bottom: -210,
                          child: IgnorePointer(
                            child: _DiagonalAccent(size: 360, angle: .55),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: wide
          ? null
          : NavigationBar(
              selectedIndex: currentIndex,
              onDestinationSelected: onSelect,
              destinations: const [
                NavigationDestination(
                  icon: Icon(Icons.home_repair_service_outlined),
                  selectedIcon: Icon(Icons.home_repair_service_rounded),
                  label: 'Servicios',
                ),
                NavigationDestination(
                  icon: Icon(Icons.person_outline_rounded),
                  selectedIcon: Icon(Icons.person_rounded),
                  label: 'Mi Perfil',
                ),
                NavigationDestination(
                  icon: Icon(Icons.event_note_outlined),
                  selectedIcon: Icon(Icons.event_note_rounded),
                  label: 'Mis Citas',
                ),
              ],
            ),
    );
  }
}

class _WorkspaceDrawer extends StatelessWidget {
  const _WorkspaceDrawer({required this.currentIndex, required this.onSelect});
  final int currentIndex;
  final ValueChanged<int> onSelect;

  @override
  Widget build(BuildContext context) => Drawer(
    backgroundColor: AppColors.navyLight,
    child: SafeArea(
      child: _WorkspaceNavigation(
        currentIndex: currentIndex,
        onSelect: (index) {
          Navigator.pop(context);
          onSelect(index);
        },
      ),
    ),
  );
}

class _WorkspaceNavigation extends StatelessWidget {
  const _WorkspaceNavigation({
    required this.currentIndex,
    required this.onSelect,
  });
  final int currentIndex;
  final ValueChanged<int> onSelect;

  static const _items = [
    (Icons.home_repair_service_outlined, 'Servicios'),
    (Icons.person_outline_rounded, 'Mi Perfil'),
    (Icons.event_note_outlined, 'Mis Citas'),
  ];

  @override
  Widget build(BuildContext context) => Container(
    width: 238,
    color: AppColors.navyLight,
    padding: const EdgeInsets.fromLTRB(18, 30, 18, 18),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Padding(
          padding: EdgeInsets.fromLTRB(14, 4, 14, 20),
          child: Text(
            'ÁREA DE CLIENTE',
            style: TextStyle(
              color: AppColors.secondaryText,
              fontSize: 11,
              fontWeight: FontWeight.w800,
              letterSpacing: 1.2,
            ),
          ),
        ),
        for (var i = 0; i < _items.length; i++)
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: _NavigationEntry(
              icon: _items[i].$1,
              label: _items[i].$2,
              selected: i == currentIndex,
              onTap: () => onSelect(i),
            ),
          ),
      ],
    ),
  );
}

class _NavigationEntry extends StatelessWidget {
  const _NavigationEntry({
    required this.icon,
    required this.label,
    required this.selected,
    required this.onTap,
  });
  final IconData icon;
  final String label;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Material(
    color: selected ? AppColors.purple : Colors.transparent,
    borderRadius: BorderRadius.circular(13),
    child: InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(13),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 13),
        child: Row(
          children: [
            Icon(icon, size: 20, color: AppColors.white),
            const SizedBox(width: 12),
            Text(
              label,
              style: const TextStyle(
                color: AppColors.white,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
      ),
    ),
  );
}

class _DiagonalAccent extends StatelessWidget {
  const _DiagonalAccent({required this.size, required this.angle});
  final double size;
  final double angle;

  @override
  Widget build(BuildContext context) => Transform.rotate(
    angle: angle,
    child: Container(
      width: size,
      height: size * .45,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(44),
        border: Border.all(
          color: AppColors.violet.withValues(alpha: .18),
          width: 2,
        ),
        color: AppColors.purple.withValues(alpha: .07),
      ),
    ),
  );
}
