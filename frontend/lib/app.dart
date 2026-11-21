import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import 'core/constants/app_routes.dart';
import 'core/theme/app_theme.dart';
import 'logic/auth_service.dart';
import 'presentation/screens/auth/login_screen.dart';
import 'presentation/screens/auth/register_screen.dart';
import 'presentation/screens/home/main_shell.dart';

const _developmentServicesRoute = '/__dev_services';
const _developmentBookingFlowEnabled = bool.fromEnvironment('DEV_BOOKING_FLOW');
bool get _useDevelopmentBookingEntry =>
    kDebugMode && _developmentBookingFlowEnabled;

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Innovart Digital',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      initialRoute: _useDevelopmentBookingEntry
          ? _developmentServicesRoute
          : AppRoutes.home,
      onGenerateRoute: (settings) {
        switch (settings.name) {
          case _developmentServicesRoute:
            if (!_useDevelopmentBookingEntry) return null;
            return MaterialPageRoute<void>(
              settings: settings,
              builder: (_) => const _DevelopmentServicesEntry(),
            );
          case AppRoutes.home:
            return MaterialPageRoute<void>(
              settings: settings,
              builder: (_) => const _SessionStartup(),
            );
          case AppRoutes.login:
            return MaterialPageRoute<void>(
              settings: settings,
              builder: (_) => const LoginScreen(),
            );
          case AppRoutes.register:
            return MaterialPageRoute<void>(
              settings: settings,
              builder: (_) => const RegisterScreen(),
            );
          case AppRoutes.main:
            return MaterialPageRoute<void>(
              settings: settings,
              builder: (_) => AuthService.instance.currentUser == null
                  ? const LoginScreen()
                  : MainShell(
                      initialIndex: settings.arguments is int
                          ? settings.arguments! as int
                          : 0,
                    ),
            );
        }
        return null;
      },
    );
  }
}

class _SessionStartup extends StatefulWidget {
  const _SessionStartup();

  @override
  State<_SessionStartup> createState() => _SessionStartupState();
}

class _SessionStartupState extends State<_SessionStartup> {
  SessionRestoreResult? _result;

  @override
  void initState() {
    super.initState();
    _restore();
  }

  Future<void> _restore() async {
    setState(() => _result = null);
    final result = await AuthService.instance.restoreSession();
    if (!mounted) return;
    if (result == SessionRestoreResult.connectionError) {
      setState(() => _result = result);
      return;
    }
    Navigator.pushReplacementNamed(
      context,
      result == SessionRestoreResult.authenticated
          ? AppRoutes.main
          : AppRoutes.login,
      arguments: 0,
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_result != SessionRestoreResult.connectionError) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.wifi_off_rounded, size: 42),
              const SizedBox(height: 16),
              const Text(
                'No pudimos validar tu sesión. Conéctate a Internet e inténtalo de nuevo.',
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              FilledButton(
                onPressed: _restore,
                child: const Text('Reintentar'),
              ),
              TextButton(
                onPressed: () =>
                    Navigator.pushReplacementNamed(context, AppRoutes.login),
                child: const Text('Ir al inicio de sesión'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _DevelopmentServicesEntry extends StatefulWidget {
  const _DevelopmentServicesEntry();

  @override
  State<_DevelopmentServicesEntry> createState() =>
      _DevelopmentServicesEntryState();
}

class _DevelopmentServicesEntryState extends State<_DevelopmentServicesEntry> {
  @override
  Widget build(BuildContext context) =>
      const MainShell(initialIndex: 0, developmentCatalogOnly: true);
}
