from propLiq import Constants, calcular_densidad, calcular_CTL
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

API = 15
Pb = 14.65  # Base pressure, psi (from API Reference)
Tref = 60.0  # Reference Temperature, °F (from API Reference)
corr = 0.01374979547  # Temperature shift value (from API Reference)
dH2O = 999.016  # Densidad del agua en kg/m³
corrCTL = 0.98847
# corrCPL = 0
TOV = 435.73  # Volumen total observado en [Bbl]
FW = 0  # Volumen de agua libre en [Bbl]
Tb = 60  # Temperatura base en °F (de referencia)
Tamb = 60  # Temperatura ambiente en °F (de referencia)
Tl = 91     # Temperatura del líquido en °F
SW = 5  # Porcentaje de agua en el líquido (en %)
# Material del tanque, puede ser "Acero al Carbón", "Acero Inoxidable 304" o "Acero Inoxidable 316"
material = "Acero al Carbón"

# Sediment and Water Correction


def CSW(SW):
    return 1 - (SW) / 100

# Net Standard Volume


def NSV(MR, KF, MF, CTL, CPL, CSW, corrCTL, corrCPL):
    return MR / KF * MF * (CTL + corrCTL) * (CPL + corrCPL) * CSW


def TK(TOV, FW, CTSh, CTL, CSW):
    return (TOV - FW) * CTSh * CTL * CSW


def CTSh(material, Tamb, Tl):

    if material == "Acero al Carbón":
        alfa = 0.0000062
    elif material == "Acero Inoxidable 304":
        alfa = 0.00000961
    else:
        alfa = 0.00000899

    return (1 + (2 * alfa * (Tl - Tamb)) + alfa ** 2 * (Tl - Tamb)**2)

# 📌 Función principal que maneja la solicitud Flask


def calcular_volumen(data):
    try:

        print("📡 Datos recibidos:", data)  # ✅ Depuración

        # API = float(data.get('API', 0))
        product = data.get('product', 'Crude Oil')
        Tl = float(data.get('Tl', 0))
        # Pl = float(data.get('Pl', 0))
        # Pe = float(data.get('Pe', 0))
        # MR = float(data.get('MR', 0))
        # KF = float(data.get('KF', 0))
        # MF = float(data.get('MF', 0))
        SW = float(data.get('SW', 0) or 0)/100
        TOV = float(data.get('TOV', 0))
        FW = float(data.get('FW', 0))
        Tamb = float(data.get('Tamb', 0))

        print("✅ Variables extraídas correctamente")

        # Calculo de la densidad en kg/m3
        dl_value = calcular_densidad(API, dH2O)
        print("✅ densidad calculada correctamente")

        # Constantes
        K0, K1, K2 = Constants(product, dl_value, Tl)
        print("✅ constantes calculada correctamente")

        # CTL
        Bl_value = K0 / (dl_value ** 2) + K1 / dl_value + K2
        CTL_value = calcular_CTL(product, Bl_value, Tl)
        print("✅ ctl calculada correctamente")

        # CPL
        # F_value = math.exp(-1.9947 + 0.00013427 * Tl + 0.79392 /
        # (dl_value / 1000) ** 2 + 0.002326 * Tl / (dl_value / 1000) ** 2)
        # CPL_value = calcular_CPL(product, Pl, Pe, Tl, dl_value)
        # print("✅ cpl calculada correctamente")

        CTSh_value = CTSh(material, Tamb, Tl)
        # CSW
        CSW_value = CSW(SW)
        # NSV
        NSV_value = TK(TOV, FW, CTSh_value, CTL_value, CSW_value)

        print(f"✅ NSV calculado: {NSV_value}")

        NSV_value = float(NSV_value)

        print(f"✅ NSV convertido a float correctamente")

        return {
            "NSV": round(NSV_value, 4),
            "CTL": round(CTL_value, 4),
            # CPL": round(CPL_value, 4),
            # "dl": round(dl_value, 4)
        }

    except Exception as e:
        return {"error": str(e)}
