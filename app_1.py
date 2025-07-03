import json
import numpy as np
import math
from calculos.calvol import calcular_volumen
from calculos.modelosU import montecarloU
import matplotlib.pyplot as plt

data = {
    "nsim": 100000,  # Número de simulaciones
    # "tipoMet": "UFM",
    "API": 129.61,  # Gravedad API
    "product": "Crude Oil",  # Tipo de producto
    "Tl": 91.4,  # T° del líquido
    "Pl": 72,  # Presión del líquido
    "Pe": 14.7,  # Presión base
    # "MR": 100000,  # pulsos
    # "KF": 1500,
    # "MF": 1,
    "SW": 5,  # Saturación de agua en porcentaje
    "TOV": 435.73,  # Volument total observado
    "uTOV": 2.0,  # Incertidumbre del volumen total observado

    "resTl": 0.1,  # Resolución T° del líquido
    "errorTl": 0.5,  # Error T° del líquido
    "ucalTl": 0.2,  # Incertidumbre de calibración T° del líquido
    # "kcalTl": 2.0,
    "uderTl": 0.1,  # Incertidumbre estándar de líquido

    "resPl": 0.1,  # Resolución de presión del líquido
    "errorPl": 0.5,  # Error presión de líquido
    "ucalPl": 0.2,  # Incertidumbre de calibración presión de líquido
    "kcalPl": 2.0,  # Factor de cobertura de calibración de líquido
    "uderPl": 0.1,  # Incertidumbre estándar de presión de líquido

    "metSW": "externo",  # Saturación de agua en el medidor
    "uTSed": 0.005,  # Incertidumbre estándar de sedimentos
    "uTW": 0.01,  # Incertidumbre estándar de agua
    "kTW": 2.0,  # Factor de cobertura de agua
    "kSed": 2.0,  # Factor de cobertura de sedimentos

    "metdl": "externo",  # Densidad del líquido en el medidor
    "uTdl": 1,  # Incertidumbre estándar de densidad de líquido
    "kdl": 2.0,  # Factor de cobertura de densidad de líquido

    "ucalMet": 0.3,  # Incertidumbre estándar de calibración en el medidor
    "kcalMet": 2.0,  # Factor de cobertura de calibración del medidor
    "ecalMet": 0.5,  # error de calibración del medidor

    "conditioner": "con acondicionador",  # equipos de acondicionamiento
    "upLong": 10,
    "dwLong": 5,
    "twLong": 3
}


resultado = calcular_volumen(data)
incertidumbre = montecarloU(data)


print("Diccionario incertidumbre:", incertidumbre)
if 'error' in incertidumbre:
    print("Error en el cálculo de incertidumbre:", incertidumbre['error'])
else:
    nsv_ = incertidumbre['NSV']
    media = np.mean(nsv_)
    percentil_025 = np.percentile(nsv_, 2.5)
    percentil_975 = np.percentile(nsv_, 97.5)
    U = (percentil_975-percentil_025)/(2*media)*100
    print('TK')

# print(U)

    plt.hist(nsv_, bins=50, color='skyblue', edgecolor='white')
    plt.title('Histograma de NSV')
    plt.xlabel('NSV')
    plt.ylabel('Frecuencia')

    plt.axvline(media, color='blue', linestyle='--',
                label=f'Media = {media:.2f}')
    plt.axvline(percentil_025, color='red', linestyle='--',
                label=f'Percentil 2.5% = {percentil_025:.3f}')
    plt.axvline(percentil_975, color='green', linestyle='--',
                label=f'Percentil 97.5% = {percentil_975:.3f}')

    plt.legend()

    plt.tight_layout()
    plt.show()
