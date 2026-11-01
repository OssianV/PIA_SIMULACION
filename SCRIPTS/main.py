import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
import sys

# Checamos si se tienen instaladas las librerias y las instalamos si no es asi
required_packages = ['yfinance', 'pandas', 'numpy', 'matplotlib']

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Definimos rutas relativas para el entorno del proyecto
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_outputs = os.path.join(os.path.dirname(ruta_actual), 'OUTPUTS')
os.makedirs(ruta_outputs, exist_ok=True)

# 1. Definimos lista de activos y el mercado a comparar (SYP100)
activos = ['MSFT', 'AAPL', 'AMZN', 'JPM', 'V', 'CVX', 'JNJ', 'PG', 'WMT', 'CAT']
mercado = ['^OEX']

# 2. Descargamos los datos historicos (2022 al 2025)
datos = yf.download(activos + mercado, start='2022-01-01', end='2025-12-31', auto_adjust=False)['Adj Close']

# Separamos los datos de los activos y del mercado
datos_activos = datos[activos]
datos_mercado = datos[mercado]

# 3. Calculo de retornos diarios
retornos_diarios = datos_activos.pct_change().dropna()

# 4. Calculo de metricas anualizadas
dias_operativos = 252   # Cantidad de dias operativos en la bolsa americana de valores
retornos_esperados_anuales = retornos_diarios.mean() * dias_operativos
matriz_covarianza_anual = retornos_diarios.cov() * dias_operativos

# 5. Generacion de lista estatica de pesos (20 iteraciones, sin aleatoriedad por ahora)
lista_pesos_fijos = [
    np.array([0.1118, 0.0316, 0.0241, 0.0751, 0.1191, 0.0516, 0.3703, 0.1082, 0.0615, 0.0467]),
    np.array([0.0686, 0.2132, 0.0943, 0.0100, 0.0829, 0.2187, 0.0329, 0.0315, 0.1238, 0.1239]),
    np.array([0.1136, 0.2138, 0.1455, 0.1066, 0.1447, 0.0440, 0.0507, 0.0293, 0.0393, 0.1125]),
    np.array([0.0105, 0.0617, 0.0612, 0.0739, 0.0602, 0.0406, 0.0603, 0.2429, 0.3131, 0.0756]),
    np.array([0.0897, 0.0113, 0.0350, 0.0492, 0.1846, 0.0265, 0.0605, 0.3888, 0.0672, 0.0871]),
    np.array([0.0145, 0.1977, 0.1044, 0.0890, 0.0474, 0.0410, 0.0609, 0.1292, 0.2353, 0.0807]),
    np.array([0.1256, 0.1000, 0.1113, 0.1274, 0.2096, 0.0099, 0.1637, 0.0317, 0.0245, 0.0964]),
    np.array([0.0129, 0.2777, 0.1265, 0.1648, 0.0021, 0.1157, 0.1043, 0.0222, 0.0213, 0.1525]),
    np.array([0.0443, 0.1360, 0.0934, 0.0569, 0.2995, 0.2129, 0.0511, 0.0051, 0.0420, 0.0587]),
    np.array([0.1024, 0.4509, 0.0369, 0.1207, 0.0755, 0.0987, 0.0137, 0.0427, 0.0231, 0.0353]),
    np.array([0.0833, 0.1272, 0.0130, 0.0162, 0.0450, 0.1255, 0.2170, 0.0933, 0.2232, 0.0563]),
    np.array([0.0379, 0.0435, 0.0187, 0.1759, 0.0412, 0.0800, 0.0860, 0.0734, 0.0003, 0.4432]),
    np.array([0.1762, 0.0174, 0.0259, 0.0549, 0.1735, 0.3074, 0.0223, 0.0621, 0.1229, 0.0375]),
    np.array([0.1218, 0.0163, 0.0851, 0.1863, 0.3807, 0.0077, 0.0519, 0.0212, 0.0555, 0.0736]),
    np.array([0.0094, 0.0339, 0.2526, 0.0810, 0.0588, 0.1347, 0.1303, 0.0048, 0.1187, 0.1759]),
    np.array([0.0209, 0.1752, 0.0389, 0.0422, 0.1262, 0.0136, 0.1261, 0.2524, 0.1375, 0.0669]),
    np.array([0.0535, 0.1343, 0.0773, 0.0082, 0.0810, 0.1563, 0.0381, 0.2434, 0.1288, 0.0791]),
    np.array([0.1548, 0.0092, 0.2180, 0.1914, 0.2674, 0.0153, 0.0095, 0.0166, 0.0566, 0.0613]),
    np.array([0.0869, 0.0137, 0.0237, 0.1757, 0.0664, 0.1737, 0.0008, 0.0844, 0.2828, 0.0919]),
    np.array([0.0367, 0.2013, 0.0758, 0.1756, 0.0047, 0.1608, 0.0052, 0.2173, 0.1019, 0.0207]),
]
cantidad_simulaciones = len(lista_pesos_fijos)

