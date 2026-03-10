# Guía de Tests - Dietaneo

Este documento explica cómo correr, entender y escribir tests en el proyecto Dietaneo.

## 🚀 Inicio Rápido

### Correr todos los tests
```bash
pytest
```

### Ver cobertura de código
```bash
pytest --cov=app --cov-report=term-missing
```

### Correr un archivo específico
```bash
pytest test/test_api.py
pytest test/test_calculations.py
```

### Correr un test específico
```bash
pytest test/test_api.py::test_health_check
pytest test/test_calculations.py::test_get_age_reduction
```

### Modo verbose (más detalles)
```bash
pytest -v
```

---

## 📁 Estructura de Tests

```
test/
├── test_api.py           # Tests de integración (endpoints)
└── test_calculations.py  # Tests de funciones puras (cálculos)
```

### Archivos Testeados

| Archivo | Cobertura | Tests |
|---------|-----------|-------|
| `app/api.py` | 87% | 8 (integración) |
| `app/calculations.py` | 97% | 27 (unitarios) |
| **TOTAL** | **87%** | **35 tests** |

---

## 🧪 Descripción de Tests

### `test_api.py` - Tests de Integración (8 tests)

Estos tests verifican que los **endpoints HTTP funcionen correctamente**.

#### 1. `test_health_check()`
- **Qué testea**: GET `/` endpoint
- **Verificaciones**:
  - Status code 200
  - Response contiene `{"status": "ok"}`
- **Por qué**: Asegurar que el servidor está vivo

#### 2. `test_calculate_valid_input()`
- **Qué testea**: POST `/calculate` con datos válidos
- **Verificaciones**:
  - Status code 200
  - Response tiene `status: "success"`
  - Resultado contiene `tdee`, `bmr`, `encabezado`
- **Por qué**: El caso feliz - entrada válida produce resultado

#### 3. `test_calculate_invalid_gender()`
- **Qué testea**: POST `/calculate` con `sexo` inválido
- **Verificaciones**:
  - Status code 422 (error de validación)
  - Response contiene mensaje de error en español
- **Por qué**: Rechazar géneros inválidos

#### 4. `test_calculate_missing_field()`
- **Qué testea**: POST `/calculate` sin campos requeridos
- **Verificaciones**:
  - Status code 422
  - Mensaje de error claro
- **Por qué**: Validar que todos los campos son obligatorios

#### 5. `test_calculate_age_too_young()`
- **Qué testea**: POST `/calculate` con edad < 18
- **Verificaciones**:
  - Status code 422
  - Mensaje de error en español
- **Por qué**: Rechazar menores de edad

#### 6. `test_calculate_invalid_activity_level()`
- **Qué testea**: POST `/calculate` con actividad fuera de 1-5
- **Verificaciones**:
  - Status code 422
- **Por qué**: Actividad debe estar en rango válido

#### 7. `test_calculate_negative_weight()`
- **Qué testea**: POST `/calculate` con peso negativo
- **Verificaciones**:
  - Status code 422
  - Mensaje de error
- **Por qué**: Peso no puede ser negativo

#### 8. `test_calculate_comma_decimal()`
- **Qué testea**: POST `/calculate` con decimales separados por coma
- **Verificaciones**:
  - Status code 200
  - Resultado correcto
- **Por qué**: API acepta comas además de puntos

---

### `test_calculations.py` - Tests Unitarios (27 tests)

Estos tests verifican que las **funciones matemáticas sean correctas**.

#### Grupo 1: `get_age_reduction()` (6 tests)

Prueba que la reducción por edad es correcta según los rangos:

```python
test_get_age_reduction_under_40()      # edad < 40  → 0 kcal
test_get_age_reduction_40_to_49()      # 40-49      → 100 kcal
test_get_age_reduction_50_to_59()      # 50-59      → 200 kcal
test_get_age_reduction_60_to_69()      # 60-69      → 300 kcal
test_get_age_reduction_70_to_79()      # 70-79      → 400 kcal
test_get_age_reduction_80_plus()       # 80+        → 500 kcal
```

**Por qué**: La edad reduce el metabolismo. Verificar que cada década tiene la reducción correcta.

#### Grupo 2: `get_activity_factor()` (5 tests)

Prueba que los factores de actividad Harris-Benedict sean correctos:

```python
test_get_activity_factor_1()  # Sedentario    → 1.2
test_get_activity_factor_2()  # Poco activo   → 1.375
test_get_activity_factor_3()  # Moderado      → 1.55
test_get_activity_factor_4()  # Muy activo    → 1.725
test_get_activity_factor_5()  # Extra activo  → 1.9
```

**Por qué**: La actividad multiplica el metabolismo. Cada nivel tiene un factor específico.

#### Grupo 3: `get_adjusted_weight()` (6 tests)

Prueba la corrección de peso para obesidad (BMI ≥ 30):

