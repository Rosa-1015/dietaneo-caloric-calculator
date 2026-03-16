# 🧪 Complete Testing Guide for Dietaneo

*Comprehensive testing documentation for the Dietaneo caloric calculator*

---

## 📚 Table of Contents
1. [Why Testing?](#why-testing)
2. [Fundamental Concepts](#fundamental-concepts)
3. [Project Structure](#project-structure)
4. [Your First Test](#your-first-test)
5. [Calculation Tests](#calculation-tests)
6. [API Tests](#api-tests)
7. [Running Tests](#running-tests)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Why Testing?

Imagine you're a chef in a restaurant. Would you serve a dish to customers without tasting it first to make sure it's properly cooked? **Of course not.**

The same applies to code. Tests are like "tasting the dish" before delivery. They give you confidence that:

✅ Your code does exactly what it should do
✅ Future changes don't break existing functionality
✅ Errors are detected early
✅ Other developers (or you in 6 months) trust that the code works

In Dietaneo, it's **critical** that nutritional calculations are accurate. A small error in the formula could affect the end user's health.

---

## Fundamental Concepts

### What is a Unit Test?

A **unit test** tests a **small part** of your code in isolation.

For example:
- A test for the function `get_age_reduction(35)` should return `0`
- A test for `get_activity_factor(3)` should return `1.55`
- A test for weight correction with BMI ≥ 30

It's **not** a test that tests the entire system together. That's called an integration test.

### Test Structure

All tests follow the same pattern: **Arrange → Act → Assert**

```python
# 1. ARRANGE (Prepare): Set up the necessary data
age = 45

# 2. ACT (Execute): Run the function you want to test
result = get_age_reduction(age)

# 3. ASSERT (Verify): Check that the result is what you expected
assert result == 100  # We expect 100 kcal reduction for age 40-50
```

**In formal test code** it looks like this:

```python
def test_age_reduction_40_to_50():
    # Arrange
    age = 45

    # Act
    result = get_age_reduction(age)

    # Assert
    assert result == 100
```

### Why "assert"?

`assert` is a Python keyword that means "I affirm this is true".

- If it's **true** → the test passes ✅
- If it's **false** → the test fails ❌ and pytest shows you what went wrong

Example:
```python
assert 2 + 2 == 4  # PASSES ✅
assert 2 + 2 == 5  # FAILS ❌
```

---

## Project Structure

Currently your `test/` folder is empty. Here's how to organize it:

```
nutrition_calculator/
├── app/
│   ├── api.py                 # FastAPI endpoints
│   ├── calculations.py        # Calculation functions
│   ├── validations.py
│   └── main.py
├── test/                      # ← YOUR TESTS GO HERE
│   ├── __init__.py           # Empty file (tells Python this is a module)
│   ├── test_calculations.py  # Tests for pure functions
│   └── test_api.py           # Tests for endpoints
├── docs/                      # ← DOCUMENTATION FOLDER
│   └── TESTING.md            # This file
├── requirements.txt
├── docker-compose.yml
└── CLAUDE.md
```

**Why this structure?**

- Keeps tests separate from production code
- Pytest automatically finds files starting with `test_`
- It's the industry standard convention (everyone on the team knows where to look)

---

## Your First Test

### Step 1: Create the folder and file

```bash
# From the project root
touch test/__init__.py
touch test/test_calculations.py
```

`__init__.py` is a special Python file (can be empty). It tells Python that this folder is an importable module.

### Step 2: Your first test

Open `test/test_calculations.py` and write:

```python
"""
Tests for the nutritional calculation module.

This file tests all mathematical functions in app/calculations.py
to ensure they do exactly what is expected.
"""

from app.calculations import get_age_reduction


def test_age_reduction_under_40():
    """
    When age is less than 40 years, there should be no reduction.

    This is important because according to clinical logic, metabolism
    is maximum until age 40, then begins to decrease.
    """
    # Arrange
    age = 35

    # Act
    result = get_age_reduction(age)

    # Assert
    assert result == 0
```

**Why does each function have a docstring?**

Because in 3 months you (or a colleague) will read this test and want to know:
- What am I testing?
- Why is it important?
- What's the use case?

### Step 3: Run the test

```bash
# From the project root
pytest test/test_calculations.py::test_age_reduction_under_40 -v
```

You should see:
```
test/test_calculations.py::test_age_reduction_under_40 PASSED ✓
```

**Congratulations! Your first test works.**

---

## Calculation Tests

Here's the complete `test/test_calculations.py` file:

```python
"""
Tests for the nutritional calculation module.

This file tests all mathematical functions in app/calculations.py
to ensure they do exactly what is expected.
"""

import pytest
from app.calculations import (
    get_age_reduction,
    get_activity_factor,
    get_adjusted_weight,
    calculate_bmr,
    calculate_tdee
)


# ============================================================================
# AGE REDUCTION TESTS
# ============================================================================

class TestAgeReduction:
    """Groups all tests related to age reduction."""

    def test_age_under_40_no_reduction(self):
        """People under 40 years old have no caloric reduction."""
        assert get_age_reduction(18) == 0
        assert get_age_reduction(35) == 0
        assert get_age_reduction(39) == 0

    def test_age_40_to_49_reduction_100(self):
        """Ages 40-49 have 100 kcal reduction."""
        assert get_age_reduction(40) == 100
        assert get_age_reduction(45) == 100
        assert get_age_reduction(49) == 100

    def test_age_50_to_59_reduction_200(self):
        """Ages 50-59 have 200 kcal reduction."""
        assert get_age_reduction(50) == 200
        assert get_age_reduction(55) == 200
        assert get_age_reduction(59) == 200

    def test_age_60_to_69_reduction_300(self):
        """Ages 60-69 have 300 kcal reduction."""
        assert get_age_reduction(60) == 300
        assert get_age_reduction(65) == 300
        assert get_age_reduction(69) == 300

    def test_age_70_to_79_reduction_400(self):
        """Ages 70-79 have 400 kcal reduction."""
        assert get_age_reduction(70) == 400
        assert get_age_reduction(75) == 400
        assert get_age_reduction(79) == 400

    def test_age_80_plus_reduction_500(self):
        """Age 80+ has 500 kcal reduction."""
        assert get_age_reduction(80) == 500
        assert get_age_reduction(90) == 500
        assert get_age_reduction(120) == 500


# ============================================================================
# ACTIVITY FACTOR TESTS
# ============================================================================

class TestActivityFactor:
    """Tests that each activity level returns the correct Harris-Benedict multiplier."""

    def test_activity_1_sedentary(self):
        """Level 1 (Sedentary) = multiplier 1.2"""
        assert get_activity_factor(1) == 1.2

    def test_activity_2_light(self):
        """Level 2 (Light) = multiplier 1.375"""
        assert get_activity_factor(2) == 1.375

    def test_activity_3_moderate(self):
        """Level 3 (Moderate) = multiplier 1.55"""
        assert get_activity_factor(3) == 1.55

    def test_activity_4_heavy(self):
        """Level 4 (Heavy) = multiplier 1.725"""
        assert get_activity_factor(4) == 1.725

    def test_activity_5_very_heavy(self):
        """Level 5 (Very Heavy) = multiplier 1.9"""
        assert get_activity_factor(5) == 1.9

    def test_activity_invalid_defaults_to_1_2(self):
        """Invalid values default to 1.2."""
        assert get_activity_factor(10) == 1.2
        assert get_activity_factor(0) == 1.2


# ============================================================================
# WEIGHT ADJUSTMENT TESTS (OBESITY)
# ============================================================================

class TestAdjustedWeight:
    """Tests the weight correction formula for patients with BMI >= 30."""

    def test_normal_weight_no_adjustment(self):
        """
        Normal BMI (< 30) is not adjusted.

        Person: 70 kg, 170 cm
        BMI = 70 / (1.70^2) = 24.22 (normal)
        """
        weight = 70
        height = 170
        result = get_adjusted_weight(weight, height)
        assert result == weight  # No changes

    def test_overweight_no_adjustment(self):
        """
        Overweight (BMI 25-29.9) is not adjusted.

        Person: 85 kg, 170 cm
        BMI = 85 / (1.70^2) = 29.41 (overweight)
        """
        weight = 85
        height = 170
        result = get_adjusted_weight(weight, height)
        assert result == weight

    def test_obese_weight_is_adjusted(self):
        """
        BMI >= 30 is adjusted using clinical formula.

        Person: 110 kg, 170 cm
        BMI = 110 / (1.70^2) = 38.05 (obese)

        The function should return less weight than the actual.
        """
        actual_weight = 110
        height = 170
        adjusted_weight = get_adjusted_weight(actual_weight, height)

        # Adjusted weight must be less than actual
        assert adjusted_weight < actual_weight

        # Must remain realistic (not negative or too small)
        assert adjusted_weight > 50

    def test_height_safety_check(self):
        """
        If height is too small (< 50 cm), returns weight unchanged.

        This prevents division by zero or absurd values.
        """
        weight = 80
        absurd_height = 30  # Impossible
        result = get_adjusted_weight(weight, absurd_height)
        assert result == weight


# ============================================================================
# BMR CALCULATION TESTS (Basal Metabolic Rate)
# ============================================================================

class TestCalculateBMR:
    """Tests the Harris-Benedict formula for BMR."""

    def test_bmr_male_typical(self):
        """
        Typical male: 80 kg, 180 cm, 35 years old.
        Expected: ~1700 kcal (approximate range)
        """
        bmr = calculate_bmr("H", 80, 180, 35)

        # Range allows for small rounding variations
        assert 1650 < bmr < 1750

    def test_bmr_female_typical(self):
        """
        Typical female: 65 kg, 165 cm, 35 years old.
        Expected: ~1400 kcal (approximate range)
        """
        bmr = calculate_bmr("M", 65, 165, 35)

        assert 1350 < bmr < 1450

    def test_bmr_men_higher_than_women(self):
        """Men burn more calories at rest than women with same weight/height."""
        bmr_m = calculate_bmr("H", 75, 170, 30)
        bmr_w = calculate_bmr("M", 75, 170, 30)

        assert bmr_m > bmr_w

    def test_bmr_increases_with_weight(self):
        """Higher weight means higher BMR (more mass requires more energy)."""
        bmr_light = calculate_bmr("H", 60, 180, 30)
        bmr_heavy = calculate_bmr("H", 100, 180, 30)

        assert bmr_heavy > bmr_light

    def test_bmr_decreases_with_age(self):
        """Metabolism decreases with age."""
        bmr_young = calculate_bmr("H", 80, 180, 25)
        bmr_old = calculate_bmr("H", 80, 180, 65)

        assert bmr_young > bmr_old


# ============================================================================
# TDEE CALCULATION TESTS (Total Daily Energy Expenditure)
# ============================================================================

class TestCalculateTDEE:
    """Tests the total daily energy expenditure calculation."""

    def test_tdee_basic_calculation(self):
        """
        TDEE = (BMR * activity_factor) - age_reduction

        If BMR=1800, factor=1.55, reduction=100
        Expected: (1800 * 1.55) - 100 = 2790 - 100 = 2690
        """
        bmr = 1800
        factor = 1.55
        reduction = 100

        tdee = calculate_tdee(bmr, factor, reduction)

        assert tdee == 2690

    def test_tdee_no_reduction_for_young(self):
        """Young person without age reduction."""
        bmr = 1600
        factor = 1.55
        reduction = 0  # Young < 40 years

        tdee = calculate_tdee(bmr, factor, reduction)

        assert tdee == 1600 * 1.55

    def test_tdee_with_max_reduction(self):
        """Older person with maximum reduction."""
        bmr = 1500
        factor = 1.2  # Sedentary
        reduction = 500  # Age 80+

        tdee = calculate_tdee(bmr, factor, reduction)

        assert tdee == (1500 * 1.2) - 500


# ============================================================================
# INTEGRATION TESTS (Complete Flow)
# ============================================================================

class TestIntegration:
    """Tests that all functions work together correctly."""

    def test_complete_calculation_flow_normal_person(self):
        """
        Complete flow for a normal person:
        - Male, 80 kg, 180 cm, 35 years old, activity level 3
        """
        # Arrange
        gender = "H"
        weight = 80
        height = 180
        age = 35
        activity = 3

        # Act
        adjusted_weight = get_adjusted_weight(weight, height)
        age_reduction = get_age_reduction(age)
        activity_factor = get_activity_factor(activity)
        bmr = calculate_bmr(gender, adjusted_weight, height, age)
        tdee = calculate_tdee(bmr, activity_factor, age_reduction)

        # Assert
        assert adjusted_weight == weight  # No adjustment for normal BMI
        assert age_reduction == 0  # Less than 40
        assert activity_factor == 1.55
        assert tdee > 2000  # Must be realistic
        assert tdee < 3000

    def test_complete_calculation_flow_obese_person(self):
        """
        Complete flow for an obese person:
        - Female, 110 kg, 165 cm, 55 years old, activity level 2
        """
        # Arrange
        gender = "M"
        weight = 110
        height = 165
        age = 55
        activity = 2

        # Act
        adjusted_weight = get_adjusted_weight(weight, height)
        age_reduction = get_age_reduction(age)
        activity_factor = get_activity_factor(activity)
        bmr = calculate_bmr(gender, adjusted_weight, height, age)
        tdee = calculate_tdee(bmr, activity_factor, age_reduction)

        # Assert
        assert adjusted_weight < weight  # Adjusted for BMI >= 30
        assert age_reduction == 200  # Age 50-59
        assert activity_factor == 1.375
        assert tdee > 1500
        assert tdee < 2500
```

**Why do I use classes (class TestAgeReduction)?**

Classes group related tests together. It's like organizing with mental folders:
- All age tests together
- All activity tests together
- All BMR tests together

This makes the code easier to navigate when you have many tests.

---

## API Tests

Now create `test/test_api.py`:

```python
"""
Tests for FastAPI endpoints.

These tests verify that:
1. Endpoints respond correctly
2. Input validation works
3. Errors are returned in the correct format
"""

import pytest
from fastapi.testclient import TestClient
from app.api import app


# Create a test client that simulates HTTP requests
client = TestClient(app)


# ============================================================================
# BASIC ENDPOINT TESTS
# ============================================================================

class TestHealthCheck:
    """Tests for the API health check endpoint."""

    def test_home_endpoint_returns_200(self):
        """The GET / endpoint should respond with 200 OK."""
        response = client.get("/")

        assert response.status_code == 200

    def test_home_endpoint_has_message(self):
        """The GET / endpoint should return a message."""
        response = client.get("/")
        data = response.json()

        assert "message" in data


# ============================================================================
# CALCULATE ENDPOINT WITH VALID INPUT
# ============================================================================

class TestCalculateValidInput:
    """Tests that the /calculate endpoint accepts valid input."""

    def test_calculate_with_all_fields_valid(self):
        """
        Basic test: send all correct fields.

        This is the "happy path" - when everything is fine.
        """
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        # Verify response was successful
        assert response.status_code == 200

        data = response.json()

        # Verify it returns success
        assert data["status"] == "success"

        # Verify it has all expected fields
        assert "total_calorias_diarias" in data
        assert "calorias_en_reposo" in data
        assert "peso_utilizado_kg" in data
        assert "kcal_actividad" in data

    def test_calculate_with_float_decimals(self):
        """Should accept decimals with period."""
        response = client.post("/calculate", json={
            "sexo": "M",
            "peso": 65.5,
            "altura": 165.3,
            "edad": 30,
            "nivel_actividad": 2
        })

        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_calculate_with_string_comma_decimals(self):
        """Should accept decimals with comma (Spanish format)."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": "80,5",           # String with comma
            "altura": "180,2",        # String with comma
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_calculate_with_string_numbers(self):
        """Should accept numbers as strings."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": "75",             # String without decimals
            "altura": "175",
            "edad": "28",
            "nivel_actividad": "3"
        })

        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_calculate_both_genders(self):
        """Should work for both males and females."""
        # Male
        response_h = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })
        assert response_h.json()["status"] == "success"

        # Female
        response_m = client.post("/calculate", json={
            "sexo": "M",
            "peso": 65,
            "altura": 165,
            "edad": 35,
            "nivel_actividad": 3
        })
        assert response_m.json()["status"] == "success"

        # Results should be different (men burn more)
        tdee_h = response_h.json()["total_calorias_diarias"]
        tdee_m = response_m.json()["total_calorias_diarias"]
        assert tdee_h > tdee_m

    def test_calculate_all_activity_levels(self):
        """Should accept activity levels 1-5."""
        for activity in range(1, 6):
            response = client.post("/calculate", json={
                "sexo": "H",
                "peso": 80,
                "altura": 180,
                "edad": 35,
                "nivel_actividad": activity
            })
            assert response.status_code == 200
            assert response.json()["status"] == "success"


# ============================================================================
# VALIDATION TESTS (INVALID INPUT)
# ============================================================================

class TestCalculateValidation:
    """Tests that validation rejects invalid input."""

    def test_invalid_gender(self):
        """
        Only 'H' or 'M' are allowed.

        Any other value should return an error.
        """
        response = client.post("/calculate", json={
            "sexo": "X",  # Invalid
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_invalid_gender_lowercase(self):
        """Should automatically convert to uppercase."""
        response = client.post("/calculate", json={
            "sexo": "h",  # Lowercase, should convert to "H"
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_age_too_young(self):
        """
        Calculator is only for adults (18+).

        Minors should be rejected.
        """
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 17,  # Under 18
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"
        assert "adult" in data["message"].lower()

    def test_activity_out_of_range_too_low(self):
        """Activity less than 1 should be rejected."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 0  # Invalid
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_activity_out_of_range_too_high(self):
        """Activity greater than 5 should be rejected."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 10  # Invalid
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_activity_with_decimal(self):
        """
        Activity should NOT accept decimals.

        "1.5" is invalid because it should be "1" or "2", not in between.
        """
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": "1.5"  # Invalid
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_invalid_peso_non_numeric(self):
        """Weight with letters should be rejected."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": "eighty",  # Non-numeric
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_invalid_height_non_numeric(self):
        """Height with letters should be rejected."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": "tall",  # Non-numeric
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_invalid_age_non_numeric(self):
        """Age with letters should be rejected."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": "thirty",  # Non-numeric
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"


# ============================================================================
# MISSING FIELDS TESTS
# ============================================================================

class TestCalculateMissingFields:
    """Tests that requests with missing fields are rejected."""

    def test_missing_sexo(self):
        """If 'sexo' is missing, should return 422."""
        response = client.post("/calculate", json={
            # "sexo": "H",  # MISSING
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 422

    def test_missing_peso(self):
        """If 'peso' is missing, should return 422."""
        response = client.post("/calculate", json={
            "sexo": "H",
            # "peso": 80,  # MISSING
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 422

    def test_missing_altura(self):
        """If 'altura' is missing, should return 422."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            # "altura": 180,  # MISSING
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 422

    def test_missing_edad(self):
        """If 'edad' is missing, should return 422."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            # "edad": 35,  # MISSING
            "nivel_actividad": 3
        })

        assert response.status_code == 422

    def test_missing_nivel_actividad(self):
        """If 'nivel_actividad' is missing, should return 422."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35
            # "nivel_actividad": 3  # MISSING
        })

        assert response.status_code == 422


# ============================================================================
# SPECIAL CASES
# ============================================================================

class TestCalculateSpecialCases:
    """Tests special cases and edge cases."""

    def test_obese_person_weight_adjustment(self):
        """
        Obese person should have weight adjusted.

        Response should show "peso_utilizado_kg" less than what was sent.
        """
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 150,  # Very high BMI
            "altura": 170,
            "edad": 45,
            "nivel_actividad": 2
        })

        assert response.status_code == 200
        data = response.json()

        # Used weight must be less than actual
        assert data["peso_utilizado_kg"] < 150

    def test_supplementation_warning_appears(self):
        """
        If TDEE < 1800 and weight is adjusted, warning should appear.

        This protects the user from malnutrition.
        """
        response = client.post("/calculate", json={
            "sexo": "M",
            "peso": 120,  # Obese
            "altura": 150,  # Short
            "edad": 60,
            "nivel_actividad": 1  # Sedentary
        })

        assert response.status_code == 200
        data = response.json()

        # Check for supplementation warning
        if data["suplementacion_requerida"]:
            assert len(data["aviso_suplementacion"]) > 0

    def test_response_format_includes_disclaimers(self):
        """Response should always include legal disclaimers."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        data = response.json()

        assert "aviso_legal" in data
        assert "recomendacion" in data
        assert len(data["aviso_legal"]) > 0


# ============================================================================
# DEBUGGING TIPS
# ============================================================================

def test_debug_example():
    """
    Example of how to debug a test you don't understand.

    Uncomment print() to see values during execution.
    Run with: pytest -s
    """
    response = client.post("/calculate", json={
        "sexo": "H",
        "peso": 80,
        "altura": 180,
        "edad": 35,
        "nivel_actividad": 3
    })

    # print(f"Status: {response.status_code}")
    # print(f"Response: {response.json()}")

    assert response.status_code == 200
```

---

## Running Tests

### Run Everything

```bash
# All tests (recommended)
pytest

# With more detailed output
pytest -v

# Showing prints
pytest -s
```

### Run Specific Tests

```bash
# Only calculation tests
pytest test/test_calculations.py

# A specific class
pytest test/test_calculations.py::TestAgeReduction

# A specific function
pytest test/test_calculations.py::TestAgeReduction::test_age_under_40_no_reduction

# Only API tests
pytest test/test_api.py

# Tests matching a pattern
pytest -k "age_reduction"  # Everything with "age_reduction"
```

### View Coverage

```bash
# What percentage of code is being tested
pytest --cov=app

# HTML report (opens htmlcov/index.html)
pytest --cov=app --cov-report=html
```

### Useful Options

```bash
# Stop at first error
pytest -x

# Run only tests that failed last time
pytest --lf

# Show the 3 slowest tests
pytest --durations=3

# Interactive debugger on failures
pytest --pdb
```

---

## Best Practices

### ✅ DO's (Do this)

**1. Descriptive names**
```python
# ✅ GOOD - It's clear what's being tested
def test_age_reduction_40_to_50_returns_100():
    pass

# ❌ BAD - Too generic
def test_age_reduction():
    pass
```

**2. One assertion per test (ideally)**
```python
# ✅ GOOD
def test_activity_factor_1_is_1_2():
    assert get_activity_factor(1) == 1.2

def test_activity_factor_5_is_1_9():
    assert get_activity_factor(5) == 1.9

# ❌ AVOID - Multiple unrelated assertions
def test_activity_factors():
    assert get_activity_factor(1) == 1.2
    assert get_activity_factor(2) == 1.375
    assert get_activity_factor(3) == 1.55
    # If the third fails, we never know if 1 and 2 passed
```

**3. Explanatory docstrings**
```python
# ✅ GOOD
def test_bmi_obese_adjustment():
    """
    Verify weight adjustment for BMI >= 30.

    Input: 100kg, 170cm (BMI 34.5)
    Expected: Adjusted weight < 100kg
    """
    pass

# ❌ BAD - No explanation
def test_weight():
    pass
```

**4. Realistic values**
```python
# ✅ GOOD - Data that exists in real life
def test_normal_person():
    response = client.post("/calculate", json={
        "sexo": "H",
        "peso": 80,
        "altura": 180,
        "edad": 35,
        "nivel_actividad": 3
    })

# ❌ AVOID - Absurd values
def test_weird_person():
    response = client.post("/calculate", json={
        "sexo": "H",
        "peso": 999999,  # Impossible
        "altura": 5,      # Impossible
        "edad": 35,
        "nivel_actividad": 3
    })
```

**5. AAA Pattern (Arrange-Act-Assert)**
```python
# ✅ GOOD - Clear structure
def test_example():
    # ARRANGE
    age = 45

    # ACT
    result = get_age_reduction(age)

    # ASSERT
    assert result == 100
```

### ❌ DON'Ts (Don't do this)

**1. Tests that depend on each other**
```python
# ❌ BAD - Test 2 depends on Test 1
def test_1_create_user():
    global user_id
    user_id = create_user("John")

def test_2_get_user():
    user = get_user(user_id)  # What if test_1 fails?
```

**2. Tests that are too large**
```python
# ❌ BAD - Too much for one test
def test_everything():
    # ... 100 lines of code ...
    pass

# ✅ GOOD - Small and focused
def test_age_validation():
    pass

def test_weight_validation():
    pass

def test_calculation_accuracy():
    pass
```

**3. Hardcoding magic values**
```python
# ❌ BAD - Why 24.82?
def test_weight_adjustment():
    adjusted = get_adjusted_weight(100, 170)
    assert adjusted == 24.82

# ✅ GOOD - With descriptive name
def test_weight_adjustment():
    EXPECTED_ADJUSTED_WEIGHT = 24.82
    adjusted = get_adjusted_weight(100, 170)
    assert adjusted == EXPECTED_ADJUSTED_WEIGHT
```

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"

**Cause**: Pytest can't find your `app` module.

**Solution**:
```bash
# Run from project root, not from test/
cd nutrition_calculator
pytest

# Or specify the path
pytest test/test_api.py
```

### Error: "ImportError: cannot import name 'get_age_reduction'"

**Cause**: The function doesn't exist or the name is misspelled.

**Solution**:
```bash
# Check that it exists in calculations.py
grep "def get_age_reduction" app/calculations.py

# Check that you imported correctly
# from app.calculations import get_age_reduction
```

### Tests pass locally but fail in CI/CD

**Cause**: Environment differences (library versions).

**Solution**:
```bash
# Update requirements.txt with exact versions
pip freeze > requirements.txt

# Or use a separate testing file
requirements-test.txt
```

### "AssertionError: assert 1700.5 == 1700"

**Cause**: Rounding errors in float calculations.

**Solution**:
```python
# ❌ BAD - Exact comparison
assert bmr == 1700

# ✅ GOOD - Allows small variation
assert 1650 < bmr < 1750

# Or use pytest.approx
assert bmr == pytest.approx(1700, abs=50)
```

---

## Next Steps

1. **Create the files**:
   ```bash
   touch test/__init__.py
   touch test/test_calculations.py
   touch test/test_api.py
   ```

2. **Copy the tests** from this guide to those files

3. **Run**:
   ```bash
   pytest -v
   ```

4. **Review failures**: Which tests are failing? Why?

5. **Iterate**: Add more tests as needed

---

## Key Concepts Summary

| Concept | What it is | Why it matters |
|---------|-----------|-----------------|
| **Unit Test** | Test of a single function | Detects bugs quickly and in isolation |
| **Fixture** | Reusable test data | DRY (Don't Repeat Yourself) |
| **Mock** | Simulating behavior | Test without external dependencies |
| **Coverage** | % of code tested | Measure test quality |
| **CI/CD** | Automatic tests on each push | Prevent bugs before production |

---

## FAQ

**Q: Do I have to test everything?**
A: No, focus on critical logic (calculations, validation). Don't test trivial code (simple getters/setters).

**Q: Is my test too specific?**
A: It's better to be specific than generic. Specific tests are easier to debug.

**Q: What do I do if I don't understand the error?**
A: Read pytest errors from top to bottom. Run with `-s` to see prints. Use `pytest --pdb` to debug interactively.

**Q: Do tests slow down my project?**
A: Initially yes (you write more code). But they save time later by catching bugs early.

**Q: How many tests should I write?**
A: Coverage: 70%+ is good, 90%+ is excellent. Start with the most important cases.

---

## Resources

If you have questions:
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python Unit Testing](https://docs.python.org/3/library/unittest.html)

---

**Written with professional quality standards. You now have everything you need to write professional tests. Let's go! 🚀**
