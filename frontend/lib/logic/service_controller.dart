import 'package:flutter/foundation.dart';

import '../data/api/api_client.dart';
import '../data/models/service_model.dart';
import '../data/models/user_model.dart';

class ServiceController extends ChangeNotifier {
  ServiceController._();
  static final ServiceController instance = ServiceController._();

  final List<ServiceModel> _services = [];
  List<ServiceCatalogItem> _catalog = [];
  bool isLoading = false;
  String? error;

  List<ServiceModel> get services => List.unmodifiable(_services);
  List<ServiceCatalogItem> get catalog => List.unmodifiable(_catalog);
  int get appointmentCount => _services.length;
  int get catalogCount => _catalog.length;

  /// Carga únicamente el catálogo público para la entrada de pruebas web.
  Future<void> loadCatalog() async {
    isLoading = true;
    error = null;
    notifyListeners();
    try {
      final catalogData = await ApiClient.instance.get('/api/servicios/');
      if (catalogData is! List) {
        throw const ApiException('El backend devolvió una lista inválida.');
      }
      _catalog = catalogData
          .whereType<Map>()
          .map(
            (item) =>
                ServiceCatalogItem.fromApi(Map<String, dynamic>.from(item)),
          )
          .toList();
    } catch (exception) {
      error = exception is ApiException
          ? exception.message
          : 'No se pudo cargar el catálogo del backend.';
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadFor(UserModel user) async {
    isLoading = true;
    error = null;
    notifyListeners();
    try {
      final results = await Future.wait([
        ApiClient.instance.get('/api/servicios/'),
        ApiClient.instance.get('/agendas/'),
      ]);
      final catalogData = results[0];
      final agendaData = results[1];
      if (catalogData is! List || agendaData is! List) {
        throw const ApiException('El backend devolvió una lista inválida.');
      }
      _catalog = catalogData
          .whereType<Map>()
          .map(
            (item) =>
                ServiceCatalogItem.fromApi(Map<String, dynamic>.from(item)),
          )
          .toList();
      _services
        ..clear()
        ..addAll(
          agendaData.whereType<Map>().map((item) {
            final row = Map<String, dynamic>.from(item);
            final ownerId = int.tryParse(
              (row['usuario_id'] ?? row['usu_id'])?.toString() ?? '',
            );
            if (ownerId != user.id) return null;
            final serviceId = int.tryParse(
              (row['servicio_id'] ?? row['ser_id'])?.toString() ?? '',
            );
            final appointmentId = row['id']?.toString();
            if (serviceId == null || appointmentId == null) return null;
            final catalogItem = _catalog.where((item) => item.id == serviceId);
            final name = catalogItem.isEmpty
                ? 'Servicio'
                : catalogItem.first.name;
            final date = _parseDateTime(row['fecha'], row['hora']);
            if (date == null) return null;
            return ServiceModel(
              id: appointmentId,
              serviceId: serviceId,
              name: name,
              dateTime: date,
              address: row['direccion']?.toString(),
              description: row['descripcion']?.toString(),
              status: row['estado']?.toString(),
            );
          }).whereType<ServiceModel>(),
        );
      _services.sort((a, b) => a.dateTime.compareTo(b.dateTime));
    } catch (exception) {
      error = exception is ApiException
          ? exception.message
          : 'No se pudieron cargar los datos del backend.';
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> add(
    ServiceCatalogItem service,
    DateTime dateTime, {
    required String address,
    required String description,
  }) async {
    final result = await ApiClient.instance.post('/agendas/', {
      'fecha': _dateString(dateTime),
      'hora': _timeString(dateTime),
      'servicio_id': service.id,
      'direccion': address,
      'descripcion': description,
    });
    if (result is! Map || result['id'] == null) {
      throw const ApiException('El backend no confirmó la cita creada.');
    }
    _services.add(
      ServiceModel(
        id: result['id'].toString(),
        serviceId: service.id,
        name: service.name,
        dateTime: dateTime,
        address: address,
        description: description,
      ),
    );
    _services.sort((a, b) => a.dateTime.compareTo(b.dateTime));
    notifyListeners();
  }

  Future<void> remove(String id) async {
    await ApiClient.instance.delete('/agendas/$id');
    _services.removeWhere((service) => service.id == id);
    notifyListeners();
  }

  void clear() {
    _services.clear();
    _catalog = [];
    error = null;
    isLoading = false;
    notifyListeners();
  }

  static String _dateString(DateTime value) =>
      '${value.year.toString().padLeft(4, '0')}-${value.month.toString().padLeft(2, '0')}-${value.day.toString().padLeft(2, '0')}';

  static String _timeString(DateTime value) =>
      '${value.hour.toString().padLeft(2, '0')}:${value.minute.toString().padLeft(2, '0')}:00';

  static DateTime? _parseDateTime(dynamic date, dynamic time) {
    if (date == null || time == null) return null;
    final dateText = date.toString();
    final timeText = time.toString();
    final dateMatch = RegExp(r'(\d{4})-(\d{2})-(\d{2})').firstMatch(dateText);
    final timeMatch = RegExp(r'(\d{2}):(\d{2})').firstMatch(timeText);
    if (dateMatch == null || timeMatch == null) return null;
    return DateTime(
      int.parse(dateMatch[1]!),
      int.parse(dateMatch[2]!),
      int.parse(dateMatch[3]!),
      int.parse(timeMatch[1]!),
      int.parse(timeMatch[2]!),
    );
  }
}
