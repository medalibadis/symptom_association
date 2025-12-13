# Symptom Checker - Flutter Mobile App

Medical symptom association checker using association rules from Apriori algorithm.

## Features
- Multi-symptom selection
- Association rule-based recommendations
- Confidence indicators
- Offline mode (all rules loaded locally)
- Clean, intuitive UI

## Setup

### Prerequisites
- Flutter SDK (>=3.0.0)
- Dart SDK (>=3.0.0)

### Installation

```bash
# Navigate to app directory
cd flutter_app/symptom_checker

# Get dependencies
flutter pub get

# Run app
flutter run
```

### Add Association Rules

1. Run the Python analysis script to generate `association_rules.json`
2. Copy `association_rules.json` to `assets/` folder
3. Rebuild the app

## Project Structure

```
lib/
├── main.dart                 # App entry point
├── models/
│   ├── symptom.dart          # Symptom model
│   └── association_rule.dart # Rule model
├── services/
│   └── rule_service.dart     # Load and query rules
├── screens/
│   ├── home_screen.dart      # Main screen
│   └── results_screen.dart   # Show associations
└── widgets/
    ├── symptom_chip.dart     # Symptom selector
    └── rule_card.dart        # Display rule
```

## Usage

1. Launch app
2. Select symptoms you're experiencing
3. Tap "Find Associations"
4. View related symptoms and confidence scores
5. See potential disease suggestions

## Model Format

The app expects `association_rules.json` in this format:

```json
{
  "metadata": {
    "total_rules": 150,
    "min_support": 0.05,
    "min_confidence": 0.6
  },
  "symptoms": ["fever", "cough", ...],
  "rules": [
    {
      "antecedents": ["fever", "cough"],
      "consequents": ["headache"],
      "support": 0.25,
      "confidence": 0.85,
      "lift": 2.3
    }
  ]
}
```
