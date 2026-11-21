import 'package:flutter/material.dart';

import '../../../core/constants/app_routes.dart';

const _navy = Color(0xFF11102F);
const _purple = Color(0xFF6D3DE0);

class AuthScaffold extends StatelessWidget {
  const AuthScaffold({super.key, required this.child});
  final Widget child;

  @override
  Widget build(BuildContext context) => Scaffold(
    body: Stack(
      fit: StackFit.expand,
      children: [
        const DecoratedBox(decoration: BoxDecoration(color: _navy)),
        const Positioned(top: -130, right: -120, child: _Geo(size: 440)),
        const Positioned(bottom: -190, left: -160, child: _Geo(size: 520)),
        SafeArea(
          child: Column(
            children: [
              _Header(),
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.fromLTRB(20, 24, 20, 32),
                  child: Center(
                    child: ConstrainedBox(
                      constraints: const BoxConstraints(maxWidth: 500),
                      child: child,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    ),
  );
}

class _Geo extends StatelessWidget {
  const _Geo({required this.size});
  final double size;
  @override
  Widget build(BuildContext context) => Transform.rotate(
    angle: -.55,
    child: Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        border: Border.all(color: _purple.withValues(alpha: .23), width: 34),
        borderRadius: BorderRadius.circular(90),
      ),
    ),
  );
}

class _Header extends StatelessWidget {
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
    decoration: BoxDecoration(
      color: _navy.withValues(alpha: .92),
      border: Border(
        bottom: BorderSide(color: Colors.white.withValues(alpha: .08)),
      ),
    ),
    child: Row(
      children: [
        const Icon(Icons.auto_awesome, color: Color(0xFF9A72FF), size: 27),
        const SizedBox(width: 9),
        const Expanded(
          child: Text(
            'INNOVART DIGITAL',
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.w800,
              letterSpacing: 1.1,
              fontSize: 13,
            ),
          ),
        ),
        if (MediaQuery.sizeOf(context).width > 720) ...[
          for (final item in [
            'INICIO',
            'SERVICIOS',
            'NOSOTROS',
            'AGENDA',
            'CONTACTO',
          ])
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 9),
              child: Text(
                item,
                style: const TextStyle(
                  color: Colors.white70,
                  fontSize: 10,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
        ],
        if (MediaQuery.sizeOf(context).width > 420) ...[
          TextButton(
            onPressed: () => Navigator.pushNamed(context, AppRoutes.login),
            child: const Text(
              'Iniciar sesión',
              style: TextStyle(color: Colors.white, fontSize: 12),
            ),
          ),
          const SizedBox(width: 4),
          OutlinedButton(
            onPressed: () => Navigator.pushNamed(context, AppRoutes.register),
            style: OutlinedButton.styleFrom(
              foregroundColor: Colors.white,
              side: const BorderSide(color: Color(0xFF8C68F3)),
            ),
            child: const Text('Registrarse', style: TextStyle(fontSize: 12)),
          ),
        ],
      ],
    ),
  );
}

class AuthCard extends StatelessWidget {
  const AuthCard({
    super.key,
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.form,
    required this.footer,
  });
  final IconData icon;
  final String title;
  final String subtitle;
  final Widget form;
  final Widget footer;
  @override
  Widget build(BuildContext context) => Container(
    padding: EdgeInsets.symmetric(
      horizontal: MediaQuery.sizeOf(context).width < 380 ? 20 : 30,
      vertical: 24,
    ),
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(24),
      boxShadow: const [
        BoxShadow(
          color: Color(0x66000000),
          blurRadius: 40,
          offset: Offset(0, 18),
        ),
      ],
    ),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 54,
          height: 54,
          decoration: BoxDecoration(
            color: const Color(0xFFF0EBFF),
            borderRadius: BorderRadius.circular(17),
          ),
          child: Icon(icon, color: _purple, size: 28),
        ),
        const SizedBox(height: 14),
        title == 'Iniciar sesión'
            ? const Text.rich(
                TextSpan(
                  children: [
                    TextSpan(
                      text: 'Iniciar ',
                      style: TextStyle(color: Color(0xFF24213B)),
                    ),
                    TextSpan(
                      text: 'sesión',
                      style: TextStyle(color: _purple),
                    ),
                  ],
                ),
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 27, fontWeight: FontWeight.w800),
              )
            : Text(
                title,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 27,
                  fontWeight: FontWeight.w800,
                  color: Color(0xFF24213B),
                ),
              ),
        const SizedBox(height: 6),
        Text(
          subtitle,
          textAlign: TextAlign.center,
          style: const TextStyle(color: Color(0xFF77758A), fontSize: 13),
        ),
        const SizedBox(height: 23),
        form,
        const SizedBox(height: 18),
        footer,
      ],
    ),
  );
}

InputDecoration authInput(String label, IconData icon, {Widget? suffix}) =>
    InputDecoration(
      labelText: label,
      prefixIcon: Icon(icon, color: const Color(0xFF8A879B), size: 20),
      suffixIcon: suffix,
      filled: true,
      fillColor: const Color(0xFFFAF9FC),
      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 15),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: Color(0xFFE8E6EF)),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: Color(0xFFE8E6EF)),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: _purple, width: 1.5),
      ),
    );

class AuthSubmit extends StatelessWidget {
  const AuthSubmit({super.key, required this.label, required this.onPressed});
  final String label;
  final VoidCallback? onPressed;
  @override
  Widget build(BuildContext context) => SizedBox(
    width: double.infinity,
    height: 50,
    child: DecoratedBox(
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF8052EC), Color(0xFF582BC6)],
        ),
        borderRadius: BorderRadius.circular(12),
        boxShadow: const [
          BoxShadow(
            color: Color(0x338052EC),
            blurRadius: 12,
            offset: Offset(0, 5),
          ),
        ],
      ),
      child: FilledButton(
        onPressed: onPressed,
        style: FilledButton.styleFrom(
          backgroundColor: Colors.transparent,
          shadowColor: Colors.transparent,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        child: Text(
          label,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),
    ),
  );
}

Widget authDivider() => const Row(
  children: [
    Expanded(child: Divider()),
    Padding(
      padding: EdgeInsets.symmetric(horizontal: 12),
      child: Text('o', style: TextStyle(color: Color(0xFF9693A5))),
    ),
    Expanded(child: Divider()),
  ],
);

Widget socialButton(String label, String mark, Color color) =>
    OutlinedButton.icon(
      onPressed: null,
      icon: Text(
        mark,
        style: TextStyle(
          color: color,
          fontWeight: FontWeight.w800,
          fontSize: 16,
        ),
      ),
      label: Text('Continuar con $label'),
      style: OutlinedButton.styleFrom(
        foregroundColor: const Color(0xFF504D60),
        minimumSize: const Size.fromHeight(45),
        side: const BorderSide(color: Color(0xFFE8E6EF)),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(11)),
      ),
    );
