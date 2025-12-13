class Symptom {
  final String name;
  final String displayName;

  Symptom({
    required this.name,
    required this.displayName,
  });

  factory Symptom.fromString(String name) {
    return Symptom(
      name: name,
      displayName: _formatSymptomName(name),
    );
  }

  static String _formatSymptomName(String name) {
    // Convert snake_case to Title Case
    return name
        .split('_')
        .map((word) => word[0].toUpperCase() + word.substring(1))
        .join(' ');
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Symptom &&
          runtimeType == other.runtimeType &&
          name == other.name;

  @override
  int get hashCode => name.hashCode;

  @override
  String toString() => displayName;
}
