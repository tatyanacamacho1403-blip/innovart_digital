import 'package:flutter/material.dart';

import '../../../core/constants/app_routes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/utils/date_formatter.dart';
import '../../../data/models/innovart_service.dart';
import '../../../data/models/service_model.dart';
import '../../../logic/auth_service.dart';
import '../../../logic/service_controller.dart';

class ServiceBookingScreen extends StatefulWidget {
  const ServiceBookingScreen({
    super.key,
    required this.service,
    required this.catalogItem,
    required this.onViewAppointments,
  });

  final InnovartService service;
  final ServiceCatalogItem catalogItem;
  final VoidCallback onViewAppointments;

  @override
  State<ServiceBookingScreen> createState() => _ServiceBookingScreenState();
}

class _ServiceBookingScreenState extends State<ServiceBookingScreen> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _address = TextEditingController(
    text: AuthService.instance.currentUser?.address ?? '',
  );
  final _description = TextEditingController();
  DateTime? _date;
  TimeOfDay? _time;
  String? _scheduleError;

  @override
  void dispose() {
    _address.dispose();
    _description.dispose();
    super.dispose();
  }

  Future<void> _pickDate() async {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final picked = await showDatePicker(
      context: context,
      initialDate: _date ?? today,
      firstDate: today,
      lastDate: DateTime(now.year + 2),
      helpText: 'Selecciona la fecha de tu servicio',
    );
    if (picked != null) setState(() => _date = picked);
  }

  Future<void> _pickTime() async {
    final picked = await showTimePicker(
      context: context,
      initialTime: _time ?? TimeOfDay.now(),
      helpText: 'Selecciona tu hora preferida',
    );
    if (picked != null) setState(() => _time = picked);
  }

  void _continue() {
    if (!_formKey.currentState!.validate()) return;
    if (_date == null || _time == null) {
      setState(
        () => _scheduleError = 'Selecciona una fecha y una hora preferida.',
      );
      return;
    }
    final dateTime = DateTime(
      _date!.year,
      _date!.month,
      _date!.day,
      _time!.hour,
      _time!.minute,
    );
    if (!dateTime.isAfter(DateTime.now())) {
      setState(() => _scheduleError = 'Selecciona una fecha y hora futuras.');
      return;
    }
    setState(() => _scheduleError = null);
    Navigator.push<void>(
      context,
      MaterialPageRoute(
        builder: (_) => _BookingSummaryScreen(
          service: widget.service,
          catalogItem: widget.catalogItem,
          address: _address.text.trim(),
          description: _description.text.trim(),
          dateTime: dateTime,
          onViewAppointments: widget.onViewAppointments,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Agendar un Servicio')),
    body: Form(
      key: _formKey,
      child: ListView(
        padding: const EdgeInsets.fromLTRB(20, 10, 20, 28),
        children: [
          const _StepIndicator(current: 1),
          const SizedBox(height: 18),
          _SelectedServiceCard(service: widget.service),
          const SizedBox(height: 20),
          Text(
            'Datos del servicio',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          TextFormField(
            controller: _address,
            textCapitalization: TextCapitalization.sentences,
            decoration: const InputDecoration(
              labelText: 'Dirección del servicio',
              prefixIcon: Icon(Icons.location_on_outlined),
            ),
            validator: (value) => value == null || value.trim().isEmpty
                ? 'Escribe la dirección donde se realizará el servicio'
                : null,
          ),
          const SizedBox(height: 12),
          TextFormField(
            controller: _description,
            minLines: 3,
            maxLines: 5,
            textCapitalization: TextCapitalization.sentences,
            decoration: const InputDecoration(
              labelText: 'Describe el mantenimiento que necesitas',
              alignLabelWithHint: true,
              prefixIcon: Icon(Icons.description_outlined),
            ),
            validator: (value) => value == null || value.trim().isEmpty
                ? 'Describe brevemente el trabajo que necesitas'
                : null,
          ),
          const SizedBox(height: 20),
          Text('Fecha y hora', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 12),
          OutlinedButton.icon(
            onPressed: _pickDate,
            icon: const Icon(Icons.calendar_month_rounded),
            label: Text(
              _date == null ? 'Elegir fecha' : DateFormatter.date(_date!),
            ),
          ),
          const SizedBox(height: 8),
          OutlinedButton.icon(
            onPressed: _pickTime,
            icon: const Icon(Icons.schedule_rounded),
            label: Text(
              _time == null ? 'Elegir hora preferida' : _time!.format(context),
            ),
          ),
          if (_scheduleError != null) ...[
            const SizedBox(height: 8),
            Text(
              _scheduleError!,
              style: TextStyle(color: Theme.of(context).colorScheme.error),
            ),
          ],
          const SizedBox(height: 14),
          const _ApiLimitNotice(),
          const SizedBox(height: 18),
          FilledButton(onPressed: _continue, child: const Text('Continuar')),
        ],
      ),
    ),
  );
}

class _BookingSummaryScreen extends StatefulWidget {
  const _BookingSummaryScreen({
    required this.service,
    required this.catalogItem,
    required this.address,
    required this.description,
    required this.dateTime,
    required this.onViewAppointments,
  });

  final InnovartService service;
  final ServiceCatalogItem catalogItem;
  final String address;
  final String description;
  final DateTime dateTime;
  final VoidCallback onViewAppointments;

  @override
  State<_BookingSummaryScreen> createState() => _BookingSummaryScreenState();
}

class _BookingSummaryScreenState extends State<_BookingSummaryScreen> {
  bool _submitting = false;
  String? _error;

  Future<void> _confirm() async {
    if (_submitting) return;
    final user = AuthService.instance.currentUser;
    if (user == null) {
      await Navigator.pushNamed(
        context,
        AppRoutes.login,
        arguments: 'resume_booking',
      );
      return;
    }
    setState(() {
      _submitting = true;
      _error = null;
    });
    try {
      await ServiceController.instance.add(
        widget.catalogItem,
        widget.dateTime,
        user,
      );
      if (!mounted) return;
      await Navigator.push<void>(
        context,
        MaterialPageRoute(
          builder: (_) => _BookingSuccessScreen(
            service: widget.service,
            address: widget.address,
            description: widget.description,
            dateTime: widget.dateTime,
            onViewAppointments: widget.onViewAppointments,
          ),
        ),
      );
    } catch (error) {
      if (mounted) setState(() => _error = error.toString());
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Resumen de tu cita')),
    body: ListView(
      padding: const EdgeInsets.fromLTRB(20, 10, 20, 28),
      children: [
        const _StepIndicator(current: 2),
        const SizedBox(height: 18),
        _SummaryCard(
          title: 'Servicio',
          value: widget.service.name,
          icon: widget.service.icon,
        ),
        _SummaryCard(
          title: 'Dirección',
          value: widget.address,
          icon: Icons.location_on_outlined,
        ),
        _SummaryCard(
          title: 'Descripción',
          value: widget.description,
          icon: Icons.description_outlined,
        ),
        _SummaryCard(
          title: 'Fecha',
          value: DateFormatter.date(widget.dateTime),
          icon: Icons.calendar_month_rounded,
        ),
        _SummaryCard(
          title: 'Hora',
          value: TimeOfDay.fromDateTime(widget.dateTime).format(context),
          icon: Icons.schedule_rounded,
        ),
        const SizedBox(height: 8),
        const _ApiLimitNotice(),
        const SizedBox(height: 10),
        const Text('Revisa la información antes de confirmar la cita.'),
        if (_error != null) ...[
          const SizedBox(height: 12),
          Text(
            _error!,
            style: TextStyle(color: Theme.of(context).colorScheme.error),
          ),
        ],
        const SizedBox(height: 18),
        OutlinedButton(
          onPressed: _submitting ? null : () => Navigator.pop(context),
          child: const Text('Volver'),
        ),
        const SizedBox(height: 8),
        FilledButton(
          onPressed: _submitting ? null : _confirm,
          child: _submitting
              ? const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Text('Confirmar Cita'),
        ),
      ],
    ),
  );
}

class _BookingSuccessScreen extends StatelessWidget {
  const _BookingSuccessScreen({
    required this.service,
    required this.address,
    required this.description,
    required this.dateTime,
    required this.onViewAppointments,
  });

  final InnovartService service;
  final String address;
  final String description;
  final DateTime dateTime;
  final VoidCallback onViewAppointments;

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Confirmación')),
    body: ListView(
      padding: const EdgeInsets.fromLTRB(24, 30, 24, 30),
      children: [
        const _StepIndicator(current: 3),
        const SizedBox(height: 36),
        const Icon(
          Icons.check_circle_rounded,
          size: 82,
          color: AppColors.green,
        ),
        const SizedBox(height: 18),
        Text(
          '¡Cita agendada con éxito!',
          textAlign: TextAlign.center,
          style: Theme.of(context).textTheme.headlineSmall,
        ),
        const SizedBox(height: 8),
        const Text(
          'Tu solicitud ha sido registrada correctamente.',
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 24),
        _SummaryCard(
          title: 'Servicio',
          value: service.name,
          icon: service.icon,
        ),
        _SummaryCard(
          title: 'Fecha',
          value: DateFormatter.date(dateTime),
          icon: Icons.calendar_month_rounded,
        ),
        _SummaryCard(
          title: 'Hora',
          value: TimeOfDay.fromDateTime(dateTime).format(context),
          icon: Icons.schedule_rounded,
        ),
        _SummaryCard(
          title: 'Dirección ingresada',
          value: address,
          icon: Icons.location_on_outlined,
        ),
        _SummaryCard(
          title: 'Descripción ingresada',
          value: description,
          icon: Icons.description_outlined,
        ),
        const SizedBox(height: 8),
        const _ApiLimitNotice(),
        const SizedBox(height: 20),
        FilledButton(
          onPressed: () {
            Navigator.popUntil(
              context,
              (route) => route.settings.name == '/main',
            );
            onViewAppointments();
          },
          child: const Text('Ver mis citas'),
        ),
        const SizedBox(height: 8),
        OutlinedButton(
          onPressed: () => Navigator.popUntil(
            context,
            (route) => route.settings.name == '/main',
          ),
          child: const Text('Volver a Servicios'),
        ),
      ],
    ),
  );
}

class _StepIndicator extends StatelessWidget {
  const _StepIndicator({required this.current});
  final int current;

  @override
  Widget build(BuildContext context) => Row(
    children: [
      Expanded(
        child: Text(
          'Paso $current de 3',
          style: const TextStyle(fontWeight: FontWeight.w700),
        ),
      ),
      const SizedBox(width: 12),
      for (var step = 1; step <= 3; step++) ...[
        Container(
          width: 25,
          height: 25,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: step <= current ? AppColors.green : AppColors.line,
            shape: BoxShape.circle,
          ),
          child: Text(
            '$step',
            style: TextStyle(
              color: step <= current ? Colors.white : AppColors.muted,
              fontSize: 12,
            ),
          ),
        ),
        if (step < 3)
          Container(
            width: 20,
            height: 2,
            color: step < current ? AppColors.green : AppColors.line,
          ),
      ],
    ],
  );
}

class _SelectedServiceCard extends StatelessWidget {
  const _SelectedServiceCard({required this.service});
  final InnovartService service;

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(
      color: AppColors.mint,
      borderRadius: BorderRadius.circular(18),
    ),
    child: Row(
      children: [
        Icon(service.icon, color: service.accent, size: 26),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Servicio seleccionado',
                style: TextStyle(fontSize: 12, color: AppColors.muted),
              ),
              Text(
                service.name,
                style: const TextStyle(fontWeight: FontWeight.w800),
              ),
            ],
          ),
        ),
        const Icon(Icons.check_circle_rounded, color: AppColors.green),
      ],
    ),
  );
}

