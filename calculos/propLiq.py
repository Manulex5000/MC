
import math
import numpy as np

Pb = 14.65  # Base pressure, psi (from API Reference)
Tref = 60.0  # Reference Temperature, °F
corr = 0.01374979547  # Temperature shift value
dH2O = 999.016  # Water density in kg/m³

# 📌 SELECCIÓN DE CONSTANTES


def Constants(Product, dl, Tl):
    # Líquidos por tipo general
    if Product == 'Crude Oil':
        return 341.0957, 0, 0

    elif Product == 'Lubricating Oil':
        return 0, 0.34878, 0

    elif Product == 'Refined Products':
        if 838.3127 <= dl <= 1163.5:
            return 103.872, 0.2701, 0
        elif 787.5195 <= dl < 838.3127:
            return 330.301, 0, 0
        elif 770.3520 <= dl < 787.5195:
            return 1489.067, 0, -0.0018684
        elif 610.6 <= dl < 770.3520:
            return 192.4571, 0.2438, 0

    elif Product == 'GLP':
        return 192.4571, 0.2438, 0

    # Compuestos específicos o por temperatura
    elif 300 <= Tl < 350:
        return 1.031118, -0.00051827, -0.0000000035109, -0.000000000019836, 0.0

    elif 350 <= Tl <= 400:
        return 1.029099, -0.00048287, -0.000000037692, 0.0000000000378575, 0.0

    elif Product == 'Benzene':
        return 1.038382492, -0.00062307, -0.00000028505, 0.00000000012692, 0.0

    elif Product == 'Cumene':
        return 1.032401114, -0.00053445, -0.000000095067, 0.000000000036272, 0.0

    elif Product == 'Cyclohexane':
        return 1.039337296, -0.00064728, -0.00000014582, 0.000000000103538, 0.0

    elif Product == 'Ethylbenzene':
        return 1.033346632, -0.00055243, 0.000000000837035, -0.0000000012692, 0.00000000000555061

    elif Product == 'Styrene':
        return 1.032227515, -0.00053444, -0.000000044323, 0.0, 0.0

    elif Product == 'Toluene':
        return 1.035323647, -0.00058887, 0.00000000246508, -0.0000000000072802, 0.0

    elif Product == 'mXylene':
        return 1.031887514, -0.00052326, -0.00000013253, -0.000000000073596, 0.0

    elif Product == 'oXylene':
        return 1.031436449, -0.00052302, -0.0000000025217, -0.00000000021384, 0.0

    elif Product == 'pXylene':
        return 1.032307, -0.00052815, -0.00000018416, 0.000000000189256, 0.0

    # Si nada aplica, retorna None para que lo manejes
    return None

# 📌 CÁLCULO DE LA DENSIDAD DEL LÍQUIDO


def calcular_densidad(API, dH2O):
    return 141.5 / (API + 131.5) * dH2O


# 📌 CÁLCULO DE CTL
def calcular_CTL(product, Bl_value, Tl):
    Tref = 60.0  # Reference Temperature, °F (from API Reference)
    if product in ["Crude Oil", "Lubricating Oil", "Fuel Oils", "Jet Fuels", "Transition Zone", "Gasolines", "GLP"]:
        return np.exp(-Bl_value * (Tl - Tref) * (1 + 0.8 * Bl_value * (Tl - Tref + corr)))
    return 1  # Si el producto no está en la lista, devolver 1

# 📌 CÁLCULO DE CPL


def calcular_CPL(product, Pl, Pe, Tl, dl):
    Pb = 14.65
    dH2O = 999.016  # Water density in kg/m³
    if product == "GLP":
        F = 1 / (-0.0000021465891 * (Tl + 459.67)**2 + 0.00001577439 * (Tl + 459.67)**2 * (dl / dH2O)**2 -
                 0.000010502139 * (Tl + 459.67)**2 * (dl / dH2O)**4 + 0.00000028324481 * (Tl + 459.67)**3 * (dl / dH2O)**6 -
                 0.95495939 + 0.000000072900662 * (Tl + 459.67)**3 * (dl / dH2O)**2 - 0.00000027769343 * (Tl + 459.67)**3 * (dl / dH2O)**4 +
                 0.03645838 * (Tl + 459.67) * (dl / dH2O)**2 - 0.05110158 * (Tl + 459.67) * (dl / dH2O) + 0.00795529 * (Tl + 459.67) +
                 9.1311491 * (dl / dH2O)) / (10**-5) + (Pl - Pe) * (-0.000000000603576667 * (Tl + 459.67)**2 +
                                                                    0.0000022112678 * (Tl + 459.67) * (dl / dH2O)**2 + 0.00088384 * (dl / dH2O) - 0.00204016 * (dl / dH2O)**2 / (0.00001))
    else:
        F = np.exp(-1.9947 + 0.00013427 * Tl + 0.79392 /
                   (dl / 1000)**2 + 0.002326 * Tl / (dl / 1000)**2)

    if product in ["Crude Oil", "Lubricating Oil", "Fuel Oils", "Jet Fuels", "Transition Zone", "Gasolines", "GLP"]:
        return 1 / (1 - (Pl - (Pe - Pb)) * F * 0.00001)
    return 1  # Si el producto no está en la lista, devolver 1

# 📌 FUNCIÓN PRINCIPAL PARA CALCULAR PROPIEDADES


def calcular_propiedades(data):
    try:
        API = float(data.get('API', 0))
        product = data.get('product', 'Crude Oil')
        Tl = float(data.get('Tl', 0))
        Pl = float(data.get('Pl', 0))
        Pe = float(data.get('Pe', 0))

        # 🔹 Cálculo de la densidad
        dl_value = calcular_densidad(API)

        # 🔹 Obtener constantes según el producto
        K0, K1, K2 = Constants(product, dl_value, Tl)

        # 🔹 Calcular CTL
        Bl_value = K0 / (dl_value ** 2) + K1 / dl_value + K2
        CTL_value = calcular_CTL(product, Bl_value, Tl)

        # 🔹 Calcular CPL
        F_value = math.exp(-1.9947 + 0.00013427 * Tl + 0.79392 /
                           (dl_value / 1000) ** 2 + 0.002326 * Tl / (dl_value / 1000) ** 2)
        CPL_value = calcular_CPL(product, Pl, Pe, Pb)

        return {
            "dl": round(dl_value, 4),
            "CTL": round(CTL_value, 4),
            "CPL": round(CPL_value, 4)
        }

    except Exception as e:
        return {"error": str(e)}
