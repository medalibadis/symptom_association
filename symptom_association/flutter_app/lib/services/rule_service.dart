import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/symptom.dart';
import '../models/association_rule.dart';

class RuleService {
  List<Symptom> _allSymptoms = [];
  List<AssociationRule> _rules = [];
  bool _isLoaded = false;

  Future<void> loadRules() async {
    if (_isLoaded) return;

    try {
      // Load JSON from assets
      final String jsonString =
          await rootBundle.loadString('assets/association_rules.json');
      final Map<String, dynamic> data = json.decode(jsonString);

      // Parse symptoms
      final List<dynamic> symptomsJson = data['symptoms'];
      _allSymptoms = symptomsJson
          .map((s) => Symptom.fromString(s as String))
          .toList()
        ..sort((a, b) => a.displayName.compareTo(b.displayName));

      // Parse rules
      final List<dynamic> rulesJson = data['rules'];
      _rules = rulesJson
          .map((r) => AssociationRule.fromJson(r as Map<String, dynamic>))
          .toList();

      _isLoaded = true;
    } catch (e) {
      print('Error loading rules: $e');
      // Generate sample data for testing
      _generateSampleData();
    }
  }

  void _generateSampleData() {
    // Sample symptoms for testing
    _allSymptoms = [
      Symptom.fromString('fever'),
      Symptom.fromString('cough'),
      Symptom.fromString('fatigue'),
      Symptom.fromString('headache'),
      Symptom.fromString('sore_throat'),
      Symptom.fromString('runny_nose'),
      Symptom.fromString('body_ache'),
      Symptom.fromString('chills'),
      Symptom.fromString('nausea'),
      Symptom.fromString('shortness_of_breath'),
    ]..sort((a, b) => a.displayName.compareTo(b.displayName));

    // Sample rules
    _rules = [
      AssociationRule(
        antecedents: ['fever', 'cough'],
        consequents: ['headache'],
        support: 0.25,
        confidence: 0.85,
        lift: 2.3,
      ),
      AssociationRule(
        antecedents: ['fever'],
        consequents: ['body_ache'],
        support: 0.30,
        confidence: 0.75,
        lift: 1.8,
      ),
      AssociationRule(
        antecedents: ['cough', 'sore_throat'],
        consequents: ['runny_nose'],
        support: 0.20,
        confidence: 0.70,
        lift: 2.1,
      ),
    ];

    _isLoaded = true;
  }

  List<Symptom> get allSymptoms => _allSymptoms;

  List<AssociationRule> findAssociations(List<Symptom> selectedSymptoms) {
    final selectedNames = selectedSymptoms.map((s) => s.name).toList();
    
    // Find rules where all antecedents are in selected symptoms
    final matchingRules = _rules
        .where((rule) => rule.matchesSymptoms(selectedNames))
        .toList()
      ..sort((a, b) => b.confidence.compareTo(a.confidence));

    return matchingRules;
  }

  List<String> getRecommendedSymptoms(List<Symptom> selectedSymptoms) {
    final associations = findAssociations(selectedSymptoms);
    final recommended = <String>{};

    for (var rule in associations) {
      recommended.addAll(rule.consequents);
    }

    // Remove already selected symptoms
    final selectedNames = selectedSymptoms.map((s) => s.name).toSet();
    recommended.removeAll(selectedNames);

    return recommended.toList();
  }
}
