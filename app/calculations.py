def get_age_reduction(age):
    if age < 40 :
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
    return factor

def calculate_bmr(gender, weight, height, age):
    if gender == "H":
        bmr = (66 + (13.7 * weight) + (5 * height) - (6.8 * age))
    elif gender == "M":
        bmr = (655 + (9.6 * weight) + (1.8 * height) - (4.7 * age))
    return bmr

def calculate_tdee(bmr, factor, reduction):
    tdee = bmr * factor - reduction
    return tdee
