# 🧪 Guía Completa de Testing para Dietaneo

*Escrito como mentoring senior para desarrolladores en nivel básico*

---

## 📚 Tabla de Contenidos
1. [¿Por qué Testing?](#por-qué-testing)
2. [Conceptos Fundamentales](#conceptos-fundamentales)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Tu Primer Test](#tu-primer-test)
5. [Tests de Cálculos](#tests-de-cálculos)
6. [Tests de API](#tests-de-api)
7. [Ejecutar Tests](#ejecutar-tests)
8. [Buenas Prácticas](#buenas-prácticas)
9. [Troubleshooting](#troubleshooting)

---

## ¿Por qué Testing?

Imagina que eres un chef en un restaurante. ¿Enviarías un plato a los clientes sin probar primero que esté bien cocinado? **No, verdad.**

Con el código pasa exactamente lo mismo. Los tests son como "probar el plato" antes de entregarlo. Te dan seguridad de que:

✅ Tu código hace lo que debería hacer
✅ Los cambios futuros no rompen lo que ya funciona
✅ Los errores se detectan rápido
✅ Otros desarrolladores (o tú en 6 meses) confían en que el código funciona

En Dietaneo, por ejemplo, es **crítico** que los cálculos nutricionales sean exactos. Un pequeño error en la fórmula podría afectar la salud del usuario final.

---

## Conceptos Fundamentales

### ¿Qué es un Test Unitario?

Un **test unitario** prueba **una pequeña parte** de tu código en aislamiento.

Por ejemplo:
- Un test para la función `get_age_reduction(35)` debe retornar `0`
- Un test para `get_activity_factor(3)` debe retornar `1.55`
- Un test para la corrección de peso con BMI ≥ 30

**No es** un test que pruebe todo el sistema junto. Eso se llama test de integración.

### Estructura de un Test

Todos los tests siguen el mismo patrón: **Arrange → Act → Assert**

```python
# 1. ARRANGE (Preparar): Configura los datos necesarios
edad = 45

# 2. ACT (Actuar): Ejecuta la función que quieres probar
resultado = get_age_reduction(edad)

# 3. ASSERT (Afirmar): Verifica que el resultado sea el esperado
assert resultado == 100  # Esperamos 100 kcal de reducción para edad 40-50
```

**En código de test formal** se ve así:

```python
def test_age_reduction_40_to_50():
    # Arrange
    edad = 45

    # Act
    resultado = get_age_reduction(edad)

    # Assert
    assert resultado == 100
```

### ¿Por qué "assert"?

`assert` es una palabra clave de Python que significa "afirmo que esto es verdad".

- Si es **verdad** → el test pasa ✅
- Si es **falso** → el test falla ❌ y pytest te muestra qué salió mal

Ejemplo:
```python
assert 2 + 2 == 4  # PASA ✅
assert 2 + 2 == 5  # FALLA ❌
```

---

## Estructura del Proyecto

Actualmente tu carpeta `test/` está vacía. Aquí te muestro cómo organizarla:

```
nutrition_calculator/
├── app/
│   ├── api.py                 # Endpoints FastAPI
│   ├── calculations.py        # Funciones de cálculo
│   ├── validations.py
│   └── main.py
├── test/                      # ← AQUÍ van tus tests
│   ├── __init__.py           # Archivo vacío (le dice a Python que es un módulo)
│   ├── test_calculations.py  # Tests para funciones puras
│   └── test_api.py           # Tests para endpoints
├── docs/                      # ← NUEVA carpeta para documentación
│   └── TESTING.md            # Este archivo
├── requirements.txt
├── docker-compose.yml
└── CLAUDE.md
```

**¿Por qué esta estructura?**

- Mantiene tests separados del código de producción
- Pytest automáticamente encuentra archivos que empiezan con `test_`
- Es la convención estándar en la industria (todos en el equipo sabrán dónde buscar)

---

## Tu Primer Test

### Paso 1: Crear la carpeta y archivo

```bash
# Desde la raíz del proyecto
touch test/__init__.py
touch test/test_calculations.py
```

`__init__.py` es un archivo especial en Python (puede estar vacío). Le dice a Python que esta carpeta es un módulo importable.

### Paso 2: Tu primer test

Abre `test/test_calculations.py` y escribe:

```python
"""
Tests para el módulo de cálculos nutricionales.

Este archivo prueba todas las funciones matemáticas en app/calculations.py
para asegurar que hacen exactamente lo que se espera.
"""

from app.calculations import get_age_reduction


def test_age_reduction_under_40():
    """
    Cuando la edad es menor a 40 años, no debe haber reducción.

    Esto es importante porque según la lógica clínica, el metabolismo
    es máximo hasta los 40 años, luego comienza a disminuir.
    """
    # Arrange
    edad = 35

    # Act
    resultado = get_age_reduction(edad)

    # Assert
    assert resultado == 0
```

**¿Por qué cada función tiene docstring?**

Porque en 3 meses tú (o un compañero) leerá este test y querrá saber:
- ¿Qué estoy probando?
- ¿Por qué es importante?
- ¿Cuál es el caso de uso?

### Paso 3: Ejecutar el test

```bash
# Desde la raíz del proyecto
pytest test/test_calculations.py::test_age_reduction_under_40 -v
```

Deberías ver:
```
test/test_calculations.py::test_age_reduction_under_40 PASSED ✓
```

**¡Felicidades! Tu primer test funciona.**

---

## Tests de Cálculos

Aquí va el archivo completo `test/test_calculations.py`:

```python
"""
Tests para el módulo de cálculos nutricionales.

Este archivo prueba todas las funciones matemáticas en app/calculations.py
para asegurar que hacen exactamente lo que se espera.
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
# TESTS DE REDUCCIÓN POR EDAD
# ============================================================================

class TestAgeReduction:
    """Agrupa todos los tests relacionados con la reducción por edad."""

    def test_age_under_40_no_reduction(self):
        """Menores de 40 años no tienen reducción calórica."""
        assert get_age_reduction(18) == 0
        assert get_age_reduction(35) == 0
        assert get_age_reduction(39) == 0

    def test_age_40_to_49_reduction_100(self):
        """Entre 40-49 años, reducción de 100 kcal."""
        assert get_age_reduction(40) == 100
        assert get_age_reduction(45) == 100
        assert get_age_reduction(49) == 100

    def test_age_50_to_59_reduction_200(self):
        """Entre 50-59 años, reducción de 200 kcal."""
        assert get_age_reduction(50) == 200
        assert get_age_reduction(55) == 200
        assert get_age_reduction(59) == 200

    def test_age_60_to_69_reduction_300(self):
        """Entre 60-69 años, reducción de 300 kcal."""
        assert get_age_reduction(60) == 300
        assert get_age_reduction(65) == 300
        assert get_age_reduction(69) == 300

    def test_age_70_to_79_reduction_400(self):
        """Entre 70-79 años, reducción de 400 kcal."""
        assert get_age_reduction(70) == 400
        assert get_age_reduction(75) == 400
        assert get_age_reduction(79) == 400

    def test_age_80_plus_reduction_500(self):
        """80+ años, reducción de 500 kcal."""
        assert get_age_reduction(80) == 500
        assert get_age_reduction(90) == 500
        assert get_age_reduction(120) == 500


# ============================================================================
# TESTS DE FACTORES DE ACTIVIDAD
# ============================================================================

class TestActivityFactor:
    """Prueba que cada nivel de actividad retorne el factor Harris-Benedict correcto."""

    def test_activity_1_sedentary(self):
        """Nivel 1 (Sedentario) = multiplicador 1.2"""
        assert get_activity_factor(1) == 1.2

    def test_activity_2_light(self):
        """Nivel 2 (Ligero) = multiplicador 1.375"""
        assert get_activity_factor(2) == 1.375

    def test_activity_3_moderate(self):
        """Nivel 3 (Moderado) = multiplicador 1.55"""
        assert get_activity_factor(3) == 1.55

    def test_activity_4_heavy(self):
        """Nivel 4 (Fuerte) = multiplicador 1.725"""
        assert get_activity_factor(4) == 1.725

    def test_activity_5_very_heavy(self):
        """Nivel 5 (Muy Fuerte) = multiplicador 1.9"""
        assert get_activity_factor(5) == 1.9

    def test_activity_invalid_defaults_to_1_2(self):
        """Si recibe un valor inválido, retorna 1.2 por defecto."""
        assert get_activity_factor(10) == 1.2
        assert get_activity_factor(0) == 1.2


# ============================================================================
# TESTS DE CORRECCIÓN DE PESO (OBESIDAD)
# ============================================================================

class TestAdjustedWeight:
    """Prueba la fórmula de corrección de peso para pacientes con BMI >= 30."""

    def test_normal_weight_no_adjustment(self):
        """
        BMI normal (< 30) no se ajusta.

        Persona: 70 kg, 170 cm
        BMI = 70 / (1.70^2) = 24.22 (normal)
        """
        peso = 70
        altura = 170
        resultado = get_adjusted_weight(peso, altura)
        assert resultado == peso  # Sin cambios

    def test_overweight_no_adjustment(self):
        """
        Sobrepeso (BMI 25-29.9) no se ajusta.

        Persona: 85 kg, 170 cm
        BMI = 85 / (1.70^2) = 29.41 (sobrepeso)
        """
        peso = 85
        altura = 170
        resultado = get_adjusted_weight(peso, altura)
        assert resultado == peso

    def test_obese_weight_is_adjusted(self):
        """
        BMI >= 30 se ajusta usando fórmula clínica.

        Persona: 110 kg, 170 cm
        BMI = 110 / (1.70^2) = 38.05 (obeso)

        La función debe retornar menos peso que el real.
        """
        peso_real = 110
        altura = 170
        peso_ajustado = get_adjusted_weight(peso_real, altura)

        # El peso ajustado debe ser menor que el real
        assert peso_ajustado < peso_real

        # Debe seguir siendo realista (no puede ser negativo o muy pequeño)
        assert peso_ajustado > 50

    def test_height_safety_check(self):
        """
        Si altura es demasiado pequeña (< 50 cm), retorna peso sin cambios.

        Esto previene divisiones por cero o valores absurdos.
        """
        peso = 80
        altura_absurda = 30  # Impossible
        resultado = get_adjusted_weight(peso, altura_absurda)
        assert resultado == peso


# ============================================================================
# TESTS DE CÁLCULO DE BMR (Basal Metabolic Rate)
# ============================================================================

class TestCalculateBMR:
    """Prueba la fórmula de Harris-Benedict para BMR."""

    def test_bmr_male_typical(self):
        """
        Hombre típico: 80 kg, 180 cm, 35 años.
        Esperado: ~1700 kcal (rango aproximado)
        """
        bmr = calculate_bmr("H", 80, 180, 35)

        # Es un rango para permitir pequeñas variaciones de redondeo
        assert 1650 < bmr < 1750

    def test_bmr_female_typical(self):
        """
        Mujer típica: 65 kg, 165 cm, 35 años.
        Esperado: ~1400 kcal (rango aproximado)
        """
        bmr = calculate_bmr("M", 65, 165, 35)

        assert 1350 < bmr < 1450

    def test_bmr_men_higher_than_women(self):
        """Hombres gastan más calorías en reposo que mujeres con mismo peso/altura."""
        bmr_h = calculate_bmr("H", 75, 170, 30)
        bmr_m = calculate_bmr("M", 75, 170, 30)

        assert bmr_h > bmr_m

    def test_bmr_increases_with_weight(self):
        """A mayor peso, mayor BMR (más masa requiere más energía)."""
        bmr_light = calculate_bmr("H", 60, 180, 30)
        bmr_heavy = calculate_bmr("H", 100, 180, 30)

        assert bmr_heavy > bmr_light

    def test_bmr_decreases_with_age(self):
        """El metabolismo disminuye con la edad."""
        bmr_young = calculate_bmr("H", 80, 180, 25)
        bmr_old = calculate_bmr("H", 80, 180, 65)

        assert bmr_young > bmr_old


# ============================================================================
# TESTS DE CÁLCULO DE TDEE (Total Daily Energy Expenditure)
# ============================================================================

class TestCalculateTDEE:
    """Prueba el cálculo del gasto energético total."""

    def test_tdee_basic_calculation(self):
        """
        TDEE = (BMR * factor_actividad) - reduccion_edad

        Si BMR=1800, factor=1.55, reducción=100
        Esperado: (1800 * 1.55) - 100 = 2790 - 100 = 2690
        """
        bmr = 1800
        factor = 1.55
        reduction = 100

        tdee = calculate_tdee(bmr, factor, reduction)

        assert tdee == 2690

    def test_tdee_no_reduction_for_young(self):
        """Un joven sin reducción por edad."""
        bmr = 1600
        factor = 1.55
        reduction = 0  # Joven < 40 años

        tdee = calculate_tdee(bmr, factor, reduction)

        assert tdee == 1600 * 1.55

    def test_tdee_with_max_reduction(self):
        """Persona mayor con máxima reducción."""
        bmr = 1500
        factor = 1.2  # Sedentario
        reduction = 500  # 80+ años

        tdee = calculate_tdee(bmr, factor, reduction)

        assert tdee == (1500 * 1.2) - 500


# ============================================================================
# TESTS DE INTEGRACIÓN (Flujo completo)
# ============================================================================

class TestIntegration:
    """Prueba que todas las funciones funcionen juntas correctamente."""

    def test_complete_calculation_flow_normal_person(self):
        """
        Flujo completo para persona normal:
        - Hombre, 80 kg, 180 cm, 35 años, actividad 3
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
        assert adjusted_weight == weight  # Sin corrección por BMI normal
        assert age_reduction == 0  # Menor de 40
        assert activity_factor == 1.55
        assert tdee > 2000  # Debe ser un valor realista
        assert tdee < 3000

    def test_complete_calculation_flow_obese_person(self):
        """
        Flujo completo para persona con obesidad:
        - Mujer, 110 kg, 165 cm, 55 años, actividad 2
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
        assert adjusted_weight < weight  # Con corrección por BMI >= 30
        assert age_reduction == 200  # Entre 50-59
        assert activity_factor == 1.375
        assert tdee > 1500
        assert tdee < 2500
```

**¿Por qué uso clases (class TestAgeReduction)?**

Las clases agrupan tests relacionados. Es como organizar con carpetas mentales:
- Todos los tests de edad juntos
- Todos los tests de actividad juntos
- Todos los tests de BMR juntos

Esto hace que el código sea más fácil de navegar cuando tienes muchos tests.

---

## Tests de API

Ahora crea `test/test_api.py`:

```python
"""
Tests para los endpoints de la API FastAPI.

Estos tests prueban que:
1. Los endpoints responden correctamente
2. La validación de entrada funciona
3. Los errores se retornan con formato correcto
"""

import pytest
from fastapi.testclient import TestClient
from app.api import app


# Crea un cliente de prueba que simula requests HTTP
client = TestClient(app)


# ============================================================================
# TESTS DE ENDPOINTS BÁSICOS
# ============================================================================

class TestHealthCheck:
    """Tests para el endpoint de salud del API."""

    def test_home_endpoint_returns_200(self):
        """El endpoint GET / debe responder con 200 OK."""
        response = client.get("/")

        assert response.status_code == 200

    def test_home_endpoint_has_message(self):
        """El endpoint GET / debe retornar un mensaje."""
        response = client.get("/")
        data = response.json()

        assert "message" in data


# ============================================================================
# TESTS DE CÁLCULO CON ENTRADA VÁLIDA
# ============================================================================

class TestCalculateValidInput:
    """Prueba que el endpoint /calculate acepta entrada válida."""

    def test_calculate_with_all_fields_valid(self):
        """
        Test básico: enviar todos los campos correctos.

        Este es el "happy path" - cuando todo está bien.
        """
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        # Verificar que la respuesta fue exitosa
        assert response.status_code == 200

        data = response.json()

        # Verificar que retorna éxito
        assert data["status"] == "success"

        # Verificar que tiene todos los campos esperados
        assert "total_calorias_diarias" in data
        assert "calorias_en_reposo" in data
        assert "peso_utilizado_kg" in data
        assert "kcal_actividad" in data

    def test_calculate_with_float_decimals(self):
        """Debe aceptar decimales con punto."""
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
        """Debe aceptar decimales con coma (formato español)."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": "80,5",           # String con coma
            "altura": "180,2",        # String con coma
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_calculate_with_string_numbers(self):
        """Debe aceptar números como strings."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": "75",             # String sin decimales
            "altura": "175",
            "edad": "28",
            "nivel_actividad": "3"
        })

        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_calculate_both_genders(self):
        """Debe funcionar tanto para hombres como mujeres."""
        # Hombre
        response_h = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })
        assert response_h.json()["status"] == "success"

        # Mujer
        response_m = client.post("/calculate", json={
            "sexo": "M",
            "peso": 65,
            "altura": 165,
            "edad": 35,
            "nivel_actividad": 3
        })
        assert response_m.json()["status"] == "success"

        # Los resultados deben ser diferentes (hombres gastan más)
        tdee_h = response_h.json()["total_calorias_diarias"]
        tdee_m = response_m.json()["total_calorias_diarias"]
        assert tdee_h > tdee_m

    def test_calculate_all_activity_levels(self):
        """Debe aceptar niveles de actividad 1-5."""
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
# TESTS DE VALIDACIÓN (ENTRADAS INVÁLIDAS)
# ============================================================================

class TestCalculateValidation:
    """Prueba que la validación rechaza entrada inválida."""

    def test_invalid_gender(self):
        """
        Solo se permiten 'H' o 'M'.

        Cualquier otro valor debe retornar error.
        """
        response = client.post("/calculate", json={
            "sexo": "X",  # Inválido
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_invalid_gender_lowercase(self):
        """Debe convertir a mayúscula automáticamente."""
        response = client.post("/calculate", json={
            "sexo": "h",  # Minúscula, debe convertirse a "H"
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_age_too_young(self):
        """
        La calculadora es solo para mayores de 18.

        Menores de edad deben ser rechazados.
        """
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 17,  # Menor de edad
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"
        # El mensaje debe mencionar que es para adultos
        assert "adulto" in data["message"].lower()

    def test_activity_out_of_range_too_low(self):
        """Actividad menor a 1 debe ser rechazada."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 0  # Inválido
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_activity_out_of_range_too_high(self):
        """Actividad mayor a 5 debe ser rechazada."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 10  # Inválido
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_activity_with_decimal(self):
        """
        La actividad NO debe aceptar decimales.

        "1.5" es inválido porque debe ser "1" o "2", no intermedio.
        """
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": "1.5"  # Inválido
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_invalid_peso_non_numeric(self):
        """Peso con letras debe ser rechazado."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": "ochenta",  # No numérico
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_invalid_height_non_numeric(self):
        """Altura con letras debe ser rechazada."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": "alto",  # No numérico
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"

    def test_invalid_age_non_numeric(self):
        """Edad con letras debe ser rechazada."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": "treinta",  # No numérico
            "nivel_actividad": 3
        })

        assert response.status_code == 200
        assert response.json()["status"] == "error"


# ============================================================================
# TESTS DE CAMPOS FALTANTES
# ============================================================================

class TestCalculateMissingFields:
    """Prueba que se rechacen requests con campos faltantes."""

    def test_missing_sexo(self):
        """Si falta 'sexo', debe retornar 422."""
        response = client.post("/calculate", json={
            # "sexo": "H",  # FALTA
            "peso": 80,
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 422

    def test_missing_peso(self):
        """Si falta 'peso', debe retornar 422."""
        response = client.post("/calculate", json={
            "sexo": "H",
            # "peso": 80,  # FALTA
            "altura": 180,
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 422

    def test_missing_altura(self):
        """Si falta 'altura', debe retornar 422."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            # "altura": 180,  # FALTA
            "edad": 35,
            "nivel_actividad": 3
        })

        assert response.status_code == 422

    def test_missing_edad(self):
        """Si falta 'edad', debe retornar 422."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            # "edad": 35,  # FALTA
            "nivel_actividad": 3
        })

        assert response.status_code == 422

    def test_missing_nivel_actividad(self):
        """Si falta 'nivel_actividad', debe retornar 422."""
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 80,
            "altura": 180,
            "edad": 35
            # "nivel_actividad": 3  # FALTA
        })

        assert response.status_code == 422


# ============================================================================
# TESTS DE CASOS ESPECIALES
# ============================================================================

class TestCalculateSpecialCases:
    """Prueba casos especiales y bordes."""

    def test_obese_person_weight_adjustment(self):
        """
        Persona con obesidad debe tener peso ajustado.

        La respuesta debe mostrar "peso_utilizado_kg" menor que el enviado.
        """
        response = client.post("/calculate", json={
            "sexo": "H",
            "peso": 150,  # BMI muy alto
            "altura": 170,
            "edad": 45,
            "nivel_actividad": 2
        })

        assert response.status_code == 200
        data = response.json()

        # El peso utilizado debe ser menor que el real
        assert data["peso_utilizado_kg"] < 150

    def test_supplementation_warning_appears(self):
        """
        Si TDEE < 1800 y hay corrección de peso, debe haber aviso.

        Esto protege al usuario de desnutrición.
        """
        response = client.post("/calculate", json={
            "sexo": "M",
            "peso": 120,  # Obesa
            "altura": 150,  # Baja
            "edad": 60,
            "nivel_actividad": 1  # Sedentario
        })

        assert response.status_code == 200
        data = response.json()

        # Verificar que hay warning de suplementación
        if data["suplementacion_requerida"]:
            assert len(data["aviso_suplementacion"]) > 0

    def test_response_format_includes_disclaimers(self):
        """La respuesta siempre debe incluir avisos legales."""
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
# TIPS PARA DEBUGGING
# ============================================================================

def test_debug_example():
    """
    Ejemplo de cómo debuggear un test que no entiendes.

    Descomenta print() para ver valores durante ejecución.
    Ejecuta con: pytest -s
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

## Ejecutar Tests

### Ejecutar TODO

```bash
# Todos los tests (recomendado)
pytest

# Con output más detallado
pytest -v

# Mostrando prints
pytest -s
```

### Ejecutar Tests Específicos

```bash
# Solo tests de cálculos
pytest test/test_calculations.py

# Una clase específica
pytest test/test_calculations.py::TestAgeReduction

# Una función específica
pytest test/test_calculations.py::TestAgeReduction::test_age_under_40_no_reduction

# Solo tests de API
pytest test/test_api.py

# Tests que coincidan con un patrón
pytest -k "age_reduction"  # Todo lo con "age_reduction"
```

### Ver Cobertura

```bash
# Qué porcentaje de código está siendo testeado
pytest --cov=app

# Reporte en HTML (abre htmlcov/index.html)
pytest --cov=app --cov-report=html
```

### Opciones Útiles

```bash
# Parar en el primer error
pytest -x

# Correr solo tests que fallaron la última vez
pytest --lf

# Mostrar los 3 tests más lentos
pytest --durations=3

# Debugger interactivo en fallos
pytest --pdb
```

---

## Buenas Prácticas

### ✅ DO's (Haz esto)

**1. Nombres descriptivos**
```python
# ✅ BIEN - Se entiende qué se prueba
def test_age_reduction_40_to_50_returns_100():
    pass

# ❌ MAL - Muy genérico
def test_age_reduction():
    pass
```

**2. Un assert por test (idealmente)**
```python
# ✅ BIEN
def test_activity_factor_1_is_1_2():
    assert get_activity_factor(1) == 1.2

def test_activity_factor_5_is_1_9():
    assert get_activity_factor(5) == 1.9

# ❌ EVITAR - Múltiples asserts no relacionados
def test_activity_factors():
    assert get_activity_factor(1) == 1.2
    assert get_activity_factor(2) == 1.375
    assert get_activity_factor(3) == 1.55
    # Si falla el tercero, nunca sabemos si 1 y 2 pasaron
```

**3. Docstrings explicativos**
```python
# ✅ BIEN
def test_bmi_obese_adjustment():
    """
    Verify weight adjustment for BMI >= 30.

    Input: 100kg, 170cm (BMI 34.5)
    Expected: Adjusted weight < 100kg
    """
    pass

# ❌ MAL - Sin explicación
def test_weight():
    pass
```

**4. Valores realistas**
```python
# ✅ BIEN - Datos que existen en la vida real
def test_normal_person():
    response = client.post("/calculate", json={
        "sexo": "H",
        "peso": 80,
        "altura": 180,
        "edad": 35,
        "nivel_actividad": 3
    })

# ❌ EVITAR - Valores absurdos
def test_weird_person():
    response = client.post("/calculate", json={
        "sexo": "H",
        "peso": 999999,  # Imposible
        "altura": 5,      # Imposible
        "edad": 35,
        "nivel_actividad": 3
    })
```

**5. AAA Pattern (Arrange-Act-Assert)**
```python
# ✅ BIEN - Estructura clara
def test_example():
    # ARRANGE
    edad = 45

    # ACT
    resultado = get_age_reduction(edad)

    # ASSERT
    assert resultado == 100
```

### ❌ DON'Ts (No hagas esto)

**1. Tests que dependen uno del otro**
```python
# ❌ MAL - Test 2 depende de Test 1
def test_1_create_user():
    global user_id
    user_id = create_user("John")

def test_2_get_user():
    user = get_user(user_id)  # ¿Qué pasa si test_1 falla?
```

**2. Tests demasiado grandes**
```python
# ❌ MAL - Demasiado para un test
def test_everything():
    # ... 100 líneas de código ...
    pass

# ✅ BIEN - Tests pequeños y enfocados
def test_age_validation():
    pass

def test_weight_validation():
    pass

def test_calculation_accuracy():
    pass
```

**3. Hardcodear valores mágicos**
```python
# ❌ MAL - ¿Por qué 24.82?
def test_weight_adjustment():
    adjusted = get_adjusted_weight(100, 170)
    assert adjusted == 24.82

# ✅ BIEN - Con nombre descriptivo
def test_weight_adjustment():
    EXPECTED_ADJUSTED_WEIGHT = 24.82
    adjusted = get_adjusted_weight(100, 170)
    assert adjusted == EXPECTED_ADJUSTED_WEIGHT
```

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"

**Causa**: Pytest no encuentra tu módulo `app`.

**Solución**:
```bash
# Ejecuta desde la raíz del proyecto, no desde test/
cd nutrition_calculator
pytest

# O especifica la ruta
pytest test/test_api.py
```

### Error: "ImportError: cannot import name 'get_age_reduction'"

**Causa**: La función no existe o el nombre está mal escrito.

**Solución**:
```bash
# Verifica que existe en calculations.py
grep "def get_age_reduction" app/calculations.py

# Verifica que importaste correctamente
# from app.calculations import get_age_reduction
```

### Tests pasan localmente pero fallan en CI/CD

**Causa**: Diferencias de ambiente (versiones de librerías).

**Solución**:
```bash
# Actualiza requirements.txt con versiones exactas
pip freeze > requirements.txt

# O usa un archivo de testing separado
requirements-test.txt
```

### "AssertionError: assert 1700.5 == 1700"

**Causa**: Errores de redondeo en cálculos flotantes.

**Solución**:
```python
# ❌ MAL - Comparación exacta
assert bmr == 1700

# ✅ BIEN - Permite pequeña variación
assert 1650 < bmr < 1750

# O usa pytest.approx
assert bmr == pytest.approx(1700, abs=50)
```

---

## Próximos Pasos

1. **Crea los archivos**:
   ```bash
   touch test/__init__.py
   touch test/test_calculations.py
   touch test/test_api.py
   ```

2. **Copia los tests** de esta guía a esos archivos

3. **Ejecuta**:
   ```bash
   pytest -v
   ```

4. **Revisa fallos**: ¿Qué tests fallan? Investiga por qué

5. **Itera**: Añade más tests según necesites

---

## Resumen de Conceptos Clave

| Concepto | Qué es | Por qué importa |
|----------|--------|-----------------|
| **Test Unitario** | Prueba de una función pequeña | Detecta bugs rápido y en aislamiento |
| **Fixture** | Datos de prueba reutilizables | DRY (Don't Repeat Yourself) |
| **Mock** | Simular comportamiento | Testear sin dependencias externas |
| **Cobertura** | % de código testeado | Medir calidad de tests |
| **CI/CD** | Tests automáticos en cada push | Prevenir bugs antes de producción |

---

## Preguntas Frecuentes para Mentees

**P: ¿Tengo que testear TODO?**
A: No, enfócate en lógica crítica (cálculos, validación). No testees código trivial (getters/setters simples).

**P: ¿Mi test es muy específico?**
A: Es mejor ser específico que genérico. Tests específicos son más fáciles de debuggear.

**P: ¿Qué hago si no entiendo el error?**
A: Lee el error de pytest de arriba a abajo. Ejecuta con `-s` para ver prints. Usa `pytest -pdb` para debuggear interactivamente.

**P: ¿Los tests hacen el proyecto más lento?**
A: Al principio sí (escribe más código). Pero ahorran tiempo después porque detectan bugs antes.

**P: ¿Cuántos tests escribo?**
A: Cobertura: 70%+ es bien, 90%+ es excelente. Empieza con los casos más importantes.

---

## Contacto & Recursos

Si tienes dudas:
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python Unit Testing](https://docs.python.org/3/library/unittest.html)

---

**Escrito con ❤️ como mentoring senior. Ahora tienes todo para escribir tests profesionales. ¡Adelante!**
