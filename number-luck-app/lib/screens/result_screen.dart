import 'package:flutter/material.dart';
import '../main.dart';
import '../strings.dart';
import '../api.dart';

class ResultScreen extends StatefulWidget {
  final String lang, number;
  final String? birthdate;
  const ResultScreen(
      {super.key, required this.lang, required this.number, this.birthdate});

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  late Future<Map<String, dynamic>> _future;
  String get lang => widget.lang;

  @override
  void initState() {
    super.initState();
    _future = Api.analyze(
        number: widget.number, lang: lang, birthdate: widget.birthdate);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(t(lang, "title"))),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (context, snap) {
          if (snap.connectionState != ConnectionState.done) {
            return Center(
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                const CircularProgressIndicator(color: kGold),
                const SizedBox(height: 16),
                Text(t(lang, "loading")),
              ]),
            );
          }
          if (snap.hasError) {
            return Center(child: Padding(
              padding: const EdgeInsets.all(24),
              child: Text("${t(lang, "error")}\n\n${snap.error}",
                  textAlign: TextAlign.center),
            ));
          }
          return _buildResult(snap.data!);
        },
      ),
    );
  }

  Widget _buildResult(Map<String, dynamic> d) {
    final grade = (d["grade"] as num).toDouble();
    final pairs = (d["pairs"] as List).cast<Map<String, dynamic>>();
    final readings = (d["readings"] as List).cast<Map<String, dynamic>>();
    final sum = d["sum"] as Map<String, dynamic>;
    final compat = d["compatibility"] as Map<String, dynamic>?;

    return ListView(padding: const EdgeInsets.all(18), children: [
      // grade circle
      Center(child: _GradeCircle(number: d["number"], grade: grade,
          label: d["grade_label"], lang: lang)),
      if (d["premium"] == true)
        Padding(padding: const EdgeInsets.only(top: 8),
          child: Text(t(lang, "premium"),
              textAlign: TextAlign.center,
              style: const TextStyle(color: kGold, fontWeight: FontWeight.bold))),
      const SizedBox(height: 20),

      // pairs
      _section(t(lang, "pairs")),
      Wrap(spacing: 8, runSpacing: 8, children: [
        for (final p in pairs)
          Chip(
            backgroundColor: (p["power"] as num) >= 0 ? kPurple2 : const Color(0xFF3A1A2A),
            label: Text("${p["pair"]}  ${p["power"]}",
                style: const TextStyle(fontWeight: FontWeight.bold)),
          ),
      ]),
      const SizedBox(height: 20),

      // readings (expandable)
      _section(t(lang, "readings")),
      for (final r in readings)
        Card(
          color: kPurple2,
          child: ExpansionTile(
            iconColor: kGold, collapsedIconColor: Colors.white54,
            title: Text("${(r["positive"] as bool) ? "🟢" : "🔴"}  ${r["pair"]}",
                style: const TextStyle(fontWeight: FontWeight.bold)),
            childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
            children: [Text(r["text"], style: const TextStyle(height: 1.5))],
          ),
        ),
      const SizedBox(height: 20),

      // sum
      _section(t(lang, "sum")),
      Card(color: kPurple2, child: Padding(
        padding: const EdgeInsets.all(16),
        child: Text("${sum["total"]} · ${sum["text"]}", style: const TextStyle(height: 1.5)),
      )),

      // compatibility (if birthday given)
      if (compat != null) ...[
        const SizedBox(height: 20),
        _section("${t(lang, "compat")} — ${compat["overall"]}%"),
        Text(compat["verdict"], style: const TextStyle(color: kPink)),
        const SizedBox(height: 8),
        for (final f in (compat["factors"] as List).cast<Map<String, dynamic>>())
          Padding(padding: const EdgeInsets.symmetric(vertical: 6),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
                Expanded(child: Text(f["name"], style: const TextStyle(fontWeight: FontWeight.w600))),
                Text("${(f["score"] as num).round()}% · ${f["weight_pct"]}%",
                    style: const TextStyle(color: Colors.white54)),
              ]),
              const SizedBox(height: 4),
              ClipRRect(borderRadius: BorderRadius.circular(6),
                child: LinearProgressIndicator(
                  value: (f["score"] as num) / 100,
                  minHeight: 7, backgroundColor: kPurple,
                  color: (f["score"] as num) >= 70 ? const Color(0xFF4ADE80)
                      : (f["score"] as num) >= 45 ? kGold : const Color(0xFFEF4444),
                )),
              const SizedBox(height: 4),
              Text(f["comment"], style: const TextStyle(color: Colors.white60, fontSize: 13)),
            ]),
          ),
      ],
      const SizedBox(height: 30),
    ]);
  }

  Widget _section(String title) => Padding(
        padding: const EdgeInsets.only(bottom: 10),
        child: Text(title, style: const TextStyle(
            fontSize: 18, fontWeight: FontWeight.bold, color: kGold)),
      );
}

class _GradeCircle extends StatelessWidget {
  final String number, label, lang;
  final double grade;
  const _GradeCircle(
      {required this.number, required this.grade, required this.label, required this.lang});

  @override
  Widget build(BuildContext context) {
    final color = grade >= 85 ? const Color(0xFF4ADE80)
        : grade >= 70 ? kGold
        : grade >= 50 ? const Color(0xFFFB923C) : const Color(0xFFEF4444);
    return Column(children: [
      Text(number, style: const TextStyle(fontSize: 24, letterSpacing: 3,
          fontWeight: FontWeight.bold)),
      const SizedBox(height: 12),
      SizedBox(width: 150, height: 150, child: Stack(
        alignment: Alignment.center, children: [
          SizedBox(width: 150, height: 150, child: CircularProgressIndicator(
              value: grade / 100, strokeWidth: 12,
              backgroundColor: kPurple2, color: color)),
          Column(mainAxisSize: MainAxisSize.min, children: [
            Text(grade.toStringAsFixed(1),
                style: TextStyle(fontSize: 36, fontWeight: FontWeight.w800, color: color)),
            Text(label, style: const TextStyle(color: Colors.white70)),
          ]),
        ],
      )),
    ]);
  }
}
