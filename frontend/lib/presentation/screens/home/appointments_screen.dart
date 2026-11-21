import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/utils/date_formatter.dart';
import '../../../data/models/service_model.dart';
import '../../../logic/auth_service.dart';
import '../../../logic/service_controller.dart';

class AppointmentsScreen extends StatelessWidget {
  const AppointmentsScreen({super.key});

  Future<void> _cancel(BuildContext context, ServiceModel appointment) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: const Text('Eliminar cita'),
        content: const Text('¿Quieres eliminar esta cita de tu agenda?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext, false),
            child: const Text('Volver'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(dialogContext, true),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );
    if (confirmed != true) return;
    try {
      await ServiceController.instance.remove(appointment.id);
    } catch (error) {
      if (context.mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text(error.toString())));
      }
    }
  }

  void _showDetails(BuildContext context, ServiceModel appointment) {
    showDialog<void>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: Text(appointment.name),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Fecha: ${DateFormatter.date(appointment.dateTime)}'),
            Text('Hora: ${DateFormatter.time(appointment.dateTime)}'),
            if ((appointment.address ?? '').isNotEmpty)
              Text('Dirección: ${appointment.address}'),
            if ((appointment.status ?? '').isNotEmpty)
              Text('Estado: ${appointment.status}')
            else
              const Text('Estado: No disponible en la API actual'),
            if ((appointment.description ?? '').isNotEmpty) ...[
              const SizedBox(height: 12),
              Text(appointment.description!),
            ],
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
  }

  @override
  Widget build(BuildContext context) {
    final controller = ServiceController.instance;
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mis Citas'),
        actions: [
          IconButton(
            tooltip: 'Actualizar citas',
            onPressed: () {
              final user = AuthService.instance.currentUser;
              if (user != null) controller.loadFor(user);
            },
            icon: const Icon(Icons.refresh_rounded),
          ),
        ],
      ),
      body: ListenableBuilder(
        listenable: controller,
        builder: (context, _) {
          if (controller.isLoading && controller.services.isEmpty) {
            return const Center(child: CircularProgressIndicator());
          }
          if (controller.error != null && controller.services.isEmpty) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(controller.error!, textAlign: TextAlign.center),
                    const SizedBox(height: 12),
                    FilledButton(
                      onPressed: () {
                        final user = AuthService.instance.currentUser;
                        if (user != null) controller.loadFor(user);
                      },
                      child: const Text('Reintentar'),
                    ),
                  ],
                ),
              ),
            );
          }
          return RefreshIndicator(
            onRefresh: () async {
              final user = AuthService.instance.currentUser;
              if (user != null) await controller.loadFor(user);
            },
            child: ListView(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.all(20),
              children: [
                Text(
                  'Tus solicitudes de servicio',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: 14),
                if (controller.services.isEmpty)
                  const _EmptyAppointments()
                else
                  for (final appointment in controller.services)
                    _AppointmentCard(
                      appointment: appointment,
                      onDetails: () => _showDetails(context, appointment),
                      onDelete: () => _cancel(context, appointment),
                    ),
              ],
            ),
          );
        },
      ),
    );
  }
}

class _AppointmentCard extends StatelessWidget {
  const _AppointmentCard({
    required this.appointment,
    required this.onDetails,
    required this.onDelete,
  });
  final ServiceModel appointment;
  final VoidCallback onDetails;
  final VoidCallback onDelete;

  @override
  Widget build(BuildContext context) => Container(
    margin: const EdgeInsets.only(bottom: 12),
    decoration: BoxDecoration(
      color: AppColors.card,
      borderRadius: BorderRadius.circular(19),
      border: Border.all(color: AppColors.line),
    ),
    child: Padding(
      padding: const EdgeInsets.all(15),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 43,
                height: 43,
                decoration: BoxDecoration(
                  color: AppColors.mint,
                  borderRadius: BorderRadius.circular(13),
                ),
                child: const Icon(
                  Icons.event_available_rounded,
                  color: AppColors.greenDark,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  appointment.name,
                  style: const TextStyle(fontWeight: FontWeight.w800),
                ),
              ),
              IconButton(
                onPressed: onDelete,
                tooltip: 'Eliminar cita',
                icon: const Icon(
                  Icons.delete_outline_rounded,
                  color: AppColors.muted,
                ),
              ),
            ],
          ),
          const SizedBox(height: 9),
          Text(
            '${DateFormatter.date(appointment.dateTime)} · ${DateFormatter.time(appointment.dateTime)}',
          ),
          if ((appointment.address ?? '').isNotEmpty) ...[
            const SizedBox(height: 5),
            Text(appointment.address!),
          ],
          const SizedBox(height: 8),
          Row(
            children: [
              const Icon(
                Icons.info_outline_rounded,
                size: 16,
                color: AppColors.muted,
              ),
              const SizedBox(width: 5),
              Text(
                appointment.status ?? 'Estado no disponible en la API',
                style: const TextStyle(color: AppColors.muted, fontSize: 12),
              ),
              const Spacer(),
              TextButton(
                onPressed: onDetails,
                child: const Text('Ver detalles'),
              ),
            ],
          ),
        ],
      ),
    ),
  );
}

class _EmptyAppointments extends StatelessWidget {
  const _EmptyAppointments();

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(22),
    decoration: BoxDecoration(
      color: AppColors.card,
      borderRadius: BorderRadius.circular(20),
      border: Border.all(color: AppColors.line),
    ),
    child: const Column(
      children: [
        Icon(Icons.event_busy_rounded, size: 38, color: AppColors.green),
        SizedBox(height: 10),
        Text(
          'Todavía no tienes citas agendadas',
          style: TextStyle(fontWeight: FontWeight.w700),
        ),
        SizedBox(height: 5),
        Text(
          'Cuando registres una solicitud, aparecerá aquí.',
          textAlign: TextAlign.center,
        ),
      ],
    ),
  );
}
