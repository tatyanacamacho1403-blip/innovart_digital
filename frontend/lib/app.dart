import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import 'core/constants/app_routes.dart';
import 'core/theme/app_theme.dart';
import 'logic/auth_service.dart';
import 'presentation/screens/auth/login_screen.dart';
import 'presentation/screens/auth/register_screen.dart';
import 'presentation/screens/home/landing_screen.dart';
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
              builder: (_) => const LandingScreen(),
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
