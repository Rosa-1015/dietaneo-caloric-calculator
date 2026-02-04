# 🍎 Dietaneo Caloric Calculator (Pro Version)

Calculadora profesional de necesidades calóricas basada en la fórmula de Harris-Benedict, refactorizada para seguir principios de **programación modular**.

## 🛠️ Project Structure
- `main.py`: The entry point and user interface flow.
- `validations.py`: Data entry shielding (Gender, Weight, Height, Age, Activity).
- `calculations.py`: The "Engine Room" (BMR and TDEE formulas).

## 🚀 Features
- **Clean Architecture**: Logical separation between UI, validation, and calculations.
- **Robustness**: Input validation using `try-except` blocks and `while` loops.
- **Localization**: Internal code in English for professional standards; User Interface in Spanish.

## 💻 How to use
```bash
python main.py