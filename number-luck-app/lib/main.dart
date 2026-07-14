import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'screens/home_screen.dart';

void main() => runApp(const NumberLuckApp());

/// สีธีมม่วง-ทอง (ให้ตรงกับเว็บ)
const Color kPurple = Color(0xFF1A1030);
const Color kPurple2 = Color(0xFF2A1B4A);
const Color kGold = Color(0xFFF5B301);
const Color kPink = Color(0xFFFF7AD9);

class NumberLuckApp extends StatefulWidget {
  const NumberLuckApp({super.key});
  @override
  State<NumberLuckApp> createState() => _NumberLuckAppState();
}

class _NumberLuckAppState extends State<NumberLuckApp> {
  String _lang = "th";

  @override
  void initState() {
    super.initState();
    _loadLang();
  }

  Future<void> _loadLang() async {
    final p = await SharedPreferences.getInstance();
    setState(() => _lang = p.getString("lang") ?? "th");
  }

  Future<void> _setLang(String l) async {
    final p = await SharedPreferences.getInstance();
    await p.setString("lang", l);
    setState(() => _lang = l);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Number Luck",
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: kPurple,
        colorScheme: const ColorScheme.dark(
          primary: kGold, secondary: kPink, surface: kPurple2,
        ),
        fontFamily: "NotoSans",
        appBarTheme: const AppBarTheme(
          backgroundColor: kPurple, foregroundColor: kGold, centerTitle: true,
        ),
      ),
      home: HomeScreen(lang: _lang, onLang: _setLang),
    );
  }
}
