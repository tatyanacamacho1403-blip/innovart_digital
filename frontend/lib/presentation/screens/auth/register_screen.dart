import 'package:flutter/material.dart';

import '../../../core/constants/app_routes.dart';
import '../../../core/utils/validators.dart';
import '../../../logic/auth_service.dart';
import 'auth_scaffold.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});
  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _firstName = TextEditingController();
  final _middleName = TextEditingController();
  final _lastName = TextEditingController();
  final _secondLastName = TextEditingController();
  final _documentNumber = TextEditingController();
  final _address = TextEditingController();
  final _email = TextEditingController();
  final _phone = TextEditingController();
  final _birthdate = TextEditingController();
  final _password = TextEditingController();
  final _confirm = TextEditingController();
  static const _documentTypes = [
    'Cédula de ciudadanía (CC)',
    'Cédula de extranjería (CE)',
    'Pasaporte',
    'Permiso por Protección Temporal (PPT)',
  ];
  String? _documentType;
  bool _showPass = false, _showConfirm = false, _loading = false;
  String? _error;

  @override
  void dispose() {
    for (final controller in [
      _firstName,
      _middleName,
      _lastName,
      _secondLastName,
      _documentNumber,
      _address,
      _email,
      _phone,
      _birthdate,
      _password,
      _confirm,
    ]) {
      controller.dispose();
    }
    super.dispose();
  }

  void _clearError() {
    if (_error != null) setState(() => _error = null);
  }

  Future<void> _selectBirthdate() async {
    final today = DateTime.now();
    final selected = await showDatePicker(
      context: context,
      initialDate: DateTime(today.year - 18, today.month, today.day),
      firstDate: DateTime(1900),
      lastDate: today,
      helpText: 'Selecciona tu fecha de nacimiento',
    );
    if (selected == null) return;
    _birthdate.text =
        '${selected.year.toString().padLeft(4, '0')}-'
        '${selected.month.toString().padLeft(2, '0')}-'
        '${selected.day.toString().padLeft(2, '0')}';
    _clearError();
  }

  String? _personName(String? value, String label) {
    final base = Validators.required(value, field: label);
    if (base != null) return base;
    return RegExp(
          r"^[\p{L}]+(?:[ '\-][\p{L}]+)*$",
          unicode: true,
        ).hasMatch(value!.trim())
        ? null
        : 'Usa solo letras';
  }

  String? _phoneValidator(String? value) {
    final base = Validators.required(value, field: 'El teléfono');
    if (base != null) return base;
    final digits = value!.replaceAll(RegExp(r'\D'), '');
    return digits.length >= 7 && digits.length <= 15
        ? null
        : 'Ingresa un teléfono válido';
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      await AuthService.instance.register(
        email: _email.text,
        password: _password.text,
        person: {
          // El contrato Flask actual usa "cedula" para el número y
          // "documento" para el tipo de documento.
          'primer_nombre': _firstName.text.trim(),
          'segundo_nombre': _middleName.text.trim(),
          'primer_apellido': _lastName.text.trim(),
          'segundo_apellido': _secondLastName.text.trim(),
          'documento': _documentType!,
          'cedula': _documentNumber.text.trim(),
          'direccion': _address.text.trim(),
          'telefono': _phone.text.trim(),
          'fecha_nacimiento': _birthdate.text,
        },
      );
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Cuenta creada. Ya puedes iniciar sesión.'),
        ),
      );
      Navigator.pushNamedAndRemoveUntil(context, AppRoutes.login, (_) => false);
    } catch (error) {
      if (mounted) setState(() => _error = error.toString());
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Widget _field(
    TextEditingController controller,
    String label,
    IconData icon, {
    TextInputType? type,
    String? Function(String?)? validator,
    bool obscure = false,
    Widget? suffix,
    VoidCallback? onTap,
    bool readOnly = false,
  }) => TextFormField(
    controller: controller,
    keyboardType: type,
    readOnly: readOnly,
    onTap: onTap,
    textCapitalization: type == TextInputType.emailAddress
        ? TextCapitalization.none
        : TextCapitalization.words,
    obscureText: obscure,
    decoration: authInput(label, icon, suffix: suffix).copyWith(
      prefixIcon: Icon(icon, color: const Color(0xFF6D3DE0), size: 20),
    ),
    validator: validator ?? (v) => Validators.required(v, field: label),
    onChanged: (_) => _clearError(),
  );

  Widget _row(BuildContext context, List<Widget> fields, {bool full = false}) {
    final narrow = MediaQuery.sizeOf(context).width < 600 || full;
    if (narrow) {
      return Column(
        children: [
          for (var i = 0; i < fields.length; i++) ...[
            fields[i],
            if (i != fields.length - 1) const SizedBox(height: 12),
          ],
        ],
      );
    }
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Expanded(child: fields[0]),
        const SizedBox(width: 14),
        Expanded(child: fields[1]),
      ],
    );
  }

  @override
  Widget build(BuildContext context) => AuthScaffold(
    child: AuthCard(
      icon: Icons.person_add_alt_1_rounded,
      title: 'Registrarse',
      subtitle: 'Crea tu cuenta en pocos segundos',
      form: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _row(context, [
              _field(
                _firstName,
                'Nombre',
                Icons.person_outline,
                validator: (v) => _personName(v, 'El nombre'),
              ),
              _field(
                _middleName,
                'Segundo nombre',
                Icons.person_outline,
                validator: (v) => _personName(v, 'El segundo nombre'),
              ),
            ]),
            const SizedBox(height: 12),
            _row(context, [
              _field(
                _lastName,
                'Primer apellido',
                Icons.person_outline,
                validator: (v) => _personName(v, 'El primer apellido'),
              ),
              _field(
                _secondLastName,
                'Segundo apellido',
                Icons.person_outline,
                validator: (v) => _personName(v, 'El segundo apellido'),
              ),
            ]),
            const SizedBox(height: 12),
            _row(context, [
              DropdownButtonFormField<String>(
                initialValue: _documentType,
                isExpanded: true,
                decoration: authInput('', Icons.badge_outlined).copyWith(
                  prefixIcon: const Icon(
                    Icons.badge_outlined,
                    color: Color(0xFF6D3DE0),
                    size: 20,
                  ),
                ),
                hint: const Text(
                  'Tipo de documento',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                items: _documentTypes
                    .map(
                      (type) => DropdownMenuItem(
                        value: type,
                        child: Text(type, overflow: TextOverflow.ellipsis),
                      ),
                    )
                    .toList(),
                validator: (value) =>
                    value == null ? 'Selecciona el tipo de documento' : null,
                onChanged: (value) {
                  setState(() => _documentType = value);
                  _clearError();
                },
              ),
              _field(
                _documentNumber,
                'Número de documento',
                Icons.badge_outlined,
                type: TextInputType.text,
              ),
            ]),
            const SizedBox(height: 12),
            _field(
              _birthdate,
              'Fecha de nacimiento',
              Icons.calendar_today_outlined,
              type: TextInputType.datetime,
              validator: Validators.date,
              onTap: _selectBirthdate,
              readOnly: true,
            ),
            const SizedBox(height: 12),
            _field(_address, 'Dirección', Icons.location_on_outlined),
            const SizedBox(height: 12),
            _field(
              _email,
              'Correo electrónico',
              Icons.email_outlined,
              type: TextInputType.emailAddress,
              validator: Validators.email,
            ),
            const SizedBox(height: 12),
            _field(
              _phone,
              'Teléfono',
              Icons.phone_outlined,
              type: TextInputType.phone,
              validator: _phoneValidator,
            ),
            const SizedBox(height: 12),
            _row(context, [
              _field(
                _password,
                'Contraseña',
                Icons.lock_outline,
                obscure: !_showPass,
                validator: Validators.password,
                suffix: IconButton(
                  onPressed: () => setState(() => _showPass = !_showPass),
                  icon: Icon(
                    _showPass ? Icons.visibility_off : Icons.visibility,
                  ),
                ),
              ),
              _field(
                _confirm,
                'Confirmar contraseña',
                Icons.lock_outline,
                obscure: !_showConfirm,
                validator: Validators.confirmPassword(() => _password.text),
                suffix: IconButton(
                  onPressed: () => setState(() => _showConfirm = !_showConfirm),
                  icon: Icon(
                    _showConfirm ? Icons.visibility_off : Icons.visibility,
                  ),
                ),
              ),
            ]),
            if (_error != null)
              Padding(
                padding: const EdgeInsets.only(top: 10),
                child: Text(
                  _error!,
                  style: TextStyle(color: Theme.of(context).colorScheme.error),
                ),
              ),
            const SizedBox(height: 14),
            AuthSubmit(
              label: _loading ? 'Creando cuenta…' : 'Crear cuenta',
              onPressed: _loading ? null : _submit,
            ),
            const SizedBox(height: 14),
            const Row(
              children: [
                Expanded(child: Divider()),
                Padding(
                  padding: EdgeInsets.symmetric(horizontal: 12),
                  child: Text('o', style: TextStyle(color: Color(0xFF77758A))),
                ),
                Expanded(child: Divider()),
              ],
            ),
            const SizedBox(height: 12),
            const Text(
              'Registrarse con:',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 13, color: Color(0xFF58546B)),
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: null,
                    icon: const Icon(
                      Icons.g_mobiledata,
                      color: Color(0xFF6D3DE0),
                    ),
                    label: const Text('Google'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: null,
                    icon: const Icon(Icons.window, color: Color(0xFF6D3DE0)),
                    label: const Text('Microsoft'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
      footer: Column(
        children: [
          const Text(
            '¿Ya tienes una cuenta? ',
            style: TextStyle(fontSize: 12, color: Color(0xFF77758A)),
          ),
          TextButton(
            onPressed: () => Navigator.pushNamed(context, AppRoutes.login),
            style: TextButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 4),
            ),
            child: const Text(
              'Inicia sesión',
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
