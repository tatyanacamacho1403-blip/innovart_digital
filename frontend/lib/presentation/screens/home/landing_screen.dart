import 'package:flutter/material.dart';

import '../../../core/constants/app_routes.dart';
import '../../../logic/auth_service.dart';

const _navy = Color(0xFF050D29);
const _ink = Color(0xFF101A3C);
const _purple = Color(0xFF6848F5);
const _violet = Color(0xFF8D64FF);
const _muted = Color(0xFF586078);
const _line = Color(0xFFE4E7F0);

class LandingScreen extends StatefulWidget {
  const LandingScreen({super.key});

  @override
  State<LandingScreen> createState() => _LandingScreenState();
}

class _LandingScreenState extends State<LandingScreen> {
  final _scrollController = ScrollController();
  final _servicesKey = GlobalKey();
  final _aboutKey = GlobalKey();

  static const _services = <_ServiceInfo>[
    _ServiceInfo(
      'Mantenimiento eléctrico',
      'Instalación, revisión y mantenimiento de sistemas eléctricos empresariales.',
      Icons.bolt_rounded,
      Color(0xFFF0EAFF),
      Color(0xFF5537E8),
    ),
    _ServiceInfo(
      'Sistemas de refrigeración',
      'Mantenimiento preventivo y correctivo de refrigeración y aire acondicionado.',
      Icons.ac_unit_rounded,
      Color(0xFFE9F3FF),
      Color(0xFF1870D5),
    ),
    _ServiceInfo(
      'Sistemas hidrosanitarios',
      'Instalación, reparación y mantenimiento de redes hidráulicas y sanitarias.',
      Icons.water_drop_outlined,
      Color(0xFFE8F2FF),
      Color(0xFF2476D2),
    ),
    _ServiceInfo(
      'Servicios constructivos',
      'Reparaciones locativas, estructuras y obras civiles para infraestructura empresarial.',
      Icons.construction_rounded,
      Color(0xFFFFF2D8),
      Color(0xFFE0A000),
    ),
    _ServiceInfo(
      'Metalmecánica',
      'Fabricación, reparación y mantenimiento de estructuras y componentes metálicos.',
      Icons.settings_outlined,
      Color(0xFFF0F1F4),
      Color(0xFF53617B),
    ),
  ];

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    // Restore credentials in the background while keeping the public page
    // available. Authenticated visitors can use the booking entry directly.
    AuthService.instance.restoreSession();
  }

  void _scrollTo(GlobalKey key) {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      final target = key.currentContext;
      if (target == null) return;
      Scrollable.ensureVisible(
        target,
        duration: const Duration(milliseconds: 500),
        curve: Curves.easeInOut,
        alignment: .04,
      );
    });
  }

  void _openAuth(String route) => Navigator.pushNamed(context, route);

  void _goHome() =>
      Navigator.pushNamedAndRemoveUntil(context, AppRoutes.home, (_) => false);

  void _showContact() => showDialog<void>(
    context: context,
    builder: (dialogContext) => AlertDialog(
      title: const Text('Contacto Innovart Digital'),
      content: const Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: Icon(Icons.phone_outlined, color: _purple),
            title: Text('+57 300 123 4567'),
          ),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: Icon(Icons.email_outlined, color: _purple),
            title: Text('contacto@innovartdigital.com'),
          ),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: Icon(Icons.location_on_outlined, color: _purple),
            title: Text('Barranquilla, Colombia'),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(dialogContext),
          child: const Text('Cerrar'),
        ),
      ],
    ),
  );

  void _bookService() {
    if (AuthService.instance.currentUser != null) {
      Navigator.pushNamed(context, AppRoutes.main, arguments: 0);
    } else {
      Navigator.pushNamed(context, AppRoutes.login, arguments: 'services');
    }
  }

  void _openService(_ServiceInfo service) {
    showDialog<void>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        icon: Icon(service.icon, color: service.accent, size: 32),
        title: Text(service.title, textAlign: TextAlign.center),
        content: Text(service.description, textAlign: TextAlign.center),
        actionsAlignment: MainAxisAlignment.center,
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext),
            child: const Text('Cerrar'),
          ),
          FilledButton(
            onPressed: () {
              Navigator.pop(dialogContext);
              _bookService();
            },
            style: FilledButton.styleFrom(backgroundColor: _purple),
            child: const Text('Agendar servicio'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    backgroundColor: Colors.white,
    body: LayoutBuilder(
      builder: (context, constraints) {
        final wide = constraints.maxWidth >= 1100;
        return SingleChildScrollView(
          controller: _scrollController,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Container(
                color: _navy,
                child: SafeArea(
                  bottom: false,
                  child: _Header(
                    wide: wide,
                    onHome: _goHome,
                    onAbout: () => _scrollTo(_aboutKey),
                    onServices: () => _scrollTo(_servicesKey),
                    onAgenda: _bookService,
                    onContact: _showContact,
                    onLogin: () => _openAuth(AppRoutes.login),
                    onRegister: () => _openAuth(AppRoutes.register),
                  ),
                ),
              ),
              _Hero(
                wide: wide,
                onBook: _bookService,
                onLearnMore: () => _scrollTo(_aboutKey),
              ),
              _FeaturesBar(wide: wide),
              _ServicesSection(
                anchorKey: _servicesKey,
                wide: wide,
                onSelect: _openService,
              ),
              _ProcessSection(wide: wide),
              _WhySection(
                anchorKey: _aboutKey,
                wide: wide,
                onBook: _bookService,
              ),
            ],
          ),
        );
      },
    ),
  );
}

