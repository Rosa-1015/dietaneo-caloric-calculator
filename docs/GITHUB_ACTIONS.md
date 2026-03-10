# GitHub Actions y CI/CD - Guía Completa

> 💡 **Eres un aprendiz de informática**, así que te explicaré qué es CI/CD y cómo GitHub Actions automatiza nuestras pruebas.

## ¿Qué es CI/CD?

### CI = Continuous Integration (Integración Continua)
**Definición simple**: Cada vez que subes código a GitHub, las máquinas de GitHub automáticamente:
1. 📥 Descargan tu código
2. 🔧 Instalan las dependencias
3. ✅ Ejecutan las pruebas
4. 📊 Generan un reporte

**Beneficio**: Detectamos errores **inmediatamente** sin esperar a que el código llegue a producción.

### CD = Continuous Deployment (Despliegue Continuo)
**Definición simple**: Si las pruebas pasan, el código se despliega automáticamente a servidores de producción.

> ⚠️ **Nota**: Nuestro proyecto actualmente **solo tiene CI** (GitHub Actions ejecuta tests). El CD (despliegue automático) se puede agregar después.

---

## El Archivo: `.github/workflows/tests.yml`

Este archivo YAML le dice a GitHub Actions **qué hacer y cuándo**.

### 📍 Ubicación en el Proyecto
```
.github/
└── workflows/
    └── tests.yml          ← Este es nuestro archivo
```

---

## Desglose Línea por Línea

```yaml
name: Tests
```
**¿Qué es?** El nombre que verás en GitHub cuando ejecute el workflow.
**Resultado**: En GitHub, verás: ✅ **Tests**

---

### Triggers: ¿Cuándo se ejecuta?

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
```

**¿Qué significa?**
- **`push`**: Se ejecuta cuando haces `git push` a las ramas `main` o `develop`
- **`pull_request`**: Se ejecuta cuando alguien abre un Pull Request hacia `main` o `develop`

**Ejemplo práctico**:
```bash
# Esto dispara el workflow (porque push a develop)
git push origin develop

# Esto también (porque abres PR hacia main o develop)
# Ir a GitHub → Open Pull Request
```

---

### El Trabajo (Job)

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
```

**¿Qué es?**
- `test`: Nombre del trabajo
- `runs-on: ubuntu-latest`: La máquina que ejecutará el código (Ubuntu Linux, última versión)

**Analógico**: Es como pedir prestada una computadora en la nube para ejecutar nuestras pruebas.

---

### Pasos (Steps)

Los pasos son **acciones secuenciales** que se ejecutan en orden:

#### Paso 1: Descargar el Código
```yaml
- uses: actions/checkout@v5
```
**Explicación**: GitHub descarga tu repositorio en esa máquina Ubuntu.

---

#### Paso 2: Instalar Python 3.13
```yaml
- name: Set up Python 3.13
  uses: actions/setup-python@v5
  with:
    python-version: '3.13'
```

**¿Qué hace?**
- `name`: Descripción del paso (verás esto en los logs)
- `uses`: Usa una acción predefinida de GitHub para instalar Python
- `python-version`: Especifica la versión (3.13, igual que nuestro `Dockerfile`)

**Resultado**: La máquina Ubuntu ahora tiene Python 3.13 listo.

---

#### Paso 3: Instalar Dependencias
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

**¿Qué hace?**
- `run: |`: Ejecuta comandos shell (el `|` significa "múltiples líneas")
- `python -m pip install --upgrade pip`: Actualiza pip (el administrador de paquetes)
- `pip install -r requirements.txt`: Instala todos los paquetes listados en `requirements.txt`

**Analógico**: Es como crear un entorno virtual y decirle "instala todo lo que necesitamos".

---

#### Paso 4: Ejecutar las Pruebas con Cobertura
```yaml
- name: Run tests with coverage
  run: |
    pytest --cov=app --cov-report=term-missing --cov-report=xml
```

**¿Qué hace?**
- `pytest`: Ejecuta todos los tests en el directorio `test/`
- `--cov=app`: Calcula la **cobertura de código** (qué porcentaje del código está siendo probado)
- `--cov-report=term-missing`: Muestra en la terminal qué líneas NO están siendo probadas
- `--cov-report=xml`: Genera un archivo `coverage.xml` con los datos detallados

**Resultado**:
```
test/test_api.py .................. [100%]
8 passed in 0.45s

Name                Stmts   Miss  Cover   Missing
---------------------------------------------------
app/api.py             95      0   100%
app/calculations.py    50      0   100%
---------------------------------------------------
TOTAL                 145      0   100%
```

---

#### Paso 5: Subir Cobertura a Codecov
```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    files: ./coverage.xml
    fail_ci_if_error: false
```

