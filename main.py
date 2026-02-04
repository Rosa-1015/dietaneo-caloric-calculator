from calculations import get_age_reduction, get_activity_factor, calculate_bmr, calculate_tdee
from validations import  validate_gender, validate_number, validate_activity

print("--- Calculadora de Necesidades Calóricas Diarias ---")

bmr = None 

gender = validate_gender()

weight = validate_number("¿Cuál es tu peso en kg? ", 0)

height = validate_number("¿Cuál es tu altura en cm? ", 0)

age = int(validate_number("¿Cuál es tu edad?: ", 0, 120))

reduction = get_age_reduction(age)

activity = validate_activity()

factor = get_activity_factor(activity)

bmr = calculate_bmr(gender, weight, height, age)

tdee = calculate_tdee(bmr, factor, reduction)

print("\n" + "="*40)
print(f"RESULTADO PARA DIETANEO")
print(f"Tu Tasa Metabólica Basal (TMB) es: {bmr:.2f} kcal")
print(f"Factor de actividad aplicado = {bmr * (factor-1):.2f} kcal")
print(f"Reducción aplicada por edad: -{reduction} kcal")
print(f"Las calorías diarias recomendadas son: {tdee:.2f} kcal")
print("="*40)
