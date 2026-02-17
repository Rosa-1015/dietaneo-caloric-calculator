# 🍎 Dietaneo Caloric Calculator (Pro Version)

A professional-grade caloric needs calculator based on the **Harris-Benedict formula**, refactored to follow **modular programming** principles and clean architecture.

## 📂 Project Structure
The project is organized into specific modules to ensure scalability and maintainability:

* **`api.py`**: The primary entry point. Configures FastAPI, handles custom error messages in Spanish, and defines endpoints.
* **`calculations.py`**: Core mathematical logic and nutritional calculation algorithms.
* **`test.http`**: Configuration for rapid API testing within VS Code (REST Client).
* **`requirements.txt`**: List of Python dependencies (FastAPI, Uvicorn, Pydantic).
* **`main.py`**: Original CLI entry point (Legacy/Testing).
* **`validations.py`**: Supplementary data validation functions.
* **`LICENSE`**: Project licensing information (MIT).
* **`.gitignore`**: Specifies files and directories to be ignored by Git (e.g., `venv/`, `__pycache__/`).

## 🚀 Features
* **Clean Architecture**: Logical separation between the API layer, data validation, and core calculations.
* **Custom Error Handling**: API responses and validation errors are localized in **Spanish** for seamless frontend integration.
* **FastAPI Powered**: High-performance asynchronous API with automatic documentation.
* **Modular Logic**: Calculation factors (age reduction, activity level) are isolated for easy updates.

## 💻 Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Rosa-1015/dietaneo-calculator.git](https://github.com/Rosa-1015/dietaneo-calculator.git)
    cd dietaneo-calculator
    ```

2.  **Set up the environment:**
    ```powershell
    # Windows
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run API locally:**
    ```bash
    python -m uvicorn api:app --reload --port 8001
    ```

## 🌐 API Endpoints & Testing
* **Documentation**: Once running, access `http://127.0.0.1:8001/docs` for interactive Swagger UI.
* **Main Endpoint**: `POST /calculate`
* **Testing**: Use the `test.http` file with the VS Code **REST Client** extension for local testing.

## 🌐 Deployment
This project is designed to be deployed on cloud environments (such as Hetzner). 

**Best Practice:** Changes should always be tested locally and pushed to GitHub before being pulled into the production server.