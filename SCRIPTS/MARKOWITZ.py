
# MODULO 2: OPTIMIZACION ESTANDAR DE MARKOWITZ
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

from pathlib import Path

# ==========================================================
# 1. CONFIGURACION GENERAL
# ==========================================================

TICKERS = [
    "AAPL", "MSFT", "AMZN", "JPM", "V",
    "CVX", "JNJ", "PG", "WMT", "CAT"
]

NUM_PORTFOLIOS = 5000
TRADING_DAYS = 252
RANDOM_SEED = 42

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

np.random.seed(RANDOM_SEED)

# ==========================================================
# 2. CARGAR RENDIMIENTOS HISTORICOS
# ==========================================================

print("\nCargando rendimientos historicos...")

daily_returns = pd.read_csv(
    OUTPUT_DIR / "daily_returns.csv",
    index_col=0,
    parse_dates=True
)

# Asegurar orden de los activos
daily_returns = daily_returns[TICKERS]

# Verificar datos
if daily_returns.isna().any().any():
    raise ValueError("Existen valores faltantes.")

if daily_returns.empty:
    raise ValueError("El archivo de rendimientos esta vacio.")

if not np.isfinite(daily_returns.to_numpy()).all():
    raise ValueError("Existen valores no finitos.")

print("Datos cargados correctamente.")
print("Observaciones:", len(daily_returns))
print("Activos:", len(TICKERS))

# ==========================================================
# 3. OBTENER TASA LIBRE DE RIESGO
# ==========================================================

print("\nDescargando tasa Treasury a 3 meses...")

start_date = daily_returns.index.min().strftime("%Y-%m-%d")

# Yahoo Finance: ^IRX representa el rendimiento
# de los Treasury Bills estadounidenses a 13 semanas.

rf_data = yf.download(
    "^IRX",
    start=start_date,
    auto_adjust=False,
    progress=False,
    threads=False
)

if rf_data.empty:
    raise ValueError(
        "No fue posible descargar la tasa libre de riesgo."
    )

# Extraer columna Close
rf_close = rf_data["Close"]

if isinstance(rf_close, pd.DataFrame):
    rf_close = rf_close.iloc[:, 0]

# Alinear las fechas con nuestros rendimientos
rf_close.index = pd.to_datetime(rf_close.index).tz_localize(None)

rf_aligned = rf_close.reindex(
    daily_returns.index
).ffill()

if rf_aligned.isna().any():
    raise ValueError("Faltan datos de la tasa libre de riesgo.")

# ^IRX expresa el rendimiento en porcentaje anual.
# Convertir a decimal y calcular promedio anual del periodo.

risk_free_rate = rf_aligned.mean() / 100

print(
    f"Tasa libre de riesgo anual promedio: "
    f"{risk_free_rate:.4%}"
)

# ==========================================================
# 4. GENERAR 5000 PORTAFOLIOS ALEATORIOS
# ==========================================================

print("\nGenerando portafolios aleatorios...")

# Distribucion Dirichlet:
# Todos los pesos son positivos y suman exactamente 1.

weights = np.random.dirichlet(
    alpha=np.ones(len(TICKERS)),
    size=NUM_PORTFOLIOS
)

print("Portafolios generados:", len(weights))

# ==========================================================
# 5. CALCULAR RENDIMIENTOS DIARIOS DE LOS PORTAFOLIOS
# ==========================================================

print("\nCalculando rendimientos diarios...")

# Matriz:
# Filas = fechas
# Columnas = activos

returns_matrix = daily_returns.to_numpy()

# Matriz:
# Filas = portafolios
# Columnas = activos

# Resultado:
# Filas = fechas
# Columnas = portafolios

portfolio_daily_returns = returns_matrix @ weights.T

# ==========================================================
# 6. CALCULAR RENDIMIENTO ANUAL ESPERADO
# ==========================================================

print("\nCalculando rendimiento esperado...")

expected_returns = (
    portfolio_daily_returns.mean(axis=0)
    * TRADING_DAYS
)

# ==========================================================
# 7. CALCULAR RIESGO ANUAL
# ==========================================================

print("\nCalculando riesgo...")

annual_risks = (
    portfolio_daily_returns.std(axis=0, ddof=1)
    * np.sqrt(TRADING_DAYS)
)

# ==========================================================
# 8. CALCULAR RATIO DE SHARPE
# ==========================================================

print("\nCalculando ratios de Sharpe...")

sharpe_ratios = (
    expected_returns - risk_free_rate
) / annual_risks

# ==========================================================
# 9. CONSTRUIR TABLA DE RESULTADOS
# ==========================================================

results = pd.DataFrame({
    "Portfolio_ID": np.arange(1, NUM_PORTFOLIOS + 1),
    "Retorno_anual_esperado": expected_returns,
    "Riesgo_anual": annual_risks,
    "Ratio_de_sharpe": sharpe_ratios
})

# Agregar los pesos de los diez activos

for i, ticker in enumerate(TICKERS):
    results[f"Weight_{ticker}"] = weights[:, i]

# ==========================================================
# 10. EXPORTAR OUTPUT 1
# ==========================================================

results.to_csv(
    OUTPUT_DIR / "markowitz_optimization_results.csv",
    index=False,
    float_format="%.10f"
)

