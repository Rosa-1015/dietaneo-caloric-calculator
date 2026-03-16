"""
Tests para el módulo de cálculos nutricionales.

Este archivo prueba todas las funciones matemáticas en app/calculations.py
para asegurar que hacen exactamente lo que se espera.
"""

from app.calculations import (
    get_age_reduction,
    get_activity_factor,
    get_adjusted_weight,
    calculate_bmr,
    calculate_tdee
)


def test_age_reduction_under_40():
    """
    Cuando la edad es menor a 40 años, no debe haber reducción.

    Esto es importante porque según la lógica clínica, el metabolismo
    es máximo hasta los 40 años, luego comienza a disminuir.
    """
    # Arrange
    edad = 35

    # Act
    resultado = get_age_reduction(edad)

    # Assert
    assert resultado == 0


class TestAgeReduction:
    """Agrupa todos los tests relacionados con la reducción por edad."""

    def test_age_under_40_no_reduction(self):
        """Menores de 40 años no tienen reducción calórica."""
        assert get_age_reduction(18) == 0
        assert get_age_reduction(35) == 0
        assert get_age_reduction(39) == 0

    def test_age_40_to_49_reduction_100(self):
        """Entre 40-49 años, reducción de 100 kcal."""
        assert get_age_reduction(40) == 100
        assert get_age_reduction(45) == 100
        assert get_age_reduction(49) == 100

    def test_age_50_to_59_reduction_200(self):
        """Entre 50-59 años, reducción de 200 kcal."""
        assert get_age_reduction(50) == 200
        assert get_age_reduction(55) == 200
        assert get_age_reduction(59) == 200

    def test_age_60_to_69_reduction_300(self):
        """Entre 60-69 años, reducción de 300 kcal."""
        assert get_age_reduction(60) == 300
        assert get_age_reduction(65) == 300
        assert get_age_reduction(69) == 300

    def test_age_70_to_79_reduction_400(self):
        """Entre 70-79 años, reducción de 400 kcal."""
        assert get_age_reduction(70) == 400
        assert get_age_reduction(75) == 400
        assert get_age_reduction(79) == 400

    def test_age_80_plus_reduction_500(self):
        """80+ años, reducción de 500 kcal."""
        assert get_age_reduction(80) == 500
        assert get_age_reduction(90) == 500
        assert get_age_reduction(120) == 500


# ============================================================================
# TESTS DE FACTORES DE ACTIVIDAD
# ============================================================================

class TestActivityFactor:
    """Prueba que cada nivel de actividad retorne el factor Harris-Benedict correcto."""

    def test_activity_1_sedentary(self):
        """Nivel 1 (Sedentario) = multiplicador 1.2"""
        assert get_activity_factor(1) == 1.2

    def test_activity_2_light(self):
        """Nivel 2 (Ligero) = multiplicador 1.375"""
        assert get_activity_factor(2) == 1.375

    def test_activity_3_moderate(self):
        """Nivel 3 (Moderado) = multiplicador 1.55"""
        assert get_activity_factor(3) == 1.55

    def test_activity_4_heavy(self):
        """Nivel 4 (Fuerte) = multiplicador 1.725"""
        assert get_activity_factor(4) == 1.725

    def test_activity_5_very_heavy(self):
        """Nivel 5 (Muy Fuerte) = multiplicador 1.9"""
        assert get_activity_factor(5) == 1.9

    def test_activity_invalid_defaults_to_1_2(self):
        """Si recibe un valor inválido, retorna 1.2 por defecto."""
        assert get_activity_factor(10) == 1.2
        assert get_activity_factor(0) == 1.2


# ============================================================================
# TESTS DE CORRECCIÓN DE PESO (OBESIDAD)
# ============================================================================

class TestAdjustedWeight:
    """Prueba la fórmula de corrección de peso para pacientes con BMI >= 30."""

    def test_normal_weight_no_adjustment(self):
        """
        BMI normal (< 30) no se ajusta.

        Persona: 70 kg, 170 cm
        BMI = 70 / (1.70^2) = 24.22 (normal)
        """
        peso = 70
        altura = 170
        resultado = get_adjusted_weight(peso, altura)
        assert resultado == peso  # Sin cambios

    def test_overweight_no_adjustment(self):
        """
        Sobrepeso (BMI 25-29.9) no se ajusta.

        Persona: 85 kg, 170 cm
        BMI = 85 / (1.70^2) = 29.41 (sobrepeso)
        """
        peso = 85
        altura = 170
        resultado = get_adjusted_weight(peso, altura)
        assert resultado == peso

    def test_obese_weight_is_adjusted(self):
        """
        BMI >= 30 se ajusta usando fórmula clínica.

        Persona: 110 kg, 170 cm
        BMI = 110 / (1.70^2) = 38.05 (obeso)

        La función debe retornar menos peso que el real.
        """
        peso_real = 110
        altura = 170
        peso_ajustado = get_adjusted_weight(peso_real, altura)

        # El peso ajustado debe ser menor que el real
        assert peso_ajustado < peso_real

        # Debe seguir siendo realista (no puede ser negativo o muy pequeño)
        assert peso_ajustado > 50

    def test_height_safety_check(self):
        """
        Si altura es demasiado pequeña (< 50 cm), retorna peso sin cambios.

        Esto previene divisiones por cero o valores absurdos.
        """
        peso = 80
        altura_absurda = 30  # Impossible
        resultado = get_adjusted_weight(peso, altura_absurda)
        assert resultado == peso


