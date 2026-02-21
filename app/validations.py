def validate_gender():
    while True:
        gender = input("¿Cuál es tu género (H/M)?: ").upper()
        if gender in ["H", "M"]:
            return gender
        print("❌ Género no reconocido. Introduce 'H' o 'M'.")

def validate_number(message, min_value, max_value=None):
    while True:
        try:
            value = float(input(message))
            if value <= min_value:
                print(f"❌ El valor debe ser mayor que {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"❌ Error: El valor no puede ser mayor que {max_value}.")
                continue
            return value
        except ValueError:
            print("❌ Error: Introduce un número válido.")

def validate_activity():
    while True:
        try:
            print("\nNiveles de actividad: 1.Sedentario, 2.Ligera, 3.Moderada, 4.Intensa, 5.Muy intensa")
            opcion = int(input("Elige tu nivel (1-5): "))
            if 1 <= opcion <= 5:
                return opcion
            print("❌ Elige un número entre 1 y 5.")
        except ValueError:
            print("❌ Error: Debe ser un número entero.")