**¿Qué hace?**
- Sube el reporte de cobertura a [Codecov.io](https://codecov.io) (servicio externo)
- Codecov te muestra gráficas bonitas y alertas si la cobertura baja
- `fail_ci_if_error: false`: No detiene el workflow si Codecov falla (opcional)

---

## ¿Cómo Ver los Resultados?

### En GitHub (Interface Web)

1. Ve a tu repositorio: https://github.com/tu_usuario/nutrition_calculator
2. Haz clic en la pestaña **"Actions"**
3. Verás una lista de ejecuciones:
   ```
   ✅ Commit message        main    2 min ago
   ❌ Commit message        develop 5 min ago
   ⏳ Commit message        main    en progreso...
   ```

4. Haz clic en una ejecución para ver detalles:
   ```
   Tests
   ├── test (ubuntu-latest)
   │   ├── ✅ Checkout code
   │   ├── ✅ Set up Python 3.13
   │   ├── ✅ Install dependencies
   │   ├── ✅ Run tests with coverage
   │   └── ✅ Upload coverage to Codecov
   ```

### En Pull Requests

Cuando abres un PR, GitHub automáticamente:
1. Ejecuta el workflow
2. Muestra un badge al final del PR:
   ```
   ✅ Tests - All checks passed
   ```

**Beneficio**: Antes de mergear, sabes que el código está funcionando.

---

## Flujo Práctico: Un Ejemplo Completo

### Escenario: Haces cambios en `app/calculations.py`

```bash
# 1. Haces cambios y los committeas
git add app/calculations.py
git commit -m "refactor: simplify get_age_reduction function"

# 2. Subes a develop
git push origin develop
```

### ¿Qué Pasa Automáticamente?

```
┌─────────────────────────────────────┐
│ GitHub recibe tu push               │
│ → Dispara el workflow "Tests"       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ Máquina Ubuntu en GitHub Cloud:     │
│ 1. Descarga tu código               │
│ 2. Instala Python 3.13              │
│ 3. Instala dependencias             │
│ 4. Ejecuta: pytest --cov            │
│ 5. Sube resultados a Codecov        │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ Resultados en GitHub                │
│ ✅ Todos los tests pasaron          │
│ 📊 100% de cobertura                │
│ 📈 Gráficas en Codecov.io           │
└─────────────────────────────────────┘
```

---

## Errores Comunes y Soluciones

### ❌ Error: "ModuleNotFoundError: No module named 'app'"

**Causa**: Las dependencias no se instalaron correctamente.

**Solución**:
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt  # Verificar que este archivo existe
```

---

### ❌ Error: "pytest: command not found"

**Causa**: `pytest` no está en `requirements.txt`.

**Solución**: Verifica que `requirements.txt` contenga:
```
pytest
pytest-cov
httpx
```

---

### ❌ Error: "Tests failed: 2 passed, 1 failed"

**Causa**: Un test no está pasando.

**Solución**:
1. Mira el log completo en GitHub Actions
2. Ejecuta localmente: `pytest -v` para ver qué falla
3. Arregla el código
4. Haz push de nuevo

---

## Optimizaciones Futuras

### ✅ Cosas que Podemos Agregar:

#### 1. **Linting Automático** (Verificar estilo de código)
```yaml
- name: Lint with Ruff
  run: python -m ruff check .
```

#### 2. **Dockerfile Build Check** (Verificar que Docker compile)
```yaml
- name: Build Docker image
  run: docker build -t nutrition-calculator .
```

#### 3. **Pruebas en Múltiples Versiones de Python**
```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12', '3.13']
```

#### 4. **Despliegue Automático a Producción** (CD)
```yaml
- name: Deploy to Production
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh
```

---

## Resumen: Lo Que Aprendimos

| Concepto | Explicación |
|----------|-------------|
| **CI/CD** | Integración Continua (tests automáticos) + Despliegue Continuo (enviar a producción) |
| **Workflow** | Archivo YAML que define qué hacer y cuándo |
| **Trigger** | Evento que inicia el workflow (push, pull_request) |
| **Job** | Conjunto de pasos que se ejecutan en una máquina |
| **Step** | Una acción individual (instalar Python, ejecutar tests, etc.) |
| **Cobertura** | Porcentaje del código que está siendo probado |
| **Codecov** | Servicio que almacena y muestra gráficas de cobertura |

---

## Preguntas Frecuentes (FAQ)

### P: ¿Por qué está en `.github/workflows/`?
**R**: GitHub automáticamente busca workflows en esa carpeta. Es como una convención.

### P: ¿Se ejecuta en mi computadora?
**R**: No, se ejecuta en servidores de GitHub en la nube (máquinas Ubuntu gratuitas).

### P: ¿Cuánto cuesta?
**R**: Para repositorios públicos es **completamente gratis**. GitHub te da minutos gratuitos al mes.

### P: ¿Puedo ver los logs?
**R**: Sí, en GitHub → Actions → Tu workflow → Ver logs detallados.

### P: ¿Qué pasa si un test falla?
**R**: El workflow se detiene con estado ❌ rojo. El PR no se puede mergear hasta que fixes el test.

---

## Próximos Pasos

1. **Observa**: Haz un push a `develop` y mira GitHub Actions en acción
2. **Experimenta**: Intenta romper un test deliberadamente para ver qué pasa
3. **Aprende**: Lee los logs detallados para entender qué hace cada paso
4. **Automatiza**: Agrega más validaciones (linting, Docker checks, etc.)

---

**Recuerda**: GitHub Actions es tu **asistente automático** que verifica el código 24/7. ¡No te duermes, pero tu CI/CD sí! 🤖✨