class _Header extends StatelessWidget {
  const _Header({
    required this.wide,
    required this.onHome,
    required this.onAbout,
    required this.onServices,
    required this.onAgenda,
    required this.onContact,
    required this.onLogin,
    required this.onRegister,
  });
  final bool wide;
  final VoidCallback onHome,
      onAbout,
      onServices,
      onAgenda,
      onContact,
      onLogin,
      onRegister;

  @override
  Widget build(BuildContext context) => Container(
    color: _navy,
    padding: EdgeInsets.symmetric(horizontal: wide ? 42 : 18, vertical: 12),
    child: Row(
      children: [
        const _Brand(),
        const Spacer(),
        if (wide) ...[
          _NavLink('INICIO', onHome, selected: true),
          _NavLink('NOSOTROS', onAbout),
          _NavLink('SERVICIOS', onServices),
          _NavLink('AGENDA', onAgenda),
          _NavLink('CONTACTO', onContact),
          const SizedBox(width: 18),
          _HeaderButton(
            label: 'Iniciar sesión',
            icon: Icons.person_outline,
            onPressed: onLogin,
          ),
          const SizedBox(width: 10),
          _HeaderButton(
            label: 'Registrarse',
            icon: Icons.person_add_alt_1,
            onPressed: onRegister,
            filled: true,
          ),
        ] else ...[
          IconButton(
            onPressed: () => showModalBottomSheet<void>(
              context: context,
              backgroundColor: _navy,
              builder: (_) => SafeArea(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    _SheetLink('Inicio', onHome),
                    _SheetLink('Nosotros', onAbout),
                    _SheetLink('Servicios', onServices),
                    _SheetLink('Agenda', onAgenda),
                    _SheetLink('Contacto', onContact),
                    _SheetLink('Iniciar sesión', onLogin),
                    _SheetLink('Registrarse', onRegister),
                  ],
                ),
              ),
            ),
            icon: const Icon(Icons.menu_rounded, color: Colors.white),
          ),
        ],
      ],
    ),
  );
}

class _Brand extends StatelessWidget {
  const _Brand();
  @override
  Widget build(BuildContext context) => Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      Container(
        width: 35,
        height: 38,
        decoration: BoxDecoration(
          border: Border.all(color: _violet, width: 2),
          borderRadius: BorderRadius.circular(8),
        ),
        child: const Icon(
          Icons.change_history_rounded,
          color: _violet,
          size: 28,
        ),
      ),
      const SizedBox(width: 10),
      const Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'INNOVART',
            style: TextStyle(
              color: Colors.white,
              fontSize: 19,
              height: 1,
              fontWeight: FontWeight.w900,
              letterSpacing: .5,
            ),
          ),
          SizedBox(height: 3),
          Text(
            'D I G I T A L',
            style: TextStyle(
              color: _violet,
              fontSize: 10,
              fontWeight: FontWeight.w800,
              height: 1,
            ),
          ),
        ],
      ),
    ],
  );
}

