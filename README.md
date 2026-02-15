# 🍎 Dietaneo Caloric Calculator (Pro Version)

A professional-grade caloric needs calculator based on the **Harris-Benedict formula**, refactored to follow **modular programming** principles and clean architecture.

## 📂 Project Structure
The project is organized into specific modules to ensure scalability and maintainability:

* **`main.py`**: The primary entry point of the application.
* **`api.py`**: API configuration and endpoint definitions (Flask/FastAPI).
* **`calculations.py`**: Core mathematical logic and nutritional calculation algorithms.
* **`validations.py`**: Data validation functions for input processing and error handling.
* **`LICENSE`**: Project licensing information (MIT).
* **`.gitignore`**: Specifies files and directories to be ignored by Git (e.g., `venv/`, `__pycache__/`).

## 🚀 Features
* **Clean Architecture**: Logical separation between the API layer, data validation, and core calculations.
* **Robustness**: Advanced input validation using `try-except` blocks to ensure data integrity.
* **Professional Localization**: Internal code and documentation in English; User Interface (UI) in Spanish.

## 💻 Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Rosa-1015/dietaneo-calculator.git](https://github.com/Rosa-1015/dietaneo-calculator.git)
    cd dietaneo-calculator
    ```

2.  **Set up the environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run locally:**
    ```bash
    python main.py
    ```

## 🌐 Deployment
This project is designed to be deployed on cloud environments (such as Hetzner, AWS, or DigitalOcean). 

**Best Practice:** Changes should always be tested locally and pushed to GitHub before being pulled into the production server.