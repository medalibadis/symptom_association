# Flutter App Setup Guide

## Prerequisites

1. **Install Flutter SDK**
   - Download from [flutter.dev](https://flutter.dev/docs/get-started/install)
   - Add Flutter to your PATH
   - Run `flutter doctor` to verify installation

2. **Install Android Studio** (for Android development)
   - Download from [developer.android.com](https://developer.android.com/studio)
   - Install Android SDK and emulator

3. **Install VS Code** (recommended)
   - Download from [code.visualstudio.com](https://code.visualstudio.com/)
   - Install Flutter and Dart extensions

## Setup Steps

### 1. Navigate to App Directory

```bash
cd symptom_association/flutter_app
```

### 2. Create Assets Folder

```bash
mkdir assets
```

### 3. Add Association Rules

1. Run the Python analysis script:
   ```bash
   cd ..
   python symptom_analysis.py
   ```

2. Copy the generated JSON file:
   ```bash
   copy models\association_rules.json flutter_app\assets\
   ```

### 4. Install Dependencies

```bash
flutter pub get
```

### 5. Run the App

#### On Android Emulator:
```bash
flutter run
```

#### On Physical Device:
1. Enable Developer Options on your Android device
2. Enable USB Debugging
3. Connect device via USB
4. Run: `flutter run`

#### On iOS (Mac only):
```bash
flutter run -d ios
```

## Building APK

### Debug APK:
```bash
flutter build apk --debug
```

### Release APK:
```bash
flutter build apk --release
```

APK will be in: `build/app/outputs/flutter-apk/app-release.apk`

## Project Structure

```
flutter_app/
├── lib/
│   ├── main.dart                 # App entry point
│   ├── models/
│   │   ├── symptom.dart          # Symptom data model
│   │   └── association_rule.dart # Rule data model
│   ├── services/
│   │   └── rule_service.dart     # Load and query rules
│   ├── screens/
│   │   ├── home_screen.dart      # Symptom selection
│   │   └── results_screen.dart   # Show associations
│   └── widgets/
│       └── (custom widgets)
├── assets/
│   └── association_rules.json    # ML model data
└── pubspec.yaml                  # Dependencies
```

## Features

### Home Screen
- Search symptoms
- Multi-select symptoms
- Clear selection
- View selected count

### Results Screen
- Display selected symptoms
- Show recommended symptoms
- List association rules
- Confidence/Lift/Support metrics
- IF-THEN rule visualization

## Customization

### Change Theme Colors

Edit `lib/main.dart`:
```dart
colorScheme: ColorScheme.fromSeed(
  seedColor: Colors.blue,  // Change this
  brightness: Brightness.light,
),
```

### Adjust Rule Thresholds

The app uses rules as-is from the JSON file. To change thresholds, modify the Python script and regenerate the JSON.

### Add More Symptoms

Add symptoms to your dataset and regenerate the JSON file.

## Troubleshooting

### "Unable to load asset"
- Make sure `association_rules.json` is in the `assets/` folder
- Check `pubspec.yaml` has the assets section
- Run `flutter clean` then `flutter pub get`

### "No rules found"
- Verify JSON file format matches expected structure
- Check console for loading errors
- Use sample data mode for testing

### App crashes on startup
- Run `flutter doctor` to check for issues
- Clear build cache: `flutter clean`
- Rebuild: `flutter pub get && flutter run`

## Testing

### Run Tests:
```bash
flutter test
```

### Check for Issues:
```bash
flutter analyze
```

## Deployment

### Google Play Store:
1. Create a keystore
2. Configure `android/app/build.gradle`
3. Build release APK
4. Upload to Play Console

### App Store (iOS):
1. Configure signing in Xcode
2. Build release IPA
3. Upload via Xcode or Transporter

## Support

For Flutter issues, visit:
- [Flutter Documentation](https://flutter.dev/docs)
- [Flutter Community](https://flutter.dev/community)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/flutter)
