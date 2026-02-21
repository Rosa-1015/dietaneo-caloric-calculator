from fastapi import FastAPI
from app.calculations import get_age_reduction, get_activity_factor, calculate_bmr, calculate_tdee
# Note: In a web API, we usually use Pydantic models instead of interactive validations

app = FastAPI(title="Dietaneo Nutritional Calculator")

@app.get("/")
def read_root():
    return {"message": "Welcome to Dietaneo API"}

@app.get("/calculate")
def calculate(gender: str, weight: float, height: float, age: int, activity: str):
    # 1. Get the factors based on your existing logic
    reduction = get_age_reduction(age)
    factor = get_activity_factor(activity)
    
    # 2. Perform the calculations
    bmr = calculate_bmr(gender, weight, height, age)
    tdee = calculate_tdee(bmr, factor, reduction)
    
    # 3. Return the result as JSON (perfect for WordPress)
    return {
        "bmr": round(bmr, 2),
        "activity_adjustment": round(bmr * (factor - 1), 2),
        "age_reduction": reduction,
        "tdee": round(tdee, 2)
    }