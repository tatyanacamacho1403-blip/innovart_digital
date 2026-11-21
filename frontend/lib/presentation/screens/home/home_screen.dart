import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/utils/date_formatter.dart';
import '../../../logic/auth_service.dart';
import '../../../logic/service_controller.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, required this.onBrowseServices});

  final VoidCallback onBrowseServices;

  @override
  Widget build(BuildContext context) {
    final user = AuthService.instance.currentUser;
    final services = ServiceController.instance;
    final nameParts = user?.name.trim().split(' ') ?? const <String>[];
    final firstName = nameParts.isEmpty || nameParts.first.isEmpty
        ? ''
        : nameParts.first;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Buen Día'),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 18),
            child: CircleAvatar(
              radius: 19,
              backgroundColor: AppColors.mint,
              child: Text(
                firstName.isEmpty ? 'B' : firstName[0].toUpperCase(),
                style: const TextStyle(
                  color: AppColors.greenDark,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ),
          ),
        ],
      ),
      body: ListenableBuilder(
        listenable: services,
        builder: (context, _) => RefreshIndicator(
          onRefresh: () async {
            final current = AuthService.instance.currentUser;
            if (current != null) await services.loadFor(current);
          },
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.fromLTRB(20, 8, 20, 30),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  firstName.isEmpty ? 'Qué gusto verte' : 'Hola, $firstName',
                  style: Theme.of(context).textTheme.headlineMedium,
                ),
                const SizedBox(height: 4),
                const Text('¿Qué hacemos más fácil para ti hoy?'),
                const SizedBox(height: 22),
                _WelcomeCard(onBrowseServices: onBrowseServices),
                const SizedBox(height: 24),
                Row(
                  children: [
                    Expanded(
                      child: _MetricCard(
                        icon: Icons.event_available_rounded,
                        label: 'Citas agendadas',
                        value: '${services.appointmentCount}',
                        tint: AppColors.mint,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _MetricCard(
                        icon: Icons.auto_awesome_rounded,
                        label: 'Servicios',
                        value: '${services.catalogCount}',
                        tint: AppColors.rose,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 28),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Tus próximas citas',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    TextButton(
                      onPressed: onBrowseServices,
                      child: const Text('Ver todas'),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                if (services.isLoading && services.services.isEmpty)
                  const Padding(
                    padding: EdgeInsets.all(28),
                    child: Center(child: CircularProgressIndicator()),
                  )
                else if (services.services.isEmpty)
                  _EmptyAppointments(onBrowseServices: onBrowseServices)
                else
                  ...services.services
                      .take(3)
                      .map(
                        (service) => Padding(
                          padding: const EdgeInsets.only(bottom: 10),
                          child: Container(
                            decoration: BoxDecoration(
                              color: AppColors.card,
                              borderRadius: BorderRadius.circular(20),
                              border: Border.all(color: AppColors.line),
                            ),
                            child: ListTile(
                              contentPadding: const EdgeInsets.symmetric(
                                horizontal: 16,
                                vertical: 7,
                              ),
                              leading: Container(
                                width: 46,
                                height: 46,
                                decoration: BoxDecoration(
                                  color: AppColors.mint,
                                  borderRadius: BorderRadius.circular(15),
                                ),
                                child: const Icon(
                                  Icons.spa_rounded,
                                  color: AppColors.green,
                                ),
                              ),
                              title: Text(
                                service.name,
                                style: const TextStyle(
                                  fontWeight: FontWeight.w700,
                                ),
                              ),
                              subtitle: Text(
                                '${DateFormatter.date(service.dateTime)} · ${DateFormatter.time(service.dateTime)}',
                              ),
                              trailing: const Icon(
                                Icons.arrow_forward_ios_rounded,
                                size: 15,
                                color: AppColors.muted,
                              ),
                            ),
                          ),
                        ),
                      ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _WelcomeCard extends StatelessWidget {
  const _WelcomeCard({required this.onBrowseServices});
  final VoidCallback onBrowseServices;

  @override
  Widget build(BuildContext context) {
    return Container(
      clipBehavior: Clip.antiAlias,
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppColors.greenDark, AppColors.green],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(26),
      ),
      child: Stack(
        children: [
          Positioned(
            right: -42,
            top: -46,
            child: Container(
              width: 170,
              height: 170,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(
                  color: Colors.white.withValues(alpha: .1),
                  width: 28,
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(22),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 11,
                    vertical: 7,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: .13),
                    borderRadius: BorderRadius.circular(30),
                  ),
                  child: const Text(
                    'UN RESPIRO PARA TU AGENDA',
                    style: TextStyle(
                      color: Colors.white,
                      letterSpacing: 1.15,
                      fontSize: 10,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ),
                const SizedBox(height: 18),
                Text(
                  'Un buen día\nempieza con tiempo.',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    color: Colors.white,
                    fontSize: 26,
                    height: 1.18,
                  ),
                ),
                const SizedBox(height: 17),
                OutlinedButton.icon(
                  onPressed: onBrowseServices,
                  icon: const Icon(Icons.add_rounded, size: 19),
                  label: const Text('Agendar un servicio'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Colors.white,
                    side: BorderSide(
                      color: Colors.white.withValues(alpha: .55),
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(14),
                    ),
                    padding: const EdgeInsets.symmetric(
                      horizontal: 15,
                      vertical: 12,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _MetricCard extends StatelessWidget {
  const _MetricCard({
    required this.icon,
    required this.label,
    required this.value,
    required this.tint,
  });

  final IconData icon;
  final String label;
  final String value;
  final Color tint;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(21),
        border: Border.all(color: AppColors.line),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 37,
            height: 37,
            decoration: BoxDecoration(
              color: tint,
              borderRadius: BorderRadius.circular(13),
            ),
            child: Icon(icon, color: AppColors.greenDark, size: 19),
          ),
          const SizedBox(height: 13),
          Text(
            value,
            style: Theme.of(context).textTheme.titleLarge
                ?.copyWith(fontSize: 25),
          ),
          const SizedBox(height: 3),
          Text(label, style: Theme.of(context).textTheme.bodyMedium),
        ],
      ),
    );
  }
}

class _EmptyAppointments extends StatelessWidget {
  const _EmptyAppointments({required this.onBrowseServices});
  final VoidCallback onBrowseServices;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(22),
      decoration: BoxDecoration(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(21),
        border: Border.all(color: AppColors.line),
      ),
      child: Column(
        children: [
          const Icon(
            Icons.calendar_month_rounded,
            size: 32,
            color: AppColors.green,
          ),
          const SizedBox(height: 9),
          Text(
            'Tu agenda está despejada',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 4),
          const Text(
            'Elige un servicio y reserva un momento para ti.',
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 10),
          TextButton(
            onPressed: onBrowseServices,
            child: const Text('Explorar servicios'),
          ),
        ],
      ),
    );
  }
}
