# 🍎 Dietaneo Caloric Calculator (Pro Version)

A professional-grade caloric needs calculator based on the **Harris-Benedict formula**, refactored to follow **modular programming** principles and clean architecture.Now fully **Dockerized** with **Redis** caching and automated quality checks.

## 📂 Project Structure
The project follows a modern Python layout to ensure scalability:

* **`app/`**: Core application directory.
    * **`api.py`**: FastAPI configuration, custom error handlers, and CORS setup.
    * **`calculations.py`**: Core mathematical logic for nutritional algorithms.
* **`docker-compose.yml`**: Orchestration for the Backend (FastAPI) and Cache (Redis) services.
* **`Dockerfile`**: Container recipe for the Python environment.
* **`.env`**: Environment variables (secrets and configuration).
* **`test.http`**: Configuration for rapid API testing within VS Code.
* **`requirements.txt`**: Project dependencies.
* **`.ruff.toml`**: Configuration for the **Ruff** linter (code quality).

## 🚀 Professional Features
* **Dockerized Workflow**: Consistent environment across development and production using Docker Compose.
* **Redis Integration**: High-performance caching layer for optimized responses.
* **Clean Architecture**: Logical separation between the API layer and core calculation logic.
* **Custom Error Handling**: Localized validation errors in **Spanish** for frontend-ready responses.
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

## 🌐 API Documentation
* **Swagger UI**: Access `http://localhost:8001/docs` for interactive testing.
* **Main Endpoint**: `POST /calculate`
* **Health Check**: `testGET /`

## 🌐 Deployment
This project is designed to be deployed on cloud environments (such as Hetzner/AWS). 
**Workflow:** Test locally → `git push` → `ssh` to server → `git pull` → `docker compose up -d .` 