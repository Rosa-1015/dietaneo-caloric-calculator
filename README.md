# 🍎 Dietaneo Caloric Calculator (Pro Version)

A professional-grade caloric needs calculator based on the **Harris-Benedict formula**, refactored to follow **modular programming** principles and clean architecture. Now fully **Dockerized** with **Redis** caching and advanced clinical validation logic.

## 📂 Project Structure
The project follows a modern Python layout to ensure scalability:

* **`app/`**: Core application directory.
    * **`api.py`**: FastAPI configuration, **custom human-readable error handlers**, and CORS setup.
    * **`calculations.py`**: Core mathematical logic, including **BMI-based weight correction (IMC 24.9)** and age-related metabolism reduction.
    * **`validations.py`**: Validation utilities and helpers.
    * **`main.py`**: Alternative API configuration (legacy).
* **`test/`**: Unit tests directory (pytest-based).
* **`docs/`**: Developer documentation.
    * **`README.md`**: Documentation index for developers.
    * **`TESTING.md`**: Complete testing guide and best practices.
* **`docker-compose.yml`**: Orchestration for the Backend (FastAPI) and Cache (Redis) services.
* **`Dockerfile`**: Container recipe for the Python environment.
* **`.env`**: Environment variables (secrets and configuration).
* **`test.http`**: Configuration for rapid API testing within VS Code.
* **`requirements.txt`**: Project dependencies.
* **`CLAUDE.md`**: Architecture and development guidelines.

## 🚀 Professional Features
* **Humanized Validation**: Custom error handling that accepts both dots and commas (`,`, `.`) for decimal inputs, providing clear Spanish messages for the frontend.
* **Clinical Weight Correction**: Automatically applies the **Adjusted Weight formula** for users with **BMI ≥ 30**, using an **Ideal BMI of 24.9** to prevent caloric overestimation in obesity cases.
* **Metabolic Age Adjustment**: Dynamic caloric reduction based on the user's decade (from 40 to 80+ years).
* **Dockerized Workflow**: Consistent environment across development and production using Docker Compose.
* **Redis Integration**: High-performance caching layer for optimized responses.
* **Clean Architecture**: Logical separation between the API layer and core calculation logic.
* **Code Quality**: Pre-configured with **Ruff** to ensure PEP8 compliance and clean code.

## 💻 Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Rosa-1015/dietaneo-calculator.git](https://github.com/Rosa-1015/dietaneo-calculator.git)
    cd dietaneo-calculator
    ```

2.  **Run with Docker (Recommended):**
    ```bash
    docker compose up --build
    ```
    The API will be available at `http://localhost:8001`

3.  **Manual Setup (Virtual Env):**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    python -m uvicorn app.api:app --reload --port 8001
    ```

## 🔍 Code Quality & Testing
Before pushing changes, ensure the code follows style guidelines:

```powershell
python -m ruff check .
```

## 👨‍💻 For Developers

For detailed guides on testing, architecture, and development workflows, see the [Developer Documentation](docs/README.md).

Quick links:
- **[Testing Guide](docs/TESTING.md)** - Complete unit testing guide (pytest, FastAPI)
- **[CLAUDE.md](CLAUDE.md)** - Architecture & development setup
- **[API Documentation](#-api-documentation)** - Endpoint details below

## 🌐 API Documentation

* **Swagger UI**: Access `http://localhost:8001/docs` for interactive testing.
* **Main Endpoint**: `POST /calculate`
* **Input Flexibility**: Accepts `string`, `int`, or `float` to handle various frontend formats.
* **Health Check**: `GET /`

## 🌐 Deployment

This project is designed to be deployed on cloud environments (such as Hetzner/AWS). 

**Workflow:** Test locally → `git push` → `ssh` to server → `git pull`

Ejecuta el siguiente comando para actualizar el servicio:

```bash
docker compose up --build -d
```