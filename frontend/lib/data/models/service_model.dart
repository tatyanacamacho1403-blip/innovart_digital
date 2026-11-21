class ServiceCatalogItem {
  const ServiceCatalogItem({
    required this.id,
    required this.name,
    this.description = '',
    this.price,
  });

  final int id;
  final String name;
  final String description;
  final num? price;

  factory ServiceCatalogItem.fromApi(Map<String, dynamic> json) {
    final id = json['id'] as int?;
    if (id == null) throw const FormatException('Servicio sin ID.');
    return ServiceCatalogItem(
      id: id,
      name: json['nombre']?.toString() ?? 'Servicio',
      description: json['descripcion']?.toString() ?? '',
      price: num.tryParse(json['precio']?.toString() ?? ''),
    );
  }
}

class ServiceModel {
  final String id;
  final int serviceId;
  final String name;
  final DateTime dateTime;
  final String? address;
  final String? description;
  final String? status;

  const ServiceModel({
    required this.id,
    required this.serviceId,
    required this.name,
    required this.dateTime,
    this.address,
    this.description,
    this.status,
  });
}