class _NavLink extends StatelessWidget {
  const _NavLink(this.label, this.onTap, {this.selected = false});
  final String label;
  final VoidCallback onTap;
  final bool selected;
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.symmetric(horizontal: 13),
    child: TextButton(
      onPressed: onTap,
      style: TextButton.styleFrom(
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(vertical: 9),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(0)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            label,
            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 7),
          Container(height: 2, width: selected ? 42 : 0, color: _purple),
        ],
      ),
    ),
  );
}

class _HeaderButton extends StatelessWidget {
  const _HeaderButton({
    required this.label,
    required this.icon,
    required this.onPressed,
    this.filled = false,
  });
  final String label;
  final IconData icon;
  final VoidCallback onPressed;
  final bool filled;
  @override
  Widget build(BuildContext context) => OutlinedButton.icon(
    onPressed: onPressed,
    icon: Icon(icon, size: 17),
    label: Text(label),
    style: OutlinedButton.styleFrom(
      foregroundColor: Colors.white,
      backgroundColor: filled ? _purple : Colors.transparent,
      side: BorderSide(color: filled ? _purple : const Color(0xFF4C4C7C)),
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(7)),
      textStyle: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700),
    ),
  );
}

class _SheetLink extends StatelessWidget {
  const _SheetLink(this.label, this.onTap);
  final String label;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) => ListTile(
    title: Text(label, style: const TextStyle(color: Colors.white)),
    onTap: () {
      Navigator.pop(context);
      onTap();
    },
  );
}

class _Hero extends StatelessWidget {
  const _Hero({
    required this.wide,
    required this.onBook,
    required this.onLearnMore,
  });
  final bool wide;
  final VoidCallback onBook, onLearnMore;
  @override
  Widget build(BuildContext context) => Container(
    color: _navy,
    padding: EdgeInsets.fromLTRB(wide ? 8.7 : 22, 16, wide ? 8.7 : 22, 26),
    child: Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 1360),
        child: wide
            ? Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Expanded(
                    flex: 43,
                    child: _HeroCopy(onBook: onBook, onLearnMore: onLearnMore),
                  ),
                  const SizedBox(width: 30),
                  const Expanded(
                    flex: 57,
                    child: SizedBox(
                      height: 360,
                      child: _IndustrialVisual(),
                    ),
                  ),
                ],
              )
            : Column(
                children: [
                  _HeroCopy(onBook: onBook, onLearnMore: onLearnMore),
                  const SizedBox(height: 22),
                  const SizedBox(height: 245, child: _IndustrialVisual()),
                ],
              ),
      ),
    ),
  );
}

class _HeroCopy extends StatelessWidget {
  const _HeroCopy({required this.onBook, required this.onLearnMore});
  final VoidCallback onBook, onLearnMore;
  @override
  Widget build(BuildContext context) => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text.rich(
        TextSpan(
          children: [
            const TextSpan(text: 'Soluciones de\nmantenimiento\n'),
            TextSpan(
              text: 'integral',
              style: const TextStyle(color: _violet),
            ),
            const TextSpan(text: ' para tu\nempresa'),
          ],
        ),
        style: TextStyle(
          color: Colors.white,
          fontSize: MediaQuery.sizeOf(context).width < 600 ? 34 : 38,
          height: 1.12,
          fontWeight: FontWeight.w800,
          letterSpacing: -.8,
        ),
      ),
      const SizedBox(height: 13),
      ConstrainedBox(
        constraints: BoxConstraints(maxWidth: 470),
        child: Text(
          'En Innovart Digital ofrecemos soluciones especializadas de mantenimiento en diferentes sectores de la ingeniería, comprometidos con la eficiencia, seguridad y calidad en cada servicio.',
          style: TextStyle(color: Color(0xFFD7D9E7), fontSize: 14, height: 1.5),
        ),
      ),
      const SizedBox(height: 19),
      Wrap(
        spacing: 12,
        runSpacing: 10,
        children: [
          FilledButton.icon(
            onPressed: onBook,
            icon: const Icon(Icons.event_available_outlined, size: 18),
            label: const Text('Agendar servicio'),
            style: FilledButton.styleFrom(
              backgroundColor: _purple,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
            ),
          ),
          OutlinedButton.icon(
            onPressed: onLearnMore,
            iconAlignment: IconAlignment.end,
            icon: const Icon(Icons.arrow_forward_rounded, size: 17),
            label: const Text('Conocer más'),
            style: OutlinedButton.styleFrom(
              foregroundColor: Colors.white,
              side: const BorderSide(color: Color(0xFF5D5A91)),
              padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
            ),
          ),
        ],
      ),
    ],
  );
}

