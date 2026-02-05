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
1. Clone the repository:
```bash
git clone https://github.com/Rosa-1015/dietaneo-caloric-calculator.git
```
2. Run the application:
```bash
python main.py
```

## 🛠️ Built With
Python 3.13
Git & GitHub

## 📄 License
This project is licensed under the MIT License.