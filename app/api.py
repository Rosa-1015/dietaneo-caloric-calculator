from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Union

# Import calculation functions from our local module
from app.calculations import (
    get_age_reduction, 
    get_activity_factor, 
    calculate_bmr, 
    calculate_tdee, 
    get_adjusted_weight
)

# 1. Initialize the FastAPI app
app = FastAPI(title="Dietaneo API")

# 2. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---
# Hemos simplificado el modelo para que no valide tipos estrictos
# Así los datos llegan a 'calculate' y tú decides qué mensaje dar.
class NutritionData(BaseModel):
    gender: str = Field(..., validation_alias="sexo") 
    weight: Union[str, float, int] = Field(..., validation_alias="peso") 
    height: Union[str, float, int] = Field(..., validation_alias="altura") 
    age: Union[str, int] = Field(..., validation_alias="edad")
    activity_level: Union[str, float, int] = Field(..., validation_alias="nivel_actividad")

# --- ERROR HANDLER (Para campos obligatorios o sexo mal puesto) ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    custom_details = []
    for error in exc.errors():
        field = error.get("loc")[-1]
        error_type = error.get("type")
        
        if error_type == "missing":
            message = f"El campo '{field}' es obligatorio."
        else:
            message = f"Asegúrate de introducir un valor válido en '{field}'."
        
        custom_details.append({"field": field, "message": message})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status": "error", "message": "Datos de entrada inválidos", "details": custom_details},
    )

# --- ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "Dietaneo API - Harris-Benedict Logic con Criterio Clínico"}

@app.post("/calculate")
def calculate(data: NutritionData):
    # 1. LIMPIEZA Y CONVERSIÓN MANUAL (Blindada)
    try:
        # Normalizamos sexo a mayúsculas
        sexo_v = str(data.gender).upper()
        if sexo_v not in ["H", "M"]:
            return {
                "status": "error",
                "message": "En el campo 'sexo' solo se permite 'H' (Hombre) o 'M' (Mujer)."
            }

        # Forzamos conversión a string para manejar comas y campos vacíos
        peso_v = float(str(data.weight).replace(',', '.'))
        altura_v = float(str(data.height).replace(',', '.'))
        
        # Edad: la tratamos como string primero para limpiar posibles espacios
        edad_raw = str(data.age).strip()
        if not edad_raw:
            return {
                "status": "error",
                "message": "El campo 'edad' no puede estar vacío."
            }
        edad_v = int(edad_raw)
        
        # Actividad: Normalizamos para verificar si es entero
        actividad_raw = str(data.activity_level).replace(',', '.')
        actividad_f = float(actividad_raw)
        
        # Bloqueo si hay decimales en actividad (ej: 1.2)
        if actividad_f != float(int(actividad_f)):
            return {
                "status": "error",
                "encabezado": "ACTIVIDAD SIN DECIMALES",
                "message": "El nivel de actividad debe ser un número entero (1, 2, 3, 4 o 5). No se permiten decimales."
            }
        
        actividad_v = int(actividad_f)

    except (ValueError, TypeError):
        return {
            "status": "error",
            "message": "Asegúrate de introducir valores numéricos válidos en peso, altura, edad y actividad (puedes usar coma o punto)."
        }

    # 2. BLOQUEO DE SEGURIDAD (Edad)
    if edad_v < 18:
        return {
            "status": "error",
            "encabezado": "EDAD NO VÁLIDA",
            "message": "Esta calculadora está diseñada exclusivamente para adultos (18+ años).",
            "suplementacion_requerida": False,
            "total_calorias_diarias": 0
        }
    
    # 3. VALIDACIÓN DE RANGO (Actividad 1-5)
    if actividad_v < 1 or actividad_v > 5:
        return {
            "status": "error",
            "encabezado": "NIVEL DE ACTIVIDAD FUERA DE RANGO",
            "message": "El nivel de actividad debe ser exactamente 1, 2, 3, 4 o 5."
        }

    # 4. LÓGICA DE NEGOCIO
    effective_weight = get_adjusted_weight(peso_v, altura_v)
    reduction = get_age_reduction(edad_v)
    factor_final = get_activity_factor(actividad_v)
    
    bmr = calculate_bmr(sexo_v, effective_weight, altura_v, edad_v)
    tdee = calculate_tdee(bmr, factor_final, reduction)
    
    # 5. LÓGICA DE SUPLEMENTACIÓN
    is_weight_corrected = effective_weight < peso_v
    needs_supplementation = is_weight_corrected and tdee < 1800

    supplement_warning = ""
    if needs_supplementation:
        supplement_warning = "Nota: Al ser una pauta hipocalórica con ajuste metabólico por debajo de 1800 kcal, se recomienda valorar suplementación de micronutrientes."

    # 6. Respuesta final
    return {
            "encabezado": "RESULTADO PARA DIETANEO",
            "peso_utilizado_kg": round(effective_weight, 2),
            "calorias_en_reposo": round(bmr, 2),
            "kcal_actividad": round(bmr * (factor_final - 1), 2),
            "reduccion_edad": reduction,
            "total_calorias_diarias": round(tdee, 2),
            "suplementacion_requerida": needs_supplementation,
            "aviso_suplementacion": supplement_warning,
            "aviso_legal": "Esta estimación es orientativa y no sustituye la valoración profesional.",
            "recomendacion": "Para personalizar tu plan, consulta con un dietista.",
            "status": "success"
    }