/// Ilustración vectorial local para que el hero cargue sin depender de un servidor de imágenes.
class _IndustrialVisual extends StatelessWidget {
  const _IndustrialVisual();
  @override
  Widget build(BuildContext context) => ClipRRect(
    borderRadius: BorderRadius.circular(18),
    child: Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Color(0xFF28374F), Color(0xFF101C36), Color(0xFF17132D)],
        ),
      ),
      child: Stack(
        fit: StackFit.expand,
        children: [
          Positioned(
            right: -40,
            top: -55,
            child: Container(
              width: 240,
              height: 240,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(
                  color: _violet.withValues(alpha: .22),
                  width: 25,
                ),
              ),
            ),
          ),
          Positioned(
            left: -15,
            bottom: -100,
            child: Container(
              width: 260,
              height: 260,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(
                  color: const Color(0xFF26A7D8).withValues(alpha: .18),
                  width: 30,
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(15),
            child: Row(
              children: [
                Expanded(
                  child: _ScenePanel(
                    icon: Icons.electrical_services_rounded,
                    title: 'ELÉCTRICO',
                    tint: const Color(0xFF3C7BBD),
                    worker: Icons.engineering_rounded,
                  ),
                ),
                const SizedBox(width: 9),
                Expanded(
                  child: Column(
                    children: [
                      Expanded(
                        child: _ScenePanel(
                          icon: Icons.ac_unit_rounded,
                          title: 'REFRIGERACIÓN',
                          tint: const Color(0xFF348BB4),
                          worker: Icons.handyman_rounded,
                        ),
                      ),
                      const SizedBox(height: 9),
                      Expanded(
                        child: _ScenePanel(
                          icon: Icons.water_drop_rounded,
                          title: 'HIDROSANITARIO',
                          tint: const Color(0xFF419EAE),
                          worker: Icons.engineering_rounded,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 9),
                Expanded(
                  child: _ScenePanel(
                    icon: Icons.construction_rounded,
                    title: 'CONSTRUCCIÓN',
                    tint: const Color(0xFFB17A35),
                    worker: Icons.construction_rounded,
                  ),
                ),
              ],
            ),
          ),
          Positioned(
            left: 24,
            bottom: 20,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(
                color: _navy.withValues(alpha: .85),
                borderRadius: BorderRadius.circular(25),
                border: Border.all(color: Colors.white24),
              ),
              child: const Row(
                children: [
                  Icon(Icons.verified_rounded, color: _violet, size: 16),
                  SizedBox(width: 7),
                  Text(
                    'Mantenimiento integral empresarial',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 11,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    ),
  );
}

class _ScenePanel extends StatelessWidget {
  const _ScenePanel({
    required this.icon,
    required this.title,
    required this.tint,
    required this.worker,
  });
  final IconData icon, worker;
  final String title;
  final Color tint;
  @override
  Widget build(BuildContext context) => Container(
    clipBehavior: Clip.antiAlias,
    decoration: BoxDecoration(
      borderRadius: BorderRadius.circular(13),
      gradient: LinearGradient(
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
        colors: [
          tint.withValues(alpha: .72),
          const Color(0xFF1A2234),
          const Color(0xFF0D1426),
        ],
      ),
      border: Border.all(color: Colors.white.withValues(alpha: .15)),
    ),
    child: Stack(
      fit: StackFit.expand,
      children: [
        Positioned(
          right: -20,
          top: -30,
          child: Icon(
            icon,
            size: 115,
            color: Colors.white.withValues(alpha: .09),
          ),
        ),
        Align(
          alignment: Alignment.center,
          child: Icon(
            worker,
            size: 60,
            color: Colors.white.withValues(alpha: .85),
          ),
        ),
        Positioned(
          left: 10,
          bottom: 10,
          child: Text(
            title,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 9,
              fontWeight: FontWeight.w800,
              letterSpacing: .5,
            ),
          ),
        ),
      ],
    ),
  );
}

class _FeaturesBar extends StatelessWidget {
  const _FeaturesBar({required this.wide});
  final bool wide;
  static const _features = [
    (Icons.workspace_premium_outlined, 'Profesionales capacitados'),
    (Icons.verified_user_outlined, 'Calidad y seguridad'),
    (Icons.tune_rounded, 'Soluciones a la medida'),
    (Icons.support_agent_rounded, 'Atención personalizada'),
  ];
  @override
  Widget build(BuildContext context) => Container(
    color: _navy,
    padding: EdgeInsets.fromLTRB(wide ? 8.7 : 20, 4, wide ? 8.7 : 20, 22),
    child: Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 1360),
        child: Wrap(
          alignment: WrapAlignment.spaceBetween,
          runSpacing: 14,
          children: _features
              .map(
                (item) => SizedBox(
                  width: wide ? 245 : 165,
                  child: Row(
                    children: [
                      Icon(item.$1, size: 25, color: _violet),
                      const SizedBox(width: 9),
                      Expanded(
                        child: Text(
                          item.$2,
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              )
              .toList(),
        ),
      ),
    ),
  );
}

class _ServicesSection extends StatelessWidget {
  const _ServicesSection({
    required this.anchorKey,
    required this.wide,
    required this.onSelect,
  });
  final GlobalKey anchorKey;
  final bool wide;
  final ValueChanged<_ServiceInfo> onSelect;
  @override
  Widget build(BuildContext context) => Container(
    key: anchorKey,
    padding: EdgeInsets.fromLTRB(wide ? 8.7 : 20, 26, wide ? 8.7 : 20, 28),
    color: Colors.white,
    child: Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 1360),
        child: Column(
          children: [
            const _SectionHeading(
              title: 'NUESTROS SERVICIOS',
              subtitle: 'Soluciones especializadas de mantenimiento para diferentes sectores de la ingeniería.',
            ),
            const SizedBox(height: 22),
            LayoutBuilder(
              builder: (context, constraints) {
                final cols = constraints.maxWidth >= 1100
                    ? 5
                    : constraints.maxWidth >= 700
                    ? 3
                    : 1;
                final width = cols == 1
                    ? constraints.maxWidth
                    : (constraints.maxWidth - 16 * (cols - 1)) / cols;
                return Wrap(
                  spacing: 16,
                  runSpacing: 14,
                  children: _LandingScreenState._services
                      .map(
                        (service) => SizedBox(
                          width: width,
                          child: _ServiceCard(
                            service: service,
                            onTap: () => onSelect(service),
                          ),
                        ),
                      )
                      .toList(),
                );
              },
            ),
          ],
        ),
      ),
    ),
  );
}

class _ServiceInfo {
  const _ServiceInfo(
    this.title,
    this.description,
    this.icon,
    this.tile,
    this.accent,
  );
  final String title, description;
  final IconData icon;
  final Color tile, accent;
}

class _ServiceCard extends StatelessWidget {
  const _ServiceCard({required this.service, required this.onTap});
  final _ServiceInfo service;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(14),
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(9),
      border: Border.all(color: _line),
      boxShadow: const [
        BoxShadow(
          color: Color(0x080D1740),
          blurRadius: 12,
          offset: Offset(0, 5),
        ),
      ],
    ),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: service.tile,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Icon(service.icon, color: service.accent, size: 28),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                service.title,
                style: const TextStyle(
                  color: _ink,
                  fontWeight: FontWeight.w800,
                  fontSize: 14,
                  height: 1.2,
                ),
              ),
              const SizedBox(height: 9),
              Text(
                service.description,
                maxLines: 4,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  color: _muted,
                  fontSize: 11,
                  height: 1.45,
                ),
              ),
              const SizedBox(height: 8),
              InkWell(
                onTap: onTap,
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: const [
                    Text(
                      'Ver más',
                      style: TextStyle(
                        color: _purple,
                        fontSize: 11,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    SizedBox(width: 5),
                    Icon(Icons.arrow_forward_rounded, size: 14, color: _purple),
                  ],
                ),
              ),
            ],
          ),
        ),
      ],
    ),
  );
}

