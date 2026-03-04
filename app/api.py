from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
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
class NutritionData(BaseModel):
    gender: str = Field(..., pattern="^[HM]$", validation_alias="sexo") 
    weight: Union[str, float, int] = Field(..., validation_alias="peso") 
    height: Union[str, float, int] = Field(..., validation_alias="altura") 
    age: int = Field(..., gt=0, lt=120, validation_alias="edad")
    activity_level: Union[str, float, int] = Field(..., validation_alias="nivel_actividad")

    @field_validator('weight', 'height', mode='before')
    @classmethod
    def clean_numeric_fields(cls, value):
        if isinstance(value, str):
            value = value.replace(',', '.')
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError("Debe ser un número válido")

    @field_validator('gender', mode='before')
    @classmethod
    def transform_gender_to_upper(cls, value: str):
        if isinstance(value, str):
            return value.upper()
        return value

# --- ERROR HANDLER ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    custom_details = []
    for error in exc.errors():
        error_type = error.get("type")
        field = error.get("loc")[-1]
        
        if error_type == "int_parsing":
            message = f"El campo '{field}' debe ser un número entero (1, 2, 3, 4 o 5) sin decimales."
        elif error_type in ["greater_than_equal", "ge", "less_than_equal", "le"]:
            message = f"El nivel de actividad debe ser un número entero entre 1 y 5."
        elif error_type == "float_parsing" or "value_error" in error_type:
            message = f"El campo '{field}' debe ser un número válido (puedes usar coma o punto)."
        elif error_type == "missing":
            message = f"El campo '{field}' es obligatorio."
        elif error_type == "string_pattern_mismatch":
            message = f"En el campo '{field}' solo se permite 'H' (Hombre) o 'M' (Mujer)."
        elif error_type in ["greater_than", "gt"]:
            limit = error.get("ctx", {}).get("gt")
            message = f"El valor de '{field}' debe ser mayor que {limit}."
        elif error_type in ["less_than", "lt"]:
            limit = error.get("ctx", {}).get("lt")
            message = f"El valor de '{field}' debe ser menor que {limit}."
        elif error_type in ["greater_than_equal", "ge"]:
            limit = error.get("ctx", {}).get("ge")
            message = f"El valor de '{field}' debe ser como mínimo {limit}."
        elif error_type in ["less_than_equal", "le"]:
            limit = error.get("ctx", {}).get("le")
            message = f"El valor de '{field}' debe ser como máximo {limit}."
        else:
            message = f"Formato no válido para '{field}'."

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
@app.post("/calculate")
@app.post("/calculate")
def calculate(data: NutritionData):
    # 1. LIMPIEZA Y CONVERSIÓN MANUAL (Blindada)
    try:
        # Forzamos conversión a string para manejar el reemplazo de comas
        peso_v = float(str(data.weight).replace(',', '.'))
        altura_v = float(str(data.height).replace(',', '.'))
        edad_v = int(data.age)
        
        # Actividad: Normalizamos para verificar si es entero
        actividad_raw = str(data.activity_level).replace(',', '.')
        
        # Bloqueo si hay decimales en actividad (ej: 1.2 o 1,2)
        if float(actividad_raw) != float(int(float(actividad_raw))):
            return {
                "status": "error",
                "encabezado": "ACTIVIDAD SIN DECIMALES",
                "message": "El nivel de actividad debe ser un número entero (1, 2, 3, 4 o 5). No se permiten decimales."
            }
        
        actividad_v = int(float(actividad_raw))

    except (ValueError, TypeError):
        return {
            "status": "error",
            "message": "Asegúrate de introducir valores numéricos válidos en peso, altura y actividad."
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
    
    bmr = calculate_bmr(data.gender, effective_weight, altura_v, edad_v)
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