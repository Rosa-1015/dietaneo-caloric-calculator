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
    weight: Union[int, float, str] = Field(..., validation_alias="peso") # Acepta cualquier formato inicial
    height: Union[int, float, str] = Field(..., validation_alias="altura")
    age: int = Field(..., gt=0, lt=120, validation_alias="edad")
    activity_level: int = Field(..., ge=1, le=5, validation_alias="nivel_actividad") 

    @field_validator('weight', 'height', mode='before')
    @classmethod
    def clean_numeric_fields(cls, value):
        if isinstance(value, str):
            value = value.replace(',', '.')  # Cambia coma por punto
        try:
            return int(float(value)) # Convierte a float y luego a entero (ej: 80.5 -> 80)
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
        
        # Detecta cuando se introducen decimales donde ahora pedimos enteros
        if error_type == "int_parsing":
            message = f"El campo '{field}' debe ser un número entero sin decimales."
        elif error_type == "float_parsing":
            message = f"El campo '{field}' debe ser un número, no puede contener letras."
        elif error_type == "missing":
            message = f"El campo '{field}' es obligatorio."
        elif error_type == "string_pattern_mismatch":
            message = f"En el campo '{field}' solo se permite 'H' para Hombre o 'M' para Mujer."
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
            message = f"El formato del campo '{field}' no es válido."

        custom_details.append({
            "field": field,
            "message": message
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Datos de entrada inválidos",
            "details": custom_details
        },
    )

# --- ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "Dietaneo API - Harris-Benedict Logic con Criterio Clínico"}

@app.post("/calculate")
def calculate(data: NutritionData):
    # 1. LÓGICA DE PESO CORREGIDO
    effective_weight = get_adjusted_weight(data.weight, data.height)

    # 2. Cálculos metabólicos
    reduction = get_age_reduction(data.age)
    factor = get_activity_factor(data.activity_level)
    bmr = calculate_bmr(data.gender, effective_weight, data.height, data.age)
    tdee = calculate_tdee(bmr, factor, reduction)
    
    # 3. LÓGICA DE SUPLEMENTACIÓN (Nueva mejora)
    # Solo si el peso fue corregido Y las calorías finales son < 1800
    is_weight_corrected = effective_weight < data.weight
    needs_supplementation = is_weight_corrected and tdee < 1800

    supplement_warning = ""
    if needs_supplementation:
        supplement_warning = "Nota: Al ser una pauta hipocalórica con ajuste metabólico por debajo de 1800 kcal, se recomienda valorar suplementación de micronutrientes."

    # 4. Respuesta final
    return {
            "encabezado": "RESULTADO PARA DIETANEO",
            "peso_utilizado_kg": round(effective_weight, 2),
            "calorias_en_reposo": round(bmr, 2),
            "kcal_actividad": round(bmr * (factor - 1), 2),
            "reduccion_edad": reduction,
            "total_calorias_diarias": round(tdee, 2),
            "suplementacion_requerida": needs_supplementation,
            "aviso_suplementacion": supplement_warning,
            "aviso_legal": "Esta estimación es orientativa y no sustituye la valoración individualizada de un profesional cualificado en nutrición.",
            "recomendacion": "Para personalizar tu plan y asegurar una ingesta adecuada, consulta con un dietista.",
            "estado": "success"
    }