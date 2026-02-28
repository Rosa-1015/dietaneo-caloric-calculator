from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from fastapi.middleware.cors import CORSMiddleware

# Import calculation functions from our local module
# Añadimos get_adjusted_weight para la nueva lógica de obesidad
from app.calculations import (
    get_age_reduction, 
    get_activity_factor, 
    calculate_bmr, 
    calculate_tdee, 
    get_adjusted_weight
)

# 1. Initialize the FastAPI app
app = FastAPI(title="Dietaneo API")

# 2. CORS Configuration para permitir peticiones desde el frontend de WordPress
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---
class NutritionData(BaseModel):
    # IMPORTANTE: Usamos validation_alias para que WordPress envíe los datos en español
    # pero internamente la lógica de Python siga usando nombres estándar en inglés
    gender: str = Field(..., pattern="^[HM]$", validation_alias="sexo") 
    weight: float = Field(..., gt=0, validation_alias="peso")
    height: float = Field(..., gt=0, validation_alias="altura")
    age: int = Field(..., gt=0, lt=120, validation_alias="edad")
    activity_level: int = Field(..., ge=1, le=5, validation_alias="nivel_actividad") 

    @field_validator('gender', mode='before')
    @classmethod
    def transform_gender_to_upper(cls, value: str):
        if isinstance(value, str):
            return value.upper()
        return value

# --- ERROR HANDLER ---
# Personalizamos las respuestas de error para que el usuario de la web reciba mensajes claros en español
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    custom_details = []
    
    for error in exc.errors():
        error_type = error.get("type")
        # 'loc' contendrá el alias (ej: 'peso') gracias a la configuración del modelo
        field = error.get("loc")[-1]
        
        # --- NUEVA LÓGICA PARA ERRORES DE FORMATO ---
        # Detecta cuando se introducen letras en campos numéricos
        if error_type in ["float_parsing", "int_parsing"]:
            message = f"El campo '{field}' debe ser un número, no puede contener letras."
        
        # --- TRADUCCIÓN DE VALIDACIONES EXISTENTES ---
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
    return {"message": "Dietaneo API - Harris-Benedict Logic"}

@app.post("/calculate")
def calculate(data: NutritionData):
    # --- LÓGICA DE PESO CORREGIDO ---
    # 1. Calculamos el peso efectivo (ajustado por obesidad si IMC >= 30)
    # Internamente mantenemos el código en inglés por estándar profesional (effective_weight)
    effective_weight = get_adjusted_weight(data.weight, data.height)

    # 2. Cálculos metabólicos principales
    # IMPORTANTE: Internamente seguimos usando los nombres en inglés (data.age, etc.)
    # Pero ahora pasamos el 'effective_weight' a la fórmula del BMR en lugar del peso real directo
    reduction = get_age_reduction(data.age)
    factor = get_activity_factor(data.activity_level)
    bmr = calculate_bmr(data.gender, effective_weight, data.height, data.age)
    tdee = calculate_tdee(bmr, factor, reduction)
    
    # 3. Respuesta final formateada en castellano para la integración con WordPress
    return {
            "encabezado": "RESULTADO PARA DIETANEO",
            "peso_utilizado_kg": effective_weight, # Mostramos qué peso se usó para transparencia clínica
            "calorias_en_reposo": round(bmr, 2),
            "kcal_actividad": round(bmr * (factor - 1), 2),
            "reduccion_edad": reduction,
            "total_calorias_diarias": round(tdee, 2),
            "estado": "success"
    }