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

app = FastAPI(title="Dietaneo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---
class NutritionData(BaseModel):
    gender: str = Field(..., validation_alias="sexo") 
    weight: Union[str, float, int] = Field(..., validation_alias="peso") 
    height: Union[str, float, int] = Field(..., validation_alias="altura") 
    age: Union[str, int] = Field(..., validation_alias="edad")
    # Quitamos 'float' para no incentivar el uso de decimales en Swagger
    activity_level: Union[str, int] = Field(..., validation_alias="nivel_actividad")

# --- ERROR HANDLER ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    custom_details = []
    for error in exc.errors():
        field = error.get("loc")[-1]
        error_type = error.get("type")
        
        if error_type == "missing":
            message = f"El campo '{field}' es obligatorio."
        elif field == "sexo":
            message = "Solo se permite 'H' (Hombre) o 'M' (Mujer)."
        else:
            message = f"El valor en '{field}' no es válido."
        
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
    try:
        # 1. GÉNERO
        sexo_v = str(data.gender).upper().strip()
        if sexo_v not in ["H", "M"]:
            return {"status": "error", "message": "En el campo 'sexo' solo se permite 'H' o 'M'."}

        # 2. PESO Y ALTURA (Aceptan coma)
        peso_v = float(str(data.weight).replace(',', '.'))
        altura_v = float(str(data.height).replace(',', '.'))
        
        # 3. EDAD
        edad_raw = str(data.age).strip()
        if not edad_raw:
            return {"status": "error", "message": "La edad no puede estar vacía."}
        edad_v = int(edad_raw)
        
        # 4. ACTIVIDAD (Control total de texto y decimales)
        act_raw = str(data.activity_level).replace(',', '.').strip()
        
        if not act_raw:
            return {"status": "error", "message": "El nivel de actividad es obligatorio."}

        # Si escriben palabras o decimales (ej: "1.5" o "mucha")
        if "." in act_raw:
            return {
                "status": "error",
                "encabezado": "ACTIVIDAD SIN DECIMALES",
                "message": "El nivel de actividad debe ser un número entero (1, 2, 3, 4 o 5)."
            }
        
        # Si es una palabra, int() lanzará ValueError y saltará al except general
        actividad_v = int(act_raw)

    except (ValueError, TypeError):
        return {
            "status": "error",
            "message": "Asegúrate de introducir valores numéricos válidos en peso, altura, edad y actividad."
        }

    # --- VALIDACIONES DE RANGO ---
    if edad_v < 18:
        return {
            "status": "error",
            "encabezado": "EDAD NO VÁLIDA",
            "message": "Esta calculadora está diseñada exclusivamente para adultos (18+ años)."
        }
    
    if actividad_v < 1 or actividad_v > 5:
        return {
            "status": "error",
            "encabezado": "NIVEL DE ACTIVIDAD FUERA DE RANGO",
            "message": "El nivel de actividad debe ser exactamente 1, 2, 3, 4 o 5."
        }

    # --- LÓGICA DE NEGOCIO ---
    effective_weight = get_adjusted_weight(peso_v, altura_v)
    reduction = get_age_reduction(edad_v)
    factor_final = get_activity_factor(actividad_v)
    
    bmr = calculate_bmr(sexo_v, effective_weight, altura_v, edad_v)
    tdee = calculate_tdee(bmr, factor_final, reduction)
    
    is_weight_corrected = effective_weight < peso_v
    needs_supplementation = is_weight_corrected and tdee < 1800

    supplement_warning = ""
    if needs_supplementation:
        supplement_warning = "Nota: Al ser una pauta hipocalórica con ajuste metabólico por debajo de 1800 kcal, se recomienda valorar suplementación de micronutrientes."

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