class _SectionHeading extends StatelessWidget {
  const _SectionHeading({required this.title, required this.subtitle});
  final String title, subtitle;
  @override
  Widget build(BuildContext context) => Column(
    children: [
      Text(
        title,
        textAlign: TextAlign.center,
        style: const TextStyle(
          color: _ink,
          fontSize: 20,
          fontWeight: FontWeight.w800,
          letterSpacing: .4,
        ),
      ),
      Container(
        width: 36,
        height: 2,
        margin: const EdgeInsets.only(top: 6, bottom: 8),
        color: _purple,
      ),
      Text(
        subtitle,
        textAlign: TextAlign.center,
        style: const TextStyle(color: _muted, fontSize: 12, height: 1.4),
      ),
    ],
  );
}

class _ProcessSection extends StatelessWidget {
  const _ProcessSection({required this.wide});
  final bool wide;
  static const _steps = [
    (Icons.person_outline_rounded, 'Regístrate', 'Crea tu cuenta en segundos.'),
    (
      Icons.assignment_outlined,
      'Elige el servicio',
      'Selecciona el tipo de mantenimiento que necesitas.',
    ),
    (
      Icons.calendar_month_outlined,
      'Selecciona fecha',
      'Elige el día y la hora que prefieras.',
    ),
    (
      Icons.check_circle_outline_rounded,
      'Confirmamos tu cita',
      'Recibirás la confirmación de tu servicio.',
    ),
    (
      Icons.engineering_outlined,
      'Ejecutamos el servicio',
      'Nuestro equipo trabaja con calidad y seguridad.',
    ),
    (
      Icons.verified_user_outlined,
      'Consulta tu solicitud',
      'Revisa el estado de tu servicio.',
    ),
  ];
  @override
  Widget build(BuildContext context) => Container(
    color: const Color(0xFFF6F6FB),
    padding: EdgeInsets.symmetric(horizontal: wide ? 8.7 : 20, vertical: 25),
    child: Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 1360),
        child: Column(
          children: [
            const _SectionHeading(
              title: '¿CÓMO FUNCIONA?',
              subtitle: 'Agenda y sigue tu servicio en unos sencillos pasos.',
            ),
            const SizedBox(height: 22),
            LayoutBuilder(
              builder: (context, constraints) {
                final cols = constraints.maxWidth >= 900
                    ? 6
                    : constraints.maxWidth >= 550
                    ? 3
                    : 2;
                final itemWidth =
                    (constraints.maxWidth - (cols - 1) * 8) / cols;
                return Wrap(
                  spacing: 8,
                  runSpacing: 18,
                  children: [
                    for (var i = 0; i < _steps.length; i++)
                      SizedBox(
                        width: itemWidth,
                        child: _StepCard(
                          number: i + 1,
                          icon: _steps[i].$1,
                          title: _steps[i].$2,
                          caption: _steps[i].$3,
                        ),
                      ),
                  ],
                );
              },
            ),
          ],
        ),
      ),
    ),
  );
}

