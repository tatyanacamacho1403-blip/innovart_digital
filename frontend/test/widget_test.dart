import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_application_1/app.dart';

void main() {
  testWidgets('muestra la página de inicio al abrir la app', (tester) async {
    await tester.pumpWidget(const MyApp());

    expect(find.text('NUESTROS SERVICIOS'), findsOneWidget);
  });
}
