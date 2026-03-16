def get_age_reduction(age: int) -> int:
    """
    Calcula la reducción calórica metabólica según la década de edad.
    """
    if age < 40:
        return 0
    elif age < 50:
        return 100
    elif age < 60:
        return 200
    elif age < 70:
        return 300
    elif age < 80:
        return 400
    else:
        return 500


def get_activity_factor(activity: int) -> float:
    """
    Asocia el nivel de actividad entero con su factor multiplicador Harris-Benedict.
    """
    factors = {
        1: 1.2,    # Sedentario
        2: 1.375,  # Ligero
        3: 1.55,   # Moderado
        4: 1.725,  # Fuerte
        5: 1.9     # Muy fuerte
    }
    return factors.get(activity, 1.2)


def get_adjusted_weight(weight: float, height: float) -> float:
    """
    Aplica la fórmula de Peso Corregido (PC) para pacientes con IMC >= 30.
    Utiliza el IMC de 24.9 (límite superior de normopeso) para el Peso Ideal (PI).
    """
    if height <= 50:
        return weight

    height_m = height / 100
    imc = weight / (height_m ** 2)

    if imc >= 30:
        pi = 24.9 * (height_m ** 2)
        pc = pi + 0.25 * (weight - pi)
        return round(pc, 2)

    return weight


def calculate_bmr(gender: str, weight: float, height: float, age: int) -> float:
    """
    Fórmula de Harris-Benedict original revisada (Roza & Shizgal).
    """
    if gender == "H":
        return (66.47 + (13.75 * weight) + (5.0 * height) - (6.75 * age))
    elif gender == "M":
        return (655.1 + (9.56 * weight) + (1.85 * height) - (4.68 * age))
    return 0.0


def calculate_tdee(bmr: float, factor: float, reduction: int) -> float:
    """
    Cálculo del Gasto Energético Total (TDEE) ajustado por factor de actividad
    y reducción metabólica por edad.
    """
    return (bmr * factor) - reduction