class _StepCard extends StatelessWidget {
  const _StepCard({
    required this.number,
    required this.icon,
    required this.title,
    required this.caption,
  });
  final int number;
  final IconData icon;
  final String title, caption;
  @override
  Widget build(BuildContext context) => Column(
    children: [
      Stack(
        clipBehavior: Clip.none,
        children: [
          Container(
            width: 56,
            height: 56,
            decoration: BoxDecoration(
              color: Colors.white,
              shape: BoxShape.circle,
              border: Border.all(color: const Color(0xFFDADCEC), width: 1.5),
            ),
            child: Icon(icon, color: _purple, size: 28),
          ),
          Positioned(
            left: -7,
            bottom: -3,
            child: CircleAvatar(
              radius: 10,
              backgroundColor: _purple,
              child: Text(
                '$number',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 10,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
          ),
        ],
      ),
      const SizedBox(height: 11),
      Text(
        title,
        textAlign: TextAlign.center,
        style: const TextStyle(
          color: _ink,
          fontSize: 11,
          fontWeight: FontWeight.w800,
        ),
      ),
      const SizedBox(height: 4),
      Text(
        caption,
        textAlign: TextAlign.center,
        maxLines: 3,
        overflow: TextOverflow.ellipsis,
        style: const TextStyle(color: _muted, fontSize: 10, height: 1.4),
      ),
    ],
  );
}

class _WhySection extends StatelessWidget {
  const _WhySection({
    required this.anchorKey,
    required this.wide,
    required this.onBook,
  });
  final GlobalKey anchorKey;
  final bool wide;
  final VoidCallback onBook;
  static const _reasons = [
    'Profesionales capacitados para cada especialidad.',
    'Experiencia en diferentes sectores de la ingeniería.',
    'Soluciones de mantenimiento integral y a la medida.',
    'Compromiso con la seguridad y el cumplimiento.',
    'Calidad en cada etapa del servicio.',
    'Atención personalizada para tu empresa.',
  ];
  @override
  Widget build(BuildContext context) => Container(
    key: anchorKey,
    color: Colors.white,
    padding: EdgeInsets.fromLTRB(wide ? 8.7 : 20, 26, wide ? 8.7 : 20, 35),
    child: Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 1360),
        child: wide
            ? Row(
                children: [
                  Expanded(child: _whyCopy()),
                  const SizedBox(width: 40),
                  const Expanded(child: _WhyIllustration()),
                ],
              )
            : Column(
                children: [
                  _whyCopy(),
                  const SizedBox(height: 22),
                  const SizedBox(height: 180, child: _WhyIllustration()),
                ],
              ),
      ),
    ),
  );

  Widget _whyCopy() => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      const Text(
        '¿POR QUÉ ELEGIR INNOVART DIGITAL?',
        style: TextStyle(
          color: _ink,
          fontSize: 20,
          fontWeight: FontWeight.w800,
        ),
      ),
      Container(
        width: 38,
        height: 2,
        margin: const EdgeInsets.only(top: 6, bottom: 16),
        color: _purple,
      ),
      for (final reason in _reasons)
        Padding(
          padding: const EdgeInsets.only(bottom: 11),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Icon(
                Icons.check_circle_outline_rounded,
                color: _purple,
                size: 18,
              ),
              const SizedBox(width: 9),
              Expanded(
                child: Text(
                  reason,
                  style: const TextStyle(
                    color: _ink,
                    fontSize: 12,
                    height: 1.4,
                  ),
                ),
              ),
            ],
          ),
        ),
      const SizedBox(height: 5),
      FilledButton.icon(
        onPressed: onBook,
        icon: const Icon(Icons.event_available_outlined),
        label: const Text('Agenda tu servicio'),
        style: FilledButton.styleFrom(
          backgroundColor: _purple,
          foregroundColor: Colors.white,
        ),
      ),
    ],
  );
}

