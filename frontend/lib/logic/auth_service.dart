import '../data/api/api_client.dart';
import '../data/models/user_model.dart';

import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

enum SessionRestoreResult { authenticated, unauthenticated, connectionError }

class AuthService {
  AuthService._();
  static final AuthService instance = AuthService._();
  static const _secureStorage = FlutterSecureStorage();

  UserModel? _currentUser;
  UserModel? get currentUser => _currentUser;
  static const _tokenKey = 'auth.token';
  static const _rememberedEmailKey = 'auth.remembered_email';
  static const _userIdKey = 'auth.user_id';
  static const _personIdKey = 'auth.person_id';
  static const _emailKey = 'auth.email';
  static const _nameKey = 'auth.name';
  static const _documentTypeKey = 'auth.document_type';
  static const _documentNumberKey = 'auth.document_number';
  static const _phoneKey = 'auth.phone';
  static const _addressKey = 'auth.address';

  /// Restores a saved session and validates its token with the existing API.
  Future<SessionRestoreResult> restoreSession() async {
    final preferences = await SharedPreferences.getInstance();
    var token = await _secureStorage.read(key: _tokenKey);
    // Migrate tokens saved by earlier versions from unencrypted preferences.
    final legacyToken = preferences.getString(_tokenKey);
    if ((token == null || token.isEmpty) && legacyToken != null) {
      token = legacyToken;
      await _secureStorage.write(key: _tokenKey, value: token);
      await preferences.remove(_tokenKey);
    } else if (legacyToken != null) {
      await preferences.remove(_tokenKey);
    }
    final id = preferences.getInt(_userIdKey);
    final personId = preferences.getInt(_personIdKey);
    if (token == null || token.isEmpty || id == null || personId == null) {
      await _clearSavedSession(preferences);
      return SessionRestoreResult.unauthenticated;
    }

    ApiClient.instance.setAccessToken(token);
    try {
      final person = await ApiClient.instance.get('/api/personas/$personId');
      final name = person is Map ? _personName(person) : '';
      _currentUser = UserModel(
        id: id,
        personId: personId,
        email: preferences.getString(_emailKey) ?? '',
        name: name.isEmpty ? preferences.getString(_nameKey) ?? '' : name,
        documentType: person is Map
            ? person['documento']?.toString() ?? ''
            : preferences.getString(_documentTypeKey) ?? '',
        documentNumber: person is Map
            ? person['cedula']?.toString() ?? ''
            : preferences.getString(_documentNumberKey) ?? '',
        phone: person is Map
            ? person['telefono']?.toString() ?? ''
            : preferences.getString(_phoneKey) ?? '',
        address: person is Map
            ? person['direccion']?.toString() ?? ''
            : preferences.getString(_addressKey) ?? '',
      );
      return SessionRestoreResult.authenticated;
    } catch (error) {
      // Clear credentials explicitly rejected by the backend.
      if (error is ApiException &&
          (error.statusCode == 401 || error.statusCode == 403)) {
        _currentUser = null;
        ApiClient.instance.clearAccessToken();
        await _clearSavedSession(preferences);
        return SessionRestoreResult.unauthenticated;
      }
      // A network/server failure does not authorize private operations. Keep
      // the credential so the user can retry when connectivity returns.
      _currentUser = null;
      return SessionRestoreResult.connectionError;
    }
  }

  Future<UserModel> login(
    String email,
    String password, {
    bool rememberAccount = false,
  }) async {
    final result = await ApiClient.instance.post('/api/usuarios/login', {
      'correo': email.trim().toLowerCase(),
      'contrasena': password,
    });
    if (result is! Map || result['usuario'] is! Map) {
      throw const ApiException('Respuesta de inicio de sesión inválida.');
    }
    final token = result['token'];
    if (token is! String || token.isEmpty) {
      throw const ApiException('El backend no devolvió un token de acceso.');
    }
    ApiClient.instance.setAccessToken(token);

    final userJson = Map<String, dynamic>.from(result['usuario'] as Map);
    final user = UserModel.fromApi(userJson);
    dynamic person;
    try {
      person = await ApiClient.instance.get('/api/personas/${user.personId}');
    } catch (_) {
      ApiClient.instance.clearAccessToken();
      rethrow;
    }
    if (person is Map) {
      final name = _personName(person);
      _currentUser = UserModel(
        id: user.id,
        personId: user.personId,
        email: user.email,
        name: name,
        documentType: person['documento']?.toString() ?? '',
        documentNumber: person['cedula']?.toString() ?? '',
        phone: person['telefono']?.toString() ?? '',
        address: person['direccion']?.toString() ?? '',
      );
    } else {
      _currentUser = user;
    }
    await _saveSession(token, _currentUser!, rememberAccount: rememberAccount);
    return _currentUser!;
  }

  String _personName(Map person) =>
      [
            person['primer_nombre'],
            person['segundo_nombre'],
            person['primer_apellido'],
            person['segundo_apellido'],
          ]
          .map((part) => part?.toString().trim() ?? '')
          .where((part) => part.isNotEmpty)
          .join(' ');

  Future<void> _saveSession(
    String token,
    UserModel user, {
    required bool rememberAccount,
  }) async {
    final preferences = await SharedPreferences.getInstance();
    await _secureStorage.write(key: _tokenKey, value: token);
    await preferences.remove(_tokenKey);
    if (rememberAccount) {
      await preferences.setString(_rememberedEmailKey, user.email);
    } else {
      await preferences.remove(_rememberedEmailKey);
    }
    await preferences.setInt(_userIdKey, user.id);
    await preferences.setInt(_personIdKey, user.personId);
    await preferences.setString(_emailKey, user.email);
    await preferences.setString(_nameKey, user.name);
    await preferences.setString(_documentTypeKey, user.documentType);
    await preferences.setString(_documentNumberKey, user.documentNumber);
    await preferences.setString(_phoneKey, user.phone);
    await preferences.setString(_addressKey, user.address);
  }

  Future<void> _clearSavedSession(SharedPreferences preferences) async {
    await _secureStorage.delete(key: _tokenKey);
    for (final key in [
      _tokenKey,
      _userIdKey,
      _personIdKey,
      _emailKey,
      _nameKey,
      _documentTypeKey,
      _documentNumberKey,
      _phoneKey,
      _addressKey,
    ]) {
      await preferences.remove(key);
    }
  }

  /// Crea primero la persona y luego la cuenta, según el contrato de la API.
  Future<void> register({
    required String email,
    required String password,
    required Map<String, String> person,
  }) async {
    final normalizedEmail = email.trim().toLowerCase();
    await ApiClient.instance.post('/api/usuarios/registro', {
      ...person,
      'correo': normalizedEmail,
      'contrasena': password,
    });
  }

  Future<void> logout() async {
    _currentUser = null;
    ApiClient.instance.clearAccessToken();
    final preferences = await SharedPreferences.getInstance();
    await _clearSavedSession(preferences);
  }

  Future<String?> rememberedEmail() async {
    final preferences = await SharedPreferences.getInstance();
    return preferences.getString(_rememberedEmailKey);
  }
}
