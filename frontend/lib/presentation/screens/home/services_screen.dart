import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../data/models/innovart_service.dart';
import '../../../data/models/service_model.dart';
import '../../../logic/auth_service.dart';
import '../../../logic/service_controller.dart';
import 'service_details_screen.dart';

class ServicesScreen extends StatelessWidget {
  const ServicesScreen({
    super.key,
    required this.onViewAppointments,
    required this.onSelectSection,
  });

  final VoidCallback onViewAppointments;
  final ValueChanged<int> onSelectSection;

  @override
  Widget build(BuildContext context) {
    final controller = ServiceController.instance;
    return ColoredBox(
      color: AppColors.navy,
      child: RefreshIndicator(
        onRefresh: () async {
          final user = AuthService.instance.currentUser;
          if (user != null) {
            await controller.loadFor(user);
          } else {
            await controller.loadCatalog();
          }
        },
        child: ListView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.fromLTRB(28, 26, 28, 38),
          children: [
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'ÁREA DE SERVICIOS',
                        style: TextStyle(
                          color: AppColors.violet.withValues(alpha: .95),
                          fontWeight: FontWeight.w800,
                          letterSpacing: 1.7,
                          fontSize: 11,
                        ),
                      ),
                      const SizedBox(height: 9),
                      Text(
                        'Nuestros Servicios',
                        style: Theme.of(context).textTheme.headlineLarge
                            ?.copyWith(color: AppColors.white),
                      ),
                      const SizedBox(height: 7),
                      const Text(
                        'Soluciones de mantenimiento para diferentes sectores de la ingeniería.',
                        style: TextStyle(
                          color: AppColors.secondaryText,
                          fontSize: 15,
                        ),
                      ),
                    ],
                  ),
                ),
                IconButton.filledTonal(
                  tooltip: 'Actualizar catálogo',
                  onPressed: () {
                    final user = AuthService.instance.currentUser;
                    if (user != null) {
                      controller.loadFor(user);
                    } else {
                      controller.loadCatalog();
                    }
                  },
                  icon: const Icon(Icons.refresh_rounded),
                ),
              ],
            ),
            const SizedBox(height: 26),
            LayoutBuilder(
              builder: (context, constraints) {
                final columns = constraints.maxWidth >= 1000
                    ? 3
                    : constraints.maxWidth >= 620
                    ? 2
                    : 1;
                final cardWidth =
                    (constraints.maxWidth - 14 * (columns - 1)) / columns;
                return Wrap(
                  spacing: 14,
                  runSpacing: 14,
                  children: [
                    for (final service in innovartServices)
                      SizedBox(
                        width: cardWidth,
                        child: _ServiceCard(
                          service: service,
                          onTap: () => Navigator.push<void>(
                            context,
                            MaterialPageRoute(
                              builder: (_) => ServiceDetailsScreen(
                                service: service,
                                catalogItem: _catalogMatch(service),
                                onViewAppointments: onViewAppointments,
                                onSelectSection: onSelectSection,
                              ),
                            ),
                          ),
                        ),
                      ),
                  ],
                );
              },
            ),
            const SizedBox(height: 24),
            ListenableBuilder(
              listenable: controller,
              builder: (context, _) => controller.error == null
                  ? const SizedBox.shrink()
                  : _CatalogError(
                      message: controller.error!,
                      onRetry: () {
                        final user = AuthService.instance.currentUser;
                        if (user != null) {
                          controller.loadFor(user);
                        } else {
                          controller.loadCatalog();
                        }
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }

  ServiceCatalogItem? _catalogMatch(InnovartService service) {
    final key = normalizeServiceName(service.name);
    for (final item in ServiceController.instance.catalog) {
      if (normalizeServiceName(item.name) == key) return item;
    }
    return null;
  }
}

class _ServiceCard extends StatelessWidget {
  const _ServiceCard({required this.service, required this.onTap});
  final InnovartService service;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Container(
    decoration: BoxDecoration(
      color: AppColors.white,
      borderRadius: BorderRadius.circular(20),
      border: Border.all(color: AppColors.line),
      boxShadow: const [
        BoxShadow(
          color: Color(0x100D1740),
          blurRadius: 15,
          offset: Offset(0, 5),
        ),
      ],
    ),
    child: Padding(
      padding: const EdgeInsets.all(17),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              color: AppColors.mint,
              borderRadius: BorderRadius.circular(14),
            ),
            child: Icon(service.icon, color: AppColors.purple, size: 27),
          ),
          const SizedBox(height: 13),
          Text(
            service.name,
            style: Theme.of(context).textTheme.titleMedium
                ?.copyWith(fontWeight: FontWeight.w800, color: AppColors.navy),
          ),
          const SizedBox(height: 7),
          Text(service.summary, style: Theme.of(context).textTheme.bodyMedium),
          const SizedBox(height: 14),
          SizedBox(
            width: double.infinity,
            height: 46,
            child: DecoratedBox(
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [AppColors.purple, AppColors.violet],
                ),
                borderRadius: BorderRadius.circular(13),
                boxShadow: const [
                  BoxShadow(
                    color: Color(0x286C19D2),
                    blurRadius: 14,
                    offset: Offset(0, 5),
                  ),
                ],
              ),
              child: TextButton.icon(
                onPressed: onTap,
                style: TextButton.styleFrom(
                  foregroundColor: AppColors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(13),
                  ),
                ),
                icon: const Icon(Icons.arrow_forward_rounded, size: 18),
                label: const Text('Más de este servicio'),
              ),
            ),
          ),
        ],
      ),
    ),
  );
}

class _CatalogError extends StatelessWidget {
  const _CatalogError({required this.message, required this.onRetry});
  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
      color: AppColors.navyLight,
      borderRadius: BorderRadius.circular(16),
      border: Border.all(color: const Color(0xFFFF9AAC).withValues(alpha: .5)),
    ),
    child: Row(
      children: [
        const Icon(Icons.cloud_off_rounded, color: Color(0xFFFF9AAC)),
        const SizedBox(width: 12),
        Expanded(
          child: Text(message, style: const TextStyle(color: AppColors.white)),
        ),
        TextButton(
          onPressed: onRetry,
          style: TextButton.styleFrom(foregroundColor: AppColors.violet),
          child: const Text('Reintentar'),
        ),
      ],
    ),
  );
}