print("\nCSV de Markowitz exportado correctamente.")

# ==========================================================
# 11. IDENTIFICAR PORTAFOLIOS SELECCIONADOS
# ==========================================================

print("\nSeleccionando portafolios...")

# A. Maximo Sharpe
idx_max_sharpe = results[
    "Ratio_de_sharpe"
].idxmax()

# B. Minima varianza
idx_min_risk = results[
    "Riesgo_anual"
].idxmin()

# C. Maximo rendimiento
idx_max_return = results[
    "Retorno_anual_esperado"
].idxmax()

# D. Portafolio equilibrado:
# Distancia minima al punto ideal.
# Rendimiento maximo y riesgo minimo.
# Ambas variables se normalizan para compararlas.

return_range = (
    results["Retorno_anual_esperado"].max()
    - results["Retorno_anual_esperado"].min()
)

risk_range = (
    results["Riesgo_anual"].max()
    - results["Riesgo_anual"].min()
)

if return_range == 0 or risk_range == 0:
    raise ValueError("No se pueden normalizar las metricas.")

normalized_return = (
    results["Retorno_anual_esperado"]
    - results["Retorno_anual_esperado"].min()
) / return_range

normalized_risk = (
    results["Riesgo_anual"]
    - results["Riesgo_anual"].min()
) / risk_range

distance_to_ideal = np.sqrt(
    (1 - normalized_return) ** 2
    + normalized_risk ** 2
)

idx_balanced = distance_to_ideal.idxmin()

# Construir tabla de seleccion

selected = pd.concat([
    results.loc[[idx_max_sharpe]].assign(
        Criterio="Maximo_Sharpe"
    ),
    results.loc[[idx_min_risk]].assign(
        Criterio="Minima_Varianza"
    ),
    results.loc[[idx_max_return]].assign(
        Criterio="Maximo_Rendimiento"
    ),
    results.loc[[idx_balanced]].assign(
        Criterio="Equilibrado"
    )
], ignore_index=True)

selected.to_csv(
    OUTPUT_DIR / "selected_portfolios.csv",
    index=False,
    float_format="%.10f"
)

# ==========================================================
# 12. GRAFICAR FRONTERA EFICIENTE
# ==========================================================

print("\nGenerando grafica de Markowitz...")

# Ordenar por riesgo
sorted_results = results.sort_values("Riesgo_anual")

# Aproximacion de la frontera eficiente:
# conservar portafolios que superan el mayor
# rendimiento encontrado para riesgos iguales o menores.

efficient_mask = (
    sorted_results["Retorno_anual_esperado"]
    > sorted_results["Retorno_anual_esperado"]
      .cummax().shift(1).fillna(-np.inf)
)

efficient_frontier = sorted_results[efficient_mask]

plt.figure(figsize=(12, 7))

plt.scatter(
    results["Riesgo_anual"] * 100,
    results["Retorno_anual_esperado"] * 100,
    c=results["Ratio_de_sharpe"],
    cmap="viridis",
    s=12,
    alpha=0.55,
    label="Portafolios simulados"
)

plt.plot(
    efficient_frontier["Riesgo_anual"] * 100,
    efficient_frontier["Retorno_anual_esperado"] * 100,
    color="red",
    linewidth=2,
    label="Frontera eficiente aproximada"
)

# Marcar portafolios seleccionados

plt.scatter(
    results.loc[idx_max_sharpe, "Riesgo_anual"] * 100,
    results.loc[idx_max_sharpe, "Retorno_anual_esperado"] * 100,
    color="gold",
    edgecolor="black",
    s=150,
    marker="*",
    label="Maximo Sharpe"
)

plt.scatter(
    results.loc[idx_min_risk, "Riesgo_anual"] * 100,
    results.loc[idx_min_risk, "Retorno_anual_esperado"] * 100,
    color="blue",
    edgecolor="black",
    s=90,
    marker="D",
    label="Minima varianza"
)

plt.scatter(
    results.loc[idx_max_return, "Riesgo_anual"] * 100,
    results.loc[idx_max_return, "Retorno_anual_esperado"] * 100,
    color="green",
    edgecolor="black",
    s=90,
    marker="^",
    label="Maximo rendimiento"
)

plt.xlabel("Riesgo anual (%)")
plt.ylabel("Rendimiento anual esperado (%)")

plt.title("Simulacion Monte Carlo - Frontera Eficiente de Markowitz")

plt.colorbar(
    label="Ratio de Sharpe"
)

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "markowitz_efficient_frontier.png",
    dpi=300
)

plt.show()

# ==========================================================
# 13. MOSTRAR RESULTADOS
# ==========================================================

print("\n==========================================")
print("RESUMEN DE LA SIMULACION DE MARKOWITZ")
print("==========================================")

print("\nPortafolios generados:", len(results))

print("\nPortafolios seleccionados:")

print(
    selected[
        [
            "Criterio",
            "Portfolio_ID",
            "Retorno_anual_esperado",
            "Riesgo_anual",
            "Ratio_de_sharpe"
        ]
    ].to_string(index=False)
)

print("\nArchivos generados:")

print("- markowitz_optimization_results.csv")
print("- selected_portfolios.csv")
print("- markowitz_efficient_frontier.png")

print("\nSimulacion completada correctamente.")
