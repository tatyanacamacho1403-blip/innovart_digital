import 'package:flutter/material.dart';

import '../../../core/constants/app_routes.dart';
import '../../../core/utils/validators.dart';
import '../../../logic/auth_service.dart';
import 'auth_scaffold.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _email = TextEditingController();
  final _password = TextEditingController();
  bool _showPassword = false, _remember = false, _loading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadRememberedAccount();
  }

  Future<void> _loadRememberedAccount() async {
    final email = await AuthService.instance.rememberedEmail();
    if (!mounted || email == null || email.isEmpty) return;
    setState(() {
      _email.text = email;
      _remember = true;
    });
  }

  @override
  void dispose() {
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      await AuthService.instance.login(
        _email.text,
        _password.text,
        rememberAccount: _remember,
      );
      if (mounted) {
        final resumeBooking =
            ModalRoute.of(context)?.settings.arguments == 'resume_booking';
        if (resumeBooking) {
          Navigator.pop(context);
        } else {
          Navigator.pushReplacementNamed(context, AppRoutes.main, arguments: 0);
        }
      }
    } catch (error) {
      if (mounted) setState(() => _error = error.toString());
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) => AuthScaffold(
    child: AuthCard(
      icon: Icons.lock_outline_rounded,
      title: 'Iniciar sesión',
      subtitle: 'Accede a tu cuenta para gestionar tus servicios',
      form: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextFormField(
              controller: _email,
              keyboardType: TextInputType.emailAddress,
              decoration: authInput('Correo electrónico', Icons.email_outlined),
              validator: Validators.email,
              onChanged: (_) {
                if (_error != null) setState(() => _error = null);
              },
            ),
            const SizedBox(height: 14),
            TextFormField(
              controller: _password,
              obscureText: !_showPassword,
              decoration: authInput(
                'Contraseña',
                Icons.lock_outline,
                suffix: IconButton(
                  onPressed: () =>
                      setState(() => _showPassword = !_showPassword),
                  icon: Icon(
                    _showPassword ? Icons.visibility_off : Icons.visibility,
                  ),
                ),
              ),
              validator: Validators.password,
              onChanged: (_) {
                if (_error != null) setState(() => _error = null);
              },
            ),
            Wrap(
              alignment: WrapAlignment.spaceBetween,
              crossAxisAlignment: WrapCrossAlignment.center,
              children: [
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Checkbox(
                      value: _remember,
                      activeColor: const Color(0xFF6D3DE0),
                      onChanged: (value) =>
                          setState(() => _remember = value ?? false),
                    ),
                    const Text(
                      'Recordar mi cuenta',
                      style: TextStyle(fontSize: 12, color: Color(0xFF676477)),
                    ),
                  ],
                ),
                TextButton(
                  onPressed: null,
                  child: const Text(
                    '¿Olvidaste tu contraseña?',
                    style: TextStyle(fontSize: 11),
                  ),
                ),
              ],
            ),
            if (_error != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: Text(
                  _error!,
                  style: TextStyle(color: Theme.of(context).colorScheme.error),
                ),
              ),
            AuthSubmit(
              label: _loading ? 'Ingresando…' : 'Ingresar',
              onPressed: _loading ? null : _submit,
            ),
          ],
        ),
      ),
      footer: Column(
        children: [
          const Text(
            '¿No tienes una cuenta? ',
            style: TextStyle(fontSize: 12, color: Color(0xFF77758A)),
          ),
          TextButton(
            onPressed: () => Navigator.pushNamed(context, AppRoutes.register),
            style: TextButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 4),
            ),
            child: const Text(
              'Regístrate aquí',
              style: TextStyle(
                fontSize: 12,
                color: Color(0xFF6D3DE0),
                fontWeight: FontWeight.w700,
              ),
            ),
          ),
        ],
      ),
    ),
  );
}