class _SummaryCard extends StatelessWidget {
  const _SummaryCard({
    required this.title,
    required this.value,
    required this.icon,
  });
  final String title;
  final String value;
  final IconData icon;

  @override
  Widget build(BuildContext context) => Container(
    margin: const EdgeInsets.only(bottom: 10),
    padding: const EdgeInsets.all(14),
    decoration: BoxDecoration(
      color: AppColors.card,
      borderRadius: BorderRadius.circular(16),
      border: Border.all(color: AppColors.line),
    ),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, color: AppColors.green),
        const SizedBox(width: 11),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: const TextStyle(color: AppColors.muted, fontSize: 12),
              ),
              const SizedBox(height: 3),
              Text(value),
            ],
          ),
        ),
      ],
    ),
  );
}

class _ApiLimitNotice extends StatelessWidget {
  const _ApiLimitNotice();

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(13),
    decoration: BoxDecoration(
      color: const Color(0xFFFFF2D8),
      borderRadius: BorderRadius.circular(14),
    ),
    child: const Text(
      'La API disponible registra servicio, fecha y hora. No guarda la dirección ni la descripción y no consulta disponibilidad; esos datos se muestran en esta solicitud, pero no quedan almacenados por el servidor.',
      style: TextStyle(fontSize: 12),
    ),
  );
}
