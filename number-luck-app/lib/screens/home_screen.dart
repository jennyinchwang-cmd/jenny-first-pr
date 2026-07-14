import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../main.dart';
import '../strings.dart';
import 'result_screen.dart';

class HomeScreen extends StatefulWidget {
  final String lang;
  final Future<void> Function(String) onLang;
  const HomeScreen({super.key, required this.lang, required this.onLang});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _numCtrl = TextEditingController();
  DateTime? _birth;

  String get lang => widget.lang;

  bool _validNumber(String s) {
    final d = s.replaceAll(RegExp(r'\D'), '');
    final core = d.startsWith('09') ? d.substring(2) : d;
    return RegExp(r'^\d{7,9}$').hasMatch(core);
  }

  void _go() {
    if (!_validNumber(_numCtrl.text)) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(t(lang, "bad_number"))));
      return;
    }
    Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => ResultScreen(
        lang: lang,
        number: _numCtrl.text.trim(),
        birthdate: _birth == null ? null : DateFormat('yyyy-MM-dd').format(_birth!),
      ),
    ));
  }

  Future<void> _pickDate() async {
    final d = await showDatePicker(
      context: context,
      initialDate: DateTime(1995, 1, 1),
      firstDate: DateTime(1930),
      lastDate: DateTime.now(),
    );
    if (d != null) setState(() => _birth = d);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            // language switch
            Align(
              alignment: Alignment.centerRight,
              child: SegmentedButton<String>(
                segments: const [
                  ButtonSegment(value: "th", label: Text("ไทย")),
                  ButtonSegment(value: "en", label: Text("EN")),
                  ButtonSegment(value: "mm", label: Text("မြန်")),
                ],
                selected: {lang},
                onSelectionChanged: (s) => widget.onLang(s.first),
                style: ButtonStyle(
                  visualDensity: VisualDensity.compact,
                ),
              ),
            ),
            const SizedBox(height: 8),
            // hero
            ClipRRect(
              borderRadius: BorderRadius.circular(18),
              child: Image.asset("assets/hero_banner.png",
                  errorBuilder: (_, __, ___) => const SizedBox.shrink()),
            ),
            const SizedBox(height: 16),
            ShaderMask(
              shaderCallback: (r) => const LinearGradient(
                colors: [kGold, kPink, Color(0xFF9B6BFF)],
              ).createShader(r),
              child: Text(t(lang, "title"),
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                      fontSize: 40, fontWeight: FontWeight.w800, color: Colors.white)),
            ),
            Text(t(lang, "tagline"),
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.white60)),
            const SizedBox(height: 28),
            // number field
            TextField(
              controller: _numCtrl,
              keyboardType: TextInputType.phone,
              style: const TextStyle(fontSize: 22, letterSpacing: 2),
              textAlign: TextAlign.center,
              decoration: InputDecoration(
                hintText: t(lang, "phone"),
                filled: true, fillColor: kPurple2,
                border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(14),
                    borderSide: BorderSide.none),
              ),
            ),
            const SizedBox(height: 14),
            // birthday picker
            OutlinedButton.icon(
              onPressed: _pickDate,
              icon: const Icon(Icons.cake_outlined),
              label: Text(_birth == null
                  ? "${t(lang, "pick_date")} (${t(lang, "no_date")})"
                  : DateFormat('d MMM yyyy').format(_birth!)),
              style: OutlinedButton.styleFrom(
                  foregroundColor: kPink,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  side: const BorderSide(color: kPurple2)),
            ),
            const SizedBox(height: 24),
            // analyze
            FilledButton(
              onPressed: _go,
              style: FilledButton.styleFrom(
                backgroundColor: kGold, foregroundColor: kPurple,
                padding: const EdgeInsets.symmetric(vertical: 18),
                textStyle: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              child: Text(t(lang, "analyze")),
            ),
          ]),
        ),
      ),
    );
  }
}
