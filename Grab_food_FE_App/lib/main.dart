import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'package:food_delivery/common/color_extension.dart';
import 'package:food_delivery/common/locator.dart';
import 'package:food_delivery/common/service_call.dart';
import 'package:food_delivery/view/login/welcome_view.dart';
import 'package:food_delivery/view/main_tabview/main_tabview.dart';
import 'package:food_delivery/view/on_boarding/startup_view.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'common/globs.dart';
import 'common/my_http_overrides.dart';

SharedPreferences? prefs;

Future<void> main() async {
  // Đảm bảo các widget được khởi tạo trước khi chạy ứng dụng.
  WidgetsFlutterBinding.ensureInitialized();

  // Thiết lập các dịch vụ và ghi đè HTTP nếu cần.
  setUpLocator();
  HttpOverrides.global = MyHttpOverrides();

  // Khởi tạo SharedPreferences.
  prefs = await SharedPreferences.getInstance();

  // Kiểm tra trạng thái đăng nhập của người dùng.
  if (Globs.udValueBool(Globs.userLogin)) {
    ServiceCall.userPayload = Globs.udValue(Globs.userPayload);
  }

  // Cấu hình loading indicator.
  configLoading();

  // Chạy ứng dụng với widget gốc.
  runApp(const MyApp(defaultHome: StartupView()));
}

void configLoading() {
  EasyLoading.instance
    ..indicatorType = EasyLoadingIndicatorType.ring
    ..loadingStyle = EasyLoadingStyle.custom
    ..indicatorSize = 45.0
    ..radius = 5.0
    ..progressColor = TColor.primaryText
    ..backgroundColor = TColor.primary
    ..indicatorColor = Colors.yellow
    ..textColor = TColor.primaryText
    ..userInteractions = false
    ..dismissOnTap = false;
}

class MyApp extends StatefulWidget {
  final Widget defaultHome;
  const MyApp({super.key, required this.defaultHome});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Food Delivery',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        fontFamily: "Metropolis",
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: widget.defaultHome,
      navigatorKey: locator<NavigationService>().navigatorKey,
      onGenerateRoute: (routeSettings) {
        switch (routeSettings.name) {
          case "welcome":
            return MaterialPageRoute(builder: (context) => const WelcomeView());
          case "Home":
            return MaterialPageRoute(builder: (context) => const MainTabView());
          default:
            return MaterialPageRoute(
              builder: (context) => Scaffold(
                body: Center(
                  child: Text("No path for ${routeSettings.name}"),
                ),
              ),
            );
        }
      },
      builder: EasyLoading.init(),
    );
  }
}
