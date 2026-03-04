# --- FUNCIONES DE APOYO (Helpers) ---

def get_age_reduction(age):
    if age < 40:
        reduction = 0
    elif age < 50:
        reduction = 100
    elif age < 60:
        reduction = 200
    elif age < 70:
        reduction = 300 
    elif age < 80:
        reduction = 400
    else:
        reduction = 500
    return reduction

def get_activity_factor(activity):
    match activity:
        case 1:
            factor = 1.2
        case 2:
            factor = 1.375
        case 3:
            factor = 1.55
        case 4:
            factor = 1.725
        case 5:
            factor = 1.9
        case _:
            factor = 1.2  # Valor por defecto por seguridad
    return factor

# --- NUEVA FUNCIÓN: PESO CORREGIDO PARA OBESIDAD ---

def get_adjusted_weight(weight, height):
    """
    Calcula el IMC y, si es >= 30, devuelve el Peso Corregido (PC).
    Si no, devuelve el Peso Real (PR).
    Blindado contra errores de tipo de dato.
    """
    # 1. Aseguramos que los valores sean numéricos para evitar Internal Server Error
    weight = float(weight)
    height = float(height)
    
    # 2. Convertimos altura a metros
    height_m = height / 100

    # 3. Calculamos IMC
    if height_m <= 0:  # Seguridad extra para evitar división por cero
        return weight
        
    imc = weight / (height_m ** 2)

    # 4. Lógica de corrección por obesidad
    if imc >= 30:
        # Peso Ideal (PI) = 22 * talla^2
        pi = 22 * (height_m ** 2)
        # Peso Corregido (PC) = PI + 0.25 * (PR - PI)
        pc = pi + 0.25 * (weight - pi)
        return round(pc, 2)
    
    return weight

# --- FÓRMULAS PRINCIPALES ---

def calculate_bmr(gender, weight, height, age):
    if gender == "H":
        bmr = (66 + (13.7 * weight) + (5 * height) - (6.8 * age))
    elif gender == "M":
        bmr = (655 + (9.6 * weight) + (1.8 * height) - (4.7 * age))
    else:
        bmr = 0
    return bmr

def calculate_tdee(bmr, factor, reduction):
    tdee = (bmr * factor) - reduction
    return tdee