# 6. Simulacion de los 20 portafolios
rendimientos_simulados = []
riesgos_simulados = []
sharpes_simulados = []

tasa_libre_riesgo = 0.0707 # CETES a 28 dias en 31/12/2025

for pesos in lista_pesos_fijos:
    # Rendimiento esperado del portafolio
    rendimiento_portafolio = np.sum(retornos_esperados_anuales * pesos)
    
    # Riesgo (Volatilidad) usando la matriz de covarianza
    riesgo_portafolio = np.sqrt(np.dot(pesos.T, np.dot(matriz_covarianza_anual, pesos)))
    
    # Ratio de Sharpe
    ratio_sharpe = (rendimiento_portafolio - tasa_libre_riesgo) / riesgo_portafolio
    
    rendimientos_simulados.append(rendimiento_portafolio)
    riesgos_simulados.append(riesgo_portafolio)
    sharpes_simulados.append(ratio_sharpe)

rendimientos_simulados = np.array(rendimientos_simulados)
riesgos_simulados = np.array(riesgos_simulados)
sharpes_simulados = np.array(sharpes_simulados)

# 7. Identificacion de portafolios optimos (Max Sharpe, Min Riesgo, Max Rendimiento)
indice_max_sharpe = sharpes_simulados.argmax()
indice_min_riesgo = riesgos_simulados.argmin()
indice_max_rendimiento = rendimientos_simulados.argmax()

# 8. Visualizacion
plt.figure(figsize=(10, 6))
plt.scatter(riesgos_simulados, rendimientos_simulados, c=sharpes_simulados, cmap='viridis')
plt.colorbar(label='Ratio de Sharpe')

# Marcar y anotar los portafolios óptimos con sus porcentajes de asignación
optimos = [
    (indice_max_sharpe, 'Máximo Sharpe', 'red'),
    (indice_min_riesgo, 'Mínimo Riesgo', 'blue'),
    (indice_max_rendimiento, 'Máximo Rendimiento', 'orange')
]

for indice, etiqueta, color in optimos:
    # Graficar la estrella del portafolio óptimo
    plt.scatter(riesgos_simulados[indice], rendimientos_simulados[indice], color=color, marker='*', s=250, label=etiqueta)
    
    # Construir el texto con los porcentajes de cada activo
    pesos_actuales = lista_pesos_fijos[indice]
    texto_porcentajes = f"{etiqueta}:\n" + "\n".join([f"{activos[i]}: {pesos_actuales[i]*100:.1f}%" for i in range(len(activos))])
    
    # Añadir la anotación en la gráfica
    plt.annotate(
        texto_porcentajes,
        xy=(riesgos_simulados[indice], rendimientos_simulados[indice]),
        xytext=(15, 15), textcoords='offset points',
        fontsize=7,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color, alpha=0.8),
    )

plt.title('Simulacion de Portafolios - Borrador (20 iteraciones fijas)')
plt.xlabel('Volatilidad Anualizada (Riesgo)')
plt.ylabel('Rendimiento Esperado Anualizado')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# Guardar grafica
ruta_imagen = os.path.join(ruta_outputs, 'grafica_borrador.png')
plt.savefig(ruta_imagen, bbox_inches='tight', dpi=300)
print(f'Simulacion terminada. Grafica exportada en: {ruta_imagen}')
