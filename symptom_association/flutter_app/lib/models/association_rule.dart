class AssociationRule {
  final List<String> antecedents;
  final List<String> consequents;
  final double support;
  final double confidence;
  final double lift;

  AssociationRule({
    required this.antecedents,
    required this.consequents,
    required this.support,
    required this.confidence,
    required this.lift,
  });

  factory AssociationRule.fromJson(Map<String, dynamic> json) {
    return AssociationRule(
      antecedents: List<String>.from(json['antecedents']),
      consequents: List<String>.from(json['consequents']),
      support: (json['support'] as num).toDouble(),
      confidence: (json['confidence'] as num).toDouble(),
      lift: (json['lift'] as num).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'antecedents': antecedents,
      'consequents': consequents,
      'support': support,
      'confidence': confidence,
      'lift': lift,
    };
  }

  bool matchesSymptoms(List<String> selectedSymptoms) {
    // Check if all antecedents are in selected symptoms
    return antecedents.every((symptom) => selectedSymptoms.contains(symptom));
  }

  String get confidencePercentage => '${(confidence * 100).toStringAsFixed(1)}%';
  String get liftFormatted => lift.toStringAsFixed(2);
}
