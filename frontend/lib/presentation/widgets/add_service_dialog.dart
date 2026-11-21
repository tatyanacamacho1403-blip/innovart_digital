import 'package:flutter/material.dart';

import '../../core/icons/app_icons.dart';
import '../../core/utils/date_formatter.dart';
import '../../data/models/service_model.dart';

/// Ventana para agendar un servicio: nombre + fecha + hora.
/// Al guardar devuelve (nombre, fecha y hora); si cancelas devuelve null.
class AddServiceDialog extends StatefulWidget {
  const AddServiceDialog({
    super.key,
    required this.services,
    this.initialServiceId,
  });

  final List<ServiceCatalogItem> services;
  final int? initialServiceId;

  @override
  State<AddServiceDialog> createState() => _AddServiceDialogState();
}

class _AddServiceDialogState extends State<AddServiceDialog> {
  int? _serviceId;
  DateTime? _date;
  TimeOfDay? _time;
  String? _error;

  @override
  void initState() {
    super.initState();
    _serviceId = widget.initialServiceId;
  }

  @override
  void dispose() {
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
    );
    if (picked != null) setState(() => _date = picked);
  }

  Future<void> _pickTime() async {
    final picked = await showTimePicker(
      context: context,
      initialTime: _time ?? TimeOfDay.now(),
    );
    if (picked != null) setState(() => _time = picked);
  }

  void _save() {
    if (_serviceId == null) {
      setState(() => _error = 'Selecciona un servicio del catálogo');
      return;
    }
    if (_date == null || _time == null) {
      setState(() => _error = 'Elige la fecha y la hora');
      return;
    }
    final dateTime = DateTime(
      _date!.year,
      _date!.month,
      _date!.day,
      _time!.hour,
      _time!.minute,
    );
    final service = widget.services.firstWhere((item) => item.id == _serviceId);
    Navigator.pop(context, (service: service, dateTime: dateTime));
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Agendar servicio'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          if (widget.services.isEmpty)
            const Text('No hay servicios disponibles en el catálogo.'),
          DropdownButtonFormField<int>(
            initialValue: _serviceId,
            isExpanded: true,
            decoration: const InputDecoration(labelText: 'Servicio'),
            items: widget.services
                .map(
                  (service) => DropdownMenuItem(
                    value: service.id,
                    child: Text(service.name, overflow: TextOverflow.ellipsis),
                  ),
                )
                .toList(),
            onChanged: (value) => setState(() => _serviceId = value),
          ),
          const SizedBox(height: 12),
          OutlinedButton.icon(
            onPressed: _pickDate,
            icon: const Icon(AppIcons.calendar),
            label: Text(
              _date == null ? 'Elegir fecha' : DateFormatter.date(_date!),
            ),
          ),
          const SizedBox(height: 8),
          OutlinedButton.icon(
            onPressed: _pickTime,
            icon: const Icon(AppIcons.clock),
            label: Text(_time == null ? 'Elegir hora' : _time!.format(context)),
          ),
          if (_error != null) ...[
            const SizedBox(height: 12),
            Text(
              _error!,
              style: TextStyle(color: Theme.of(context).colorScheme.error),
            ),
          ],
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cancelar'),
        ),
        FilledButton(onPressed: _save, child: const Text('Agendar')),
      ],
    );
  }
}
