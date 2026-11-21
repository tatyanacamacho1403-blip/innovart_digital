import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class ApiException implements Exception {
  const ApiException(this.message, {this.statusCode});
  final String message;
  final int? statusCode;

  @override
  String toString() => message;
}

class ApiClient {
  ApiClient._();
  static final ApiClient instance = ApiClient._();
  final http.Client _http = http.Client();
  String? _accessToken;

  void setAccessToken(String token) => _accessToken = token;
  void clearAccessToken() => _accessToken = null;

  static const _configuredUrl = String.fromEnvironment('API_BASE_URL');
  static String get _baseUrl {
    if (_configuredUrl.isNotEmpty) return _configuredUrl;
    if (kIsWeb) return 'http://localhost:5000';
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return 'http://10.2.135.149:5000';
      default:
        return 'http://127.0.0.1:5000';
    }
  }

  Future<dynamic> get(String path) => _send('GET', path);
  Future<dynamic> post(String path, Map<String, dynamic> body) =>
      _send('POST', path, body: body);
  Future<dynamic> delete(String path) => _send('DELETE', path);

  Future<dynamic> _send(
    String method,
    String path, {
    Map<String, dynamic>? body,
  }) async {
    final uri = Uri.parse('$_baseUrl$path');
    try {
      final request = http.Request(method, uri)
        ..headers['Accept'] = 'application/json'
        ..headers['Content-Type'] = 'application/json';
      if (_accessToken != null) {
        request.headers['Authorization'] = 'Bearer $_accessToken';
      }
      if (body != null) request.body = jsonEncode(body);
      final streamed = await _http
          .send(request)
          .timeout(const Duration(seconds: 15));
      final response = await http.Response.fromStream(streamed);
      dynamic data;
      if (response.body.isNotEmpty) {
        try {
          data = jsonDecode(response.body);
        } on FormatException {
          throw const ApiException(
            'El servidor devolvió una respuesta inválida.',
          );
        }
      }
      if (response.statusCode < 200 || response.statusCode >= 300) {
        final message = data is Map
            ? (data['mensaje'] ?? data['error'] ?? data['campos'])
            : null;
        throw ApiException(
          message?.toString() ?? 'Error del servidor (${response.statusCode}).',
          statusCode: response.statusCode,
        );
      }
      return data;
    } on ApiException {
      rethrow;
    } catch (error) {
      if (error is http.ClientException || error is Exception) {
        throw ApiException(
          'No se pudo conectar con el backend. Revisa que esté iniciado y que API_BASE_URL sea accesible desde este dispositivo.',
        );
      }
      rethrow;
    }
  }
}
