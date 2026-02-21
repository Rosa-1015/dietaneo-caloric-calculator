from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from fastapi.middleware.cors import CORSMiddleware

# Import calculation functions from our local module
from app.calculations import get_age_reduction, get_activity_factor, calculate_bmr, calculate_tdee

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

# --- ERROR HANDLER (Customized for Spanish users) ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    custom_details = []
    
    for error in exc.errors():
        error_type = error.get("type")
        field = error.get("loc")[-1]
        
        if error_type == "missing":
            message = f"El campo '{field}' es obligatorio."
        elif error_type == "string_pattern_mismatch":
            message = f"En el campo '{field}' solo se permite 'H' para Hombre o 'M' para Mujer."
        elif error_type == "greater_than":
            limit = error.get("ctx", {}).get("gt")
            message = f"El valor de '{field}' debe ser mayor que {limit}."
        elif error_type == "less_than":
            limit = error.get("ctx", {}).get("lt")
            message = f"El valor de '{field}' debe ser menor que {limit}."
        elif error_type == "greater_than_equal":
            limit = error.get("ctx", {}).get("ge")
            message = f"El valor de '{field}' debe ser como mínimo {limit}."
        elif error_type == "less_than_equal":
            limit = error.get("ctx", {}).get("le")
            message = f"El valor de '{field}' debe ser como máximo {limit}."
        else:
            message = "El formato de este dato no es válido."

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