class _WhyIllustration extends StatelessWidget {
  const _WhyIllustration();
  @override
  Widget build(BuildContext context) => Container(
    width: double.infinity,
    decoration: BoxDecoration(
      color: const Color(0xFFF8F7FF),
      borderRadius: BorderRadius.circular(20),
      border: Border.all(color: const Color(0xFFEAE6FF)),
    ),
    child: Stack(
      alignment: Alignment.center,
      children: [
        const Icon(
          Icons.apartment_rounded,
          color: Color(0xFFB9ABFF),
          size: 150,
        ),
        Positioned(
          left: 20,
          top: 24,
          child: _FloatingBadge(
            icon: Icons.electrical_services_rounded,
            label: 'Eléctrico',
          ),
        ),
        Positioned(
          right: 20,
          top: 50,
          child: _FloatingBadge(
            icon: Icons.ac_unit_rounded,
            label: 'Refrigeración',
          ),
        ),
        Positioned(
          left: 55,
          bottom: 24,
          child: _FloatingBadge(
            icon: Icons.water_drop_outlined,
            label: 'Hidrosanitario',
          ),
        ),
        Positioned(
          right: 34,
          bottom: 25,
          child: _FloatingBadge(
            icon: Icons.construction_rounded,
            label: 'Obras',
          ),
        ),
      ],
    ),
  );
}

class _FloatingBadge extends StatelessWidget {
  const _FloatingBadge({required this.icon, required this.label});
  final IconData icon;
  final String label;
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(12),
      boxShadow: const [
        BoxShadow(
          color: Color(0x14050D29),
          blurRadius: 12,
          offset: Offset(0, 4),
        ),
      ],
    ),
    child: Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, color: _purple, size: 17),
        const SizedBox(width: 6),
        Text(
          label,
          style: const TextStyle(
            color: _ink,
            fontSize: 10,
            fontWeight: FontWeight.w700,
          ),
        ),
      ],
    ),
  );
}
