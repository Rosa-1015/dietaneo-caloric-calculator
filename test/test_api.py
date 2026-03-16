import pytest 
from fastapi.testclient import TestClient                                                                                      
from app.api import app                                                                                                        

# Esto es el cliente para hacer peticiones HTTP a nuestro API
client = TestClient(app)


def test_health_check():
    """Test del endpoint GET / - Verificar que la API está viva"""

    # ACT - Hacemos la petición
    response = client.get("/")

    # ASSERT - Verificamos que:
    # 1. El servidor responde con código 200 (OK)
    assert response.status_code == 200

    # 2. La respuesta contiene un mensaje de bienvenida
    data = response.json()
    assert "message" in data
    assert "Dietaneo" in data["message"]


def test_calculate_valid_input():
    """Test del endpoint POST /calculate - Datos válidos"""

    # ARRANGE - Preparamos datos válidos
    payload = {
        "sexo": "M",          # Mujer
        "peso": 60,           # 60 kg
        "altura": 165,        # 165 cm
        "edad": 30,           # 30 años
        "nivel_actividad": 3  # Actividad moderada
    }

    # ACT - Hacemos la petición POST
    response = client.post("/calculate", json=payload)

    # ASSERT - Verificamos que:
    # 1. El servidor responde con 200
    assert response.status_code == 200

    # 2. La respuesta contiene "status: success"
    data = response.json()
    assert data["status"] == "success"

    # 3. Los campos importantes existen
    assert "encabezado" in data
    assert "total_calorias_diarias" in data
    assert "calorias_en_reposo" in data

    # 4. El valor de calorías es un número razonable (entre 1200 y 3000)
    tdee = data["total_calorias_diarias"]
    assert 1200 < tdee < 3000


def test_calculate_invalid_gender():
    """Test POST /calculate - Género inválido"""

    # ARRANGE - Género inválido (debe ser H o M)
    payload = {
        "sexo": "X",              # Inválido
        "peso": 75,
        "altura": 180,
        "edad": 30,
        "nivel_actividad": 3
    }

    # ACT
    response = client.post("/calculate", json=payload)

    # ASSERT
    # 1. El servidor responde con 200 (pero el JSON indica error)
    assert response.status_code == 200

    # 2. La respuesta contiene status: "error"
    data = response.json()
    assert data["status"] == "error"

    # 3. El mensaje explica el problema con el campo sexo
    assert "sexo" in data["message"]


def test_calculate_missing_field():
    """Test POST /calculate - Campo obligatorio faltante"""

    # ARRANGE - Falta el campo "edad"
    payload = {
        "sexo": "H",
        "peso": 75,
        "altura": 180,
        # Falta "edad"
        "nivel_actividad": 3
    }

    # ACT
    response = client.post("/calculate", json=payload)

    # ASSERT
    # 1. El servidor responde con 422 (validación fallida)
    assert response.status_code == 422

    # 2. La respuesta tiene estructura de error
    data = response.json()
    assert data["status"] == "error"
    assert "details" in data  # detalles de error

    # 3. El error especifica qué campo falta
    errors = data["details"]
    assert len(errors) > 0
    assert errors[0]["field"] == "edad"


def test_calculate_age_too_young():
    """Test POST /calculate - Edad menor a 18 años"""

    # ARRANGE - Edad < 18 (no permitida)
    payload = {
        "sexo": "M",
        "peso": 60,
        "altura": 165,
        "edad": 17,              # ❌ Menor de 18
        "nivel_actividad": 3
    }

    # ACT
    response = client.post("/calculate", json=payload)

    # ASSERT
    # 1. El servidor responde con 200
    assert response.status_code == 200

    # 2. El JSON indica error
    data = response.json()
    assert data["status"] == "error"

    # 3. El encabezado es específico para edad
    assert data["encabezado"] == "EDAD NO VÁLIDA"

    # 4. El mensaje explica que es para mayores de 18
    assert "18+" in data["message"]


def test_calculate_invalid_activity_level():
    """Test POST /calculate - Nivel de actividad fuera del rango 1-5"""

    # ARRANGE - Actividad fuera de rango
    payload = {
        "sexo": "H",
        "peso": 80,
        "altura": 180,
        "edad": 35,
        "nivel_actividad": 6     # ❌ Inválido (debe ser 1-5)
    }

    # ACT
    response = client.post("/calculate", json=payload)

    # ASSERT
    # 1. El servidor responde con 200
    assert response.status_code == 200

    # 2. La respuesta indica error
    data = response.json()
    assert data["status"] == "error"

    # 3. El encabezado es específico para actividad
    assert data["encabezado"] == "NIVEL DE ACTIVIDAD FUERA DE RANGO"

    # 4. El mensaje explica el rango válido
    assert "1, 2, 3, 4 o 5" in data["message"]


def test_calculate_negative_weight():
    """Test POST /calculate - Peso negativo (esperamos error)"""

    # ARRANGE - Peso negativo (inválido)
    payload = {
        "sexo": "H",
        "peso": -80,             # ❌ Negativo
        "altura": 180,
        "edad": 35,
        "nivel_actividad": 3
    }

    # ACT
    response = client.post("/calculate", json=payload)

    # ASSERT
    # 1. Status code
    assert response.status_code == 200

    # 2. Indica error
    data = response.json()
    assert data["status"] == "error"

    # 3. Encabezado específico para peso
    assert data["encabezado"] == "PESO INVÁLIDO"

    # 4. Mensaje menciona peso
    assert "peso" in data["message"]


def test_calculate_comma_decimal():
    """Test POST /calculate - Aceptar decimales con coma"""

    # ARRANGE - Usar coma como separador decimal en peso Y altura
    payload = {
        "sexo": "H",
        "peso": "80,5",          # Con coma (80,5 → 80.5)
        "altura": "180,5",       # Con coma (180,5 → 180.5)
        "edad": 35,
        "nivel_actividad": 3
    }

    # ACT
    response = client.post("/calculate", json=payload)

    # ASSERT
    # 1. Status code: 200
    assert response.status_code == 200

    # 2. Respuesta indica éxito
    data = response.json()
    assert data["status"] == "success"

    # 3. El peso se convirtió correctamente (80,5 → 80.5)
    assert data["peso_utilizado_kg"] == 80.5

    # 4. Los cálculos son correctos (dependen de peso Y altura)
    # Si altura no se convirtiera, los cálculos serían muy diferentes
    # Si falla aquí → la altura NO se convirtió correctamente
    assert 2800 < data["total_calorias_diarias"] < 2900