```python
test_adjusted_weight_normal_bmi()      # BMI < 30 → peso sin cambios
test_adjusted_weight_overweight_bmi()  # BMI 25-30 → peso sin cambios
test_adjusted_weight_obese_bmi()       # BMI ≥ 30 → peso ajustado
test_adjusted_weight_calculation()     # Fórmula correcta: PC = PI + 0.25*(actual-PI)
test_adjusted_weight_extreme_obesity() # Caso extremo
test_adjusted_weight_borderline()      # Frontera BMI = 30
```

**Por qué**: En obesidad, usamos peso ajustado para evitar sobrestimar calorías.

#### Grupo 4: `calculate_bmr()` (4 tests)

Prueba la fórmula Harris-Benedict para Metabolismo Basal:

```python
test_calculate_bmr_male()      # Hombre
test_calculate_bmr_female()    # Mujer
test_calculate_bmr_male_low()  # Hombre con valores bajos
test_calculate_bmr_female_high() # Mujer con valores altos
```

**Por qué**: BMR es el cálculo central. Verificar con datos reales que el resultado es correcto.

#### Grupo 5: `calculate_tdee()` (3 tests)

Prueba el cálculo de gasto energético total:

```python
test_calculate_tdee_normal()     # Caso normal
test_calculate_tdee_low()        # Gasto bajo
test_calculate_tdee_high()       # Gasto alto
```

**Por qué**: TDEE = BMR × Factor × (1 - Reducción/BMR). Verificar la fórmula final.

#### Grupo 6: Tests de Integración (3 tests)

Prueba que todo funciona junto:

```python
test_full_calculation_male()     # Hombre: entrada → cálculo completo
test_full_calculation_female()   # Mujer: entrada → cálculo completo
test_full_calculation_obese()    # Obeso: entrada → cálculo con corrección
```

**Por qué**: Asegurar que el pipeline completo funciona sin errores.

---

## ✍️ Cómo Agregar un Nuevo Test

### Paso 1: Identificar qué testear

¿Es un endpoint o una función pura?

- **Endpoint** → `test/test_api.py`
- **Función matemática** → `test/test_calculations.py`

### Paso 2: Crear el test

**Ejemplo 1: Testear una función en `calculations.py`**

```python
def test_get_age_reduction_example():
    """Test que la reducción por edad es 200 para edad 55"""
    # Arrange (preparar)
    age = 55

    # Act (ejecutar)
    result = get_age_reduction(age)

    # Assert (verificar)
    assert result == 200
```

**Ejemplo 2: Testear un endpoint en `api.py`**

```python
def test_calculate_with_male_input():
    """Test POST /calculate con datos de hombre válidos"""
    # Arrange
    payload = {
        "sexo": "H",
        "peso": 80,
        "altura": 180,
        "edad": 30,
        "nivel_actividad": 3
    }

    # Act
    response = client.post("/calculate", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "tdee" in response.json()
```

### Paso 3: Correr el test

```bash
pytest test/test_api.py::test_calculate_with_male_input -v
```

### Paso 4: Si falla, investigar

```bash
# Ver el error detallado
pytest test/test_api.py::test_calculate_with_male_input -vv
```

---

## 📊 Cobertura de Código

### ¿Qué es cobertura?

Es el porcentaje de líneas de código que son ejecutadas por los tests.

### Cobertura Actual

```
app/api.py           87%  (9 líneas sin cubrir)
app/calculations.py  97%  (1 línea sin cubrir)
─────────────────────────
PROMEDIO             87%
```

### Líneas sin cubrir en `app/api.py`

Las 9 líneas faltantes son:
- Handlers de excepciones raras
- Configuración de CORS
- Casos que necesitarían mocks complejos

En producción funcionan bien sin tests específicos.

### Ver cobertura con detalles

```bash
pytest --cov=app --cov-report=term-missing
```

Esto te muestra exactamente qué líneas no tienen tests:

```
Missing
───────
46-49, 79, 86, 90, 99-100, 140
```

---

## 🔧 Solucionar Problemas

### Problema: "ModuleNotFoundError: No module named 'app'"

**Solución:** Corre pytest desde la raíz del proyecto:
```bash
cd nutrition_calculator
pytest
```

### Problema: "ImportError: cannot import name..."

**Solución:** Asegúrate de que la ruta en `sys.path` es correcta:
```python
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### Problema: Test lento

**Solución:** Corre solo el test que necesitas:
```bash
pytest test/test_api.py::test_health_check
```

### Problema: "FAILED - Connection refused"

**Solución:** Asegúrate de que FastAPI está importado correctamente:
```python
from fastapi.testclient import TestClient
```

---

## 🚀 GitHub Actions (CI/CD)

Los tests se ejecutan **automáticamente** en cada `git push`:

1. Ve a: https://github.com/Rosa-1015/dietaneo-caloric-calculator/actions
2. Haz clic en el último workflow
3. Verás si pasaron ✅ o fallaron ❌

Si fallan, el workflow mostrará:
- Qué test falló
- Por qué falló
- Dónde investigar

---

## 📚 Lectura Adicional

- [pytest documentación oficial](https://docs.pytest.org/)
- [FastAPI - Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [CLAUDE.md](../CLAUDE.md) - Arquitectura completa del proyecto
- [TESTING.md](./TESTING.md) - Guía mentor para aprender testing

---

**¡A testear! 🎯**
