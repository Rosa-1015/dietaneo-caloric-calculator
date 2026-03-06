# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Dietaneo** is a professional-grade caloric needs calculator API built with FastAPI. It implements the Harris-Benedict formula with clinical adjustments for weight correction (obesity), age-related metabolism reduction, and activity-level factors.

### Key Principles
- **Clinical Accuracy**: Weight correction formula (BMI ≥ 30) prevents caloric overestimation in obesity cases
- **Input Flexibility**: Accepts both comma and dot decimal separators
- **User-Friendly Errors**: Spanish-language validation messages for frontend consumption
- **Clean Separation**: Business logic isolated from API layer

## Architecture

### Core Structure
```
app/
├── api.py              # Main FastAPI application with endpoints and error handlers
├── calculations.py     # Pure functions for Harris-Benedict formulas and weight correction
├── validations.py      # CLI validation helpers (legacy, not used by API)
└── main.py             # Alternative/older API file (not the active endpoint)
```

### Key Responsibilities

**api.py** - The active API entry point (`app.api:app`)
- POST `/calculate` - Main endpoint accepting gender, weight, height, age, activity_level
- GET `/` - Health check endpoint
- Custom `RequestValidationError` handler returning structured Spanish error messages
- CORS middleware configured (allows all origins)
- Pydantic model `NutritionData` with field aliases (e.g., `sexo`, `peso`, `altura`, `edad`, `nivel_actividad`)

**calculations.py** - Pure calculation functions
- `get_age_reduction(age)` - Returns metabolic reduction in kcal based on age decade (0-500 kcal)
- `get_activity_factor(activity)` - Maps 1-5 activity level to Harris-Benedict multipliers (1.2-1.9)
- `get_adjusted_weight(weight, height)` - Applies weight correction for BMI ≥ 30 using target BMI of 24.9
- `calculate_bmr(gender, weight, height, age)` - Harris-Benedict revised formula (Roza & Shizgal)
- `calculate_tdee(bmr, factor, reduction)` - Total Daily Energy Expenditure

### Calculation Pipeline
1. Input validation in `api.py` (gender H/M, numeric ranges, activity 1-5)
2. Weight adjustment: `get_adjusted_weight()` (obesity correction)
3. Age-based reduction: `get_age_reduction()`
4. Activity factor: `get_activity_factor()`
5. BMR calculation: `calculate_bmr()` using adjusted weight
6. Final TDEE: `calculate_tdee(bmr, activity_factor, age_reduction)`

### Input Validation Flow
- Gender must be "H" or "M" (case-insensitive)
- Weight/Height accept strings with comma decimals (converted to float)
- Age must be ≥ 18 years
- Activity must be integer 1-5 (decimals rejected)
- All validations return structured error responses with `status: "error"` and human-readable field messages

## Development Commands

### Running Locally

**Docker (Recommended)**
```bash
docker compose up --build
# API available at http://localhost:8001
# Redis available at localhost:6379 (for future caching implementation)
```

**Manual Setup with Virtual Env**
```bash
python -m venv venv
source venv/bin/activate  # or: .\venv\Scripts\activate (Windows)
pip install -r requirements.txt
python -m uvicorn app.api:app --reload --port 8001
```

### Code Quality

**Linting**
```bash
python -m ruff check .
```
Note: No `.ruff.toml` configuration file currently exists; using Ruff defaults.

**Testing**
Currently no tests are implemented (test/ directory is empty). When adding tests:
```bash
pytest                      # Run all tests
pytest -v                   # Verbose output
pytest --cov               # Coverage report
pytest test/test_api.py    # Single test file
```

Testing libraries available: `pytest`, `pytest-cov`, `httpx` (for API testing)

### API Testing

**Interactive Testing**
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc
- VS Code: `test.http` file configured for REST Client extension

**Example Request**
```json
POST /calculate
{
  "sexo": "H",
  "peso": 80.5,
  "altura": 180,
  "edad": 35,
  "nivel_actividad": 3
}
```

## Important Implementation Details

### Validation Aliases
The `NutritionData` model uses `validation_alias` to accept Spanish field names:
- `gender` ← `sexo`
- `weight` ← `peso`
- `height` ← `altura`
- `age` ← `edad`
- `activity_level` ← `nivel_actividad`

Accept both formats in client requests.

### Weight Correction Logic
- Only applies when BMI ≥ 30
- Uses target BMI of 24.9 (upper limit of normal weight)
- Formula: `PC = PI + 0.25 * (actual_weight - PI)` where PI is ideal weight at BMI 24.9
- The 0.25 factor represents metabolic contribution of adipose tissue

### Age Reduction Schedule
| Age Range | Reduction (kcal) |
|-----------|------------------|
| < 40      | 0                |
| 40-49     | 100              |
| 50-59     | 200              |
| 60-69     | 300              |
| 70-79     | 400              |
| 80+       | 500              |

### Supplementation Warning
If weight is corrected AND final TDEE < 1800 kcal, the response includes a micronutrient supplementation recommendation. This prevents malnutrition in low-calorie clinical diets.

## Key Files to Know

- **api.py**: Primary development file for endpoints and validation logic
- **calculations.py**: Update formulas or adjustment factors here
- **docker-compose.yml**: Redis service defined but not actively used (reserved for future caching)
- **requirements.txt**: Keep updated when adding dependencies
- **.env**: Contains configuration (not in git)
- **Dockerfile**: Multi-stage optimizations; uses Python 3.13-slim

## Common Tasks

### Adding a New Endpoint
1. Define input model in `api.py` using Pydantic with `validation_alias`
2. Add endpoint function with validation logic
3. Use functions from `calculations.py` for business logic
4. Return structured response with `status`, `encabezado` (header), and data fields

### Modifying Formulas
All Harris-Benedict formula variations are in `calculations.py`. Each function is independent and documented.

### Adding Tests
Create test files in `test/` directory following pytest conventions:
```python
import pytest
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_calculate_valid_input():
    response = client.post("/calculate", json={
        "sexo": "H",
        "peso": 75,
        "altura": 180,
        "edad": 30,
        "nivel_actividad": 3
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

## Deployment

The project is designed for Docker-based cloud deployment:
1. Build image: `docker compose build`
2. Push to registry
3. On server: `git pull` → `docker compose up --build -d`

FastAPI serves at `0.0.0.0:8001` inside container, mapped to port 8001 on host.
