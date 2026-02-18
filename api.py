from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

# Importamos tus funciones de calculations.py
from calculations import get_age_reduction, get_activity_factor, calculate_bmr, calculate_tdee

app = FastAPI(title="Dietaneo API")

# --- MODELO DE DATOS ---
class NutritionData(BaseModel):
    gender: str = Field(..., pattern="^[HM]$") 
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    age: int = Field(..., gt=0, lt=120)
    activity_level: int = Field(..., ge=1, le=5) 

    @field_validator('gender', mode='before')
    @classmethod
    def transform_gender_to_upper(cls, value: str):
        if isinstance(value, str):
            return value.upper()
        return value

# --- MANEJADOR DE ERRORES EN ESPAÑOL ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    detalles_personalizados = []
    
    for error in exc.errors():
        tipo = error.get("type")
        campo = error.get("loc")[-1]
        
        if tipo == "missing":
            mensaje = f"El campo '{campo}' es obligatorio."
        elif tipo == "string_pattern_mismatch":
            mensaje = f"En el campo '{campo}' solo se permite 'H' para Hombre o 'M' para Mujer."
        elif tipo == "greater_than":
            limite = error.get("ctx", {}).get("gt")
            mensaje = f"El valor de '{campo}' debe ser mayor que {limite}."
        elif tipo == "less_than":
            limite = error.get("ctx", {}).get("lt")
            mensaje = f"El valor de '{campo}' debe ser menor que {limite}."
        elif tipo == "greater_than_equal":
            limite = error.get("ctx", {}).get("ge")
            mensaje = f"El valor de '{campo}' debe ser como mínimo {limite}."
        elif tipo == "less_than_equal":
            limite = error.get("ctx", {}).get("le")
            mensaje = f"El valor de '{campo}' debe ser como máximo {limite}."
        else:
            mensaje = "El formato de este dato no es válido."

        detalles_personalizados.append({
            "campo": campo,
            "mensaje": mensaje
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Datos de entrada inválidos",
            "detalles": detalles_personalizados
        },
    )

# --- ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "Dietaneo API - Harris-Benedict Logic"}

@app.post("/calculate")
def calculate(data: NutritionData):
    
    reduction = get_age_reduction(data.age)
    factor = get_activity_factor(data.activity_level)
    bmr = calculate_bmr(data.gender, data.weight, data.height, data.age)
    tdee = calculate_tdee(bmr, factor, reduction)
    
    return {
        "header": "RESULTADO PARA DIETANEO",
        "bmr_kcal": round(bmr, 2),
        "activity_added_kcal": round(bmr * (factor - 1), 2),
        "age_reduction_kcal": reduction,
        "total_recommended_kcal": round(tdee, 2),
        "status": "success"
    }