# ============================================================================
# TESTS DE CÁLCULO DE BMR (Basal Metabolic Rate)
# ============================================================================

class TestCalculateBMR:
    """Prueba la fórmula de Harris-Benedict para BMR."""

    def test_bmr_male_typical(self):
        """
        Hombre típico: 80 kg, 180 cm, 35 años.
        Esperado: ~1830 kcal (rango aproximado)
        """
        bmr = calculate_bmr("H", 80, 180, 35)

        # Es un rango para permitir pequeñas variaciones de redondeo
        assert 1800 < bmr < 1860

    def test_bmr_female_typical(self):
        """
        Mujer típica: 65 kg, 165 cm, 35 años.
        Esperado: ~1400 kcal (rango aproximado)
        """
        bmr = calculate_bmr("M", 65, 165, 35)

        assert 1350 < bmr < 1450

    def test_bmr_men_higher_than_women(self):
        """Hombres gastan más calorías en reposo que mujeres con mismo peso/altura."""
        bmr_h = calculate_bmr("H", 75, 170, 30)
        bmr_m = calculate_bmr("M", 75, 170, 30)

        assert bmr_h > bmr_m

    def test_bmr_increases_with_weight(self):
        """A mayor peso, mayor BMR (más masa requiere más energía)."""
        bmr_light = calculate_bmr("H", 60, 180, 30)
        bmr_heavy = calculate_bmr("H", 100, 180, 30)

        assert bmr_heavy > bmr_light

    def test_bmr_decreases_with_age(self):
        """El metabolismo disminuye con la edad."""
        bmr_young = calculate_bmr("H", 80, 180, 25)
        bmr_old = calculate_bmr("H", 80, 180, 65)

        assert bmr_young > bmr_old


# ============================================================================
# TESTS DE CÁLCULO DE TDEE (Total Daily Energy Expenditure)
# ============================================================================

class TestCalculateTDEE:
    """Prueba el cálculo del gasto energético total."""

    def test_tdee_basic_calculation(self):
        """
        TDEE = (BMR * factor_actividad) - reduccion_edad

        Si BMR=1800, factor=1.55, reducción=100
        Esperado: (1800 * 1.55) - 100 = 2790 - 100 = 2690
        """
        bmr = 1800
        factor = 1.55
        reduction = 100

        tdee = calculate_tdee(bmr, factor, reduction)

        assert tdee == 2690

    def test_tdee_no_reduction_for_young(self):
        """Un joven sin reducción por edad."""
        bmr = 1600
        factor = 1.55
        reduction = 0  # Joven < 40 años

        tdee = calculate_tdee(bmr, factor, reduction)

        assert tdee == 1600 * 1.55

    def test_tdee_with_max_reduction(self):
        """Persona mayor con máxima reducción."""
        bmr = 1500
        factor = 1.2  # Sedentario
        reduction = 500  # 80+ años

        tdee = calculate_tdee(bmr, factor, reduction)

        assert tdee == (1500 * 1.2) - 500


# ============================================================================
# TESTS DE INTEGRACIÓN (Flujo completo)
# ============================================================================

class TestIntegration:
    """Prueba que todas las funciones funcionen juntas correctamente."""

    def test_complete_calculation_flow_normal_person(self):
        """
        Flujo completo para persona normal:
        - Hombre, 80 kg, 180 cm, 35 años, actividad 3
        """
        # Arrange
        gender = "H"
        weight = 80
        height = 180
        age = 35
        activity = 3

        # Act
        adjusted_weight = get_adjusted_weight(weight, height)
        age_reduction = get_age_reduction(age)
        activity_factor = get_activity_factor(activity)
        bmr = calculate_bmr(gender, adjusted_weight, height, age)
        tdee = calculate_tdee(bmr, activity_factor, age_reduction)

        # Assert
        assert adjusted_weight == weight  # Sin corrección por BMI normal
        assert age_reduction == 0  # Menor de 40
        assert activity_factor == 1.55
        assert tdee > 2000  # Debe ser un valor realista
        assert tdee < 3000

    def test_complete_calculation_flow_obese_person(self):
        """
        Flujo completo para persona con obesidad:
        - Mujer, 110 kg, 165 cm, 55 años, actividad 2
        """
        # Arrange
        gender = "M"
        weight = 110
        height = 165
        age = 55
        activity = 2

        # Act
        adjusted_weight = get_adjusted_weight(weight, height)
        age_reduction = get_age_reduction(age)
        activity_factor = get_activity_factor(activity)
        bmr = calculate_bmr(gender, adjusted_weight, height, age)
        tdee = calculate_tdee(bmr, activity_factor, age_reduction)

        # Assert
        assert adjusted_weight < weight  # Con corrección por BMI >= 30
        assert age_reduction == 200  # Entre 50-59
        assert activity_factor == 1.375
        assert tdee > 1500
        assert tdee < 2500
