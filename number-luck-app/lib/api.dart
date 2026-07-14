import 'dart:convert';
import 'package:http/http.dart' as http;

/// ไคลเอนต์เรียก Number Luck API
/// เปลี่ยน [baseUrl] เป็น URL จริงหลัง deploy (ตอนนี้ค่า placeholder)
class Api {
  /// TODO: หลัง deploy API บน DO เปลี่ยนเป็น URL จริง
  /// เช่น "https://api.jbacworkhub.com" หรือ "https://ft.jbacworkhub.com/api"
  static const String baseUrl = "https://number-luck-api.ondigitalocean.app";

  static Future<Map<String, dynamic>> _get(
      String path, Map<String, String> params) async {
    final uri = Uri.parse("$baseUrl$path").replace(queryParameters: params);
    final res = await http.get(uri).timeout(const Duration(seconds: 20));
    if (res.statusCode != 200) {
      throw ApiException(res.statusCode, utf8.decode(res.bodyBytes));
    }
    return jsonDecode(utf8.decode(res.bodyBytes)) as Map<String, dynamic>;
  }

  static Future<Map<String, dynamic>> analyze({
    required String number,
    required String lang,
    String? birthdate,
    bool wednesdayPm = false,
    String? name,
  }) {
    final p = <String, String>{"number": number, "lang": lang};
    if (birthdate != null) p["birthdate"] = birthdate;
    if (wednesdayPm) p["wednesday_pm"] = "true";
    if (name != null && name.isNotEmpty) p["name"] = name;
    return _get("/analyze", p);
  }

  static Future<Map<String, dynamic>> weekly(
          {required String lang, String? birthdate, String? name}) =>
      _get("/horoscope/weekly", {
        "lang": lang,
        if (birthdate != null) "birthdate": birthdate,
        if (name != null && name.isNotEmpty) "name": name,
      });

  static Future<Map<String, dynamic>> monthly(
          {required String lang, String? birthdate, String? name}) =>
      _get("/horoscope/monthly", {
        "lang": lang,
        if (birthdate != null) "birthdate": birthdate,
        if (name != null && name.isNotEmpty) "name": name,
      });

  static Future<Map<String, dynamic>> auspiciousDays(
          {required String lang, int days = 14}) =>
      _get("/auspicious-days", {"lang": lang, "days": "$days"});
}

class ApiException implements Exception {
  final int status;
  final String body;
  ApiException(this.status, this.body);
  @override
  String toString() => "API error $status: $body";
}
