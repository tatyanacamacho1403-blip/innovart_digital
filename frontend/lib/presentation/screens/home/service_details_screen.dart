import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../data/models/innovart_service.dart';
import '../../../data/models/service_model.dart';
import '../../../logic/service_controller.dart';
import 'private_area_shell.dart';
import 'service_booking_screen.dart';

class ServiceDetailsScreen extends StatelessWidget {
  const ServiceDetailsScreen({
    super.key,
    required this.service,
    required this.catalogItem,
    required this.onViewAppointments,
    required this.onSelectSection,
  });

  final InnovartService service;
  final ServiceCatalogItem? catalogItem;
  final VoidCallback onViewAppointments;
  final ValueChanged<int> onSelectSection;

  void _book(BuildContext context) {
    final serviceKey = normalizeServiceName(service.name);
    final item =
        catalogItem ??
        ServiceController.instance.catalog
            .where(
              (candidate) => normalizeServiceName(candidate.name) == serviceKey,
            )
            .firstOrNull;
    if (item == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            '“${service.name}” no aparece en el catálogo del servidor. Actualiza el catálogo para poder agendarlo.',
          ),
        ),
      );
      return;
    }
    Navigator.push<void>(
      context,
      MaterialPageRoute(
        builder: (_) => ServiceBookingScreen(
          service: service,
          catalogItem: item,
          onViewAppointments: onViewAppointments,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) => PrivateAreaShell(
    currentIndex: 0,
    onSelect: (index) {
      Navigator.pop(context);
      onSelectSection(index);
    },
    onBack: () => Navigator.pop(context),
    child: ColoredBox(
      color: AppColors.navy,
      child: ListView(
        padding: const EdgeInsets.fromLTRB(28, 26, 28, 36),
        children: [
          Text(
            'DETALLE DEL SERVICIO',
            style: TextStyle(
              color: AppColors.violet.withValues(alpha: .95),
              fontWeight: FontWeight.w800,
              letterSpacing: 1.7,
              fontSize: 11,
            ),
          ),
          const SizedBox(height: 9),
          Text(
            service.name,
            style: Theme.of(context).textTheme.headlineLarge
                ?.copyWith(color: AppColors.white),
          ),
          const SizedBox(height: 22),
          Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 1120),
              child: Container(
                padding: const EdgeInsets.all(28),
                decoration: BoxDecoration(
                  color: AppColors.white,
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: const [
                    BoxShadow(
                      color: Color(0x30000000),
                      blurRadius: 28,
                      offset: Offset(0, 12),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 76,
                          height: 76,
                          decoration: BoxDecoration(
                            color: AppColors.mint,
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Icon(
                            service.icon,
                            color: AppColors.purple,
                            size: 42,
                          ),
                        ),
                        const SizedBox(width: 18),
                        Expanded(
                          child: Text(
                            service.name,
                            style: Theme.of(context).textTheme.headlineMedium
                                ?.copyWith(color: AppColors.navy),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 28),
                    Text(
                      'Descripción',
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        color: AppColors.navy,
                        fontFamily: 'Roboto',
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      service.description,
                      style: const TextStyle(
                        color: AppColors.secondaryText,
                        height: 1.55,
                      ),
                    ),
                    const SizedBox(height: 22),
                    Text(
                      'Trabajos que comprende',
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        color: AppColors.navy,
                        fontFamily: 'Roboto',
                      ),
                    ),
                    const SizedBox(height: 10),
                    for (final activity in service.activities)
                      _BulletRow(icon: service.icon, text: activity),
                    const SizedBox(height: 15),
                    Text(
                      'Beneficios para tu empresa',
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        color: AppColors.navy,
                        fontFamily: 'Roboto',
                      ),
                    ),
                    const SizedBox(height: 10),
                    for (final benefit in service.benefits)
                      _BulletRow(
                        icon: Icons.check_circle_outline_rounded,
                        text: benefit,
                      ),
                    const SizedBox(height: 22),
                    SizedBox(
                      height: 52,
                      child: DecoratedBox(
                        decoration: BoxDecoration(
                          gradient: const LinearGradient(
                            colors: [AppColors.purple, AppColors.violet],
                          ),
                          borderRadius: BorderRadius.circular(14),
                          boxShadow: const [
                            BoxShadow(
                              color: Color(0x286C19D2),
                              blurRadius: 14,
                              offset: Offset(0, 5),
                            ),
                          ],
                        ),
                        child: TextButton.icon(
                          onPressed: () => _book(context),
                          style: TextButton.styleFrom(
                            foregroundColor: AppColors.white,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(14),
                            ),
                          ),
                          icon: const Icon(Icons.calendar_month_rounded),
                          label: const Text('Agendar Servicio'),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    ),
  );
}

class _BulletRow extends StatelessWidget {
  const _BulletRow({required this.icon, required this.text});
  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 9),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, size: 19, color: AppColors.purple),
        const SizedBox(width: 10),
        Expanded(
          child: Text(text, style: const TextStyle(color: AppColors.navy)),
        ),
      ],
    ),
  );
}
