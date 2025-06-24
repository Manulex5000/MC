import json
import numpy as np
import math
from calculos.propLiq import Constants, calcular_densidad, calcular_CTL, calcular_CPL
from calculos.calvol import calcular_volumen
from calculos.modelosU import montecarloU
import matplotlib.pyplot as plt

data = {
    "nsim": 100000,
    "tipoMet": "UFM",
    "API": 129.61,
    "product": "Lubricating Oil",
    "Tl": 91.4,
    "Pl": 72,
    "Pe": 14,
    "MR": 100000,  # pulsos
    "KF": 1500,
    "MF": 1,
    "SW": 1.5,

    "resTl": 0.1,
    "errorTl": 0.5,
    "ucalTl": 0.2,
    "kcalTl": 2.0,
    "uderTl": 0.1,

    "resPl": 0.1,
    "errorPl": 0.5,
    "ucalPl": 0.2,
    "kcalPl": 2.0,
    "uderPl": 0.1,

    "metSW": "externo",
    "uTSed": 0.005,
    "uTW": 0.01,
    "kTW": 2.0,
    "kSed": 2.0,

    "metdl": "externo",
    "uTdl": 1,
    "kdl": 2.0,

    "ucalMet": 0.3,
    "kcalMet": 2.0,
    "ecalMet": 0.5,

    "conditioner": "con acondicionador",
    "upLong": 10,
    "dwLong": 5,
    "twLong": 3
}


resultado = calcular_volumen(data)
incertidumbre = montecarloU(data)
print("Diccionario incertidumbre:", incertidumbre)
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

plt.axvline(media, color='blue', linestyle='--', label=f'Media = {media:.2f}')
plt.axvline(percentil_025, color='red', linestyle='--',
            label=f'Percentil 2.5% = {percentil_025:.3f}')
plt.axvline(percentil_975, color='green', linestyle='--',
            label=f'Percentil 97.5% = {percentil_975:.3f}')

plt.legend()

plt.tight_layout()
plt.show()
