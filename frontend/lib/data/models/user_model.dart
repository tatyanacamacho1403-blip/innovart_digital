class UserModel {
  final int id;
  final int personId;
  final String name;
  final String email;
  final String documentType;
  final String documentNumber;
  final String phone;
  final String address;

  const UserModel({
    required this.id,
    required this.personId,
    required this.name,
    required this.email,
    this.documentType = '',
    this.documentNumber = '',
    this.phone = '',
    this.address = '',
  });

  factory UserModel.fromApi(Map<String, dynamic> json, {String? name}) {
    final personId = json['per_id'] as int?;
    final id = json['id'] as int?;
    if (id == null || personId == null) {
      throw const FormatException(
        'El backend no devolvió los IDs del usuario.',
      );
    }
    return UserModel(
      id: id,
      personId: personId,
      name: name ?? '',
      email: json['correo'] as String? ?? '',
    );
  }
}
