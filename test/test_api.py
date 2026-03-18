import pytest
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_health_check():
    """Test del endpoint GET / - Verificar que la API está viva"""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Dietaneo" in data["message"]


def test_calculate_valid_input():
    """Test del endpoint POST /calculate - Datos válidos"""
    payload = {
        "sexo": "M",
        "peso": 60,
        "altura": 165,
        "edad": 30,
        "nivel_actividad": 3
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "encabezado" in data
    assert "total_calorias_diarias" in data
    assert "calorias_en_reposo" in data
    tdee = data["total_calorias_diarias"]
    assert 1200 < tdee < 3000


def test_calculate_invalid_gender():
    """Test POST /calculate - Género inválido"""
    payload = {
        "sexo": "X",
        "peso": 75,
        "altura": 180,
        "edad": 30,
        "nivel_actividad": 3
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "sexo" in data["message"]


def test_calculate_missing_field():
    """Test POST /calculate - Campo obligatorio faltante"""
    payload = {
        "sexo": "H",
        "peso": 75,
        "altura": 180,
        "nivel_actividad": 3
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"
    assert "details" in data
    errors = data["details"]
    assert len(errors) > 0
    assert errors[0]["field"] == "edad"


def test_calculate_age_too_young():
    """Test POST /calculate - Edad menor a 18 años"""
    payload = {
        "sexo": "M",
        "peso": 60,
        "altura": 165,
        "edad": 17,
        "nivel_actividad": 3
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["encabezado"] == "EDAD NO VÁLIDA"
    assert "18+" in data["message"]


def test_calculate_invalid_activity_level():
    """Test POST /calculate - Nivel de actividad fuera del rango 1-5"""
    payload = {
        "sexo": "H",
        "peso": 80,
        "altura": 180,
        "edad": 35,
        "nivel_actividad": 6
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["encabezado"] == "NIVEL DE ACTIVIDAD FUERA DE RANGO"
    assert "1, 2, 3, 4 o 5" in data["message"]


def test_calculate_weight_out_of_range():
    """Test POST /calculate - Peso fuera del rango válido (30-300 kg)"""
    payload = {
        "sexo": "H",
        "peso": 10000,
        "altura": 180,
        "edad": 35,
        "nivel_actividad": 3
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["encabezado"] == "PESO NO VÁLIDO"
    assert "30" in data["message"]
    assert "300" in data["message"]


def test_calculate_height_out_of_range():
    """Test POST /calculate - Altura fuera del rango válido (50-250 cm)"""
    payload = {
        "sexo": "H",
        "peso": 80,
        "altura": 10,
        "edad": 35,
        "nivel_actividad": 3
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["encabezado"] == "ALTURA NO VÁLIDA"
    assert "50" in data["message"]
    assert "250" in data["message"]


def test_calculate_comma_decimal():
    """Test POST /calculate - Aceptar decimales con coma"""
    payload = {
        "sexo": "H",
        "peso": "80,5",
        "altura": "180,5",
        "edad": 35,
        "nivel_actividad": 3
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["peso_utilizado_kg"] == 80.5
    assert 2800 < data["total_calorias_diarias"] < 2900


def test_minimum_calorie_warning():
    """Test POST /calculate - Aviso cuando el TDEE cae por debajo de 1200 kcal/día.

    Caso real: mujer, 77 años, sedentaria, 83 kg, 154 cm.
    Tiene obesidad → se aplica peso corregido.
    La combinación de corrección de peso + edad avanzada + sedentarismo
    produce un TDEE ~1042 kcal, por debajo del mínimo clínico de 1200 kcal.
    """
    payload = {
        "sexo": "M",
        "peso": 83,
        "altura": 154,
        "edad": 77,
        "nivel_actividad": 1
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["total_calorias_diarias"] < 1200
    assert "aviso_minimo_calorico" in data
    assert "1200" in data["aviso_minimo_calorico"]
