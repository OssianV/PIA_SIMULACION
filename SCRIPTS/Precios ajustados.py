
# MÓDULO 1: OBTENCIÓN Y PREPARACIÓN DE DATOS
# ==========================================

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

# ------------------------------------------
# 1. CONFIGURACIÓN
# ------------------------------------------

TICKERS = [
    "MSFT", "AAPL", "AMZN", "JPM", "V",
    "CVX", "JNJ", "PG", "WMT", "CAT"
]

START_DATE = "2021-11-12"
END_DATE = "2026-11-13"

# Crear carpeta de resultados
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

# ------------------------------------------

# ------------------------------------------
# 2. DESCARGA INDIVIDUAL DE INFORMACIÓN
# ------------------------------------------

print("Descargando información de Yahoo Finance...")

price_data = {}

for ticker in TICKERS:

    print(f"\nDescargando {ticker}...")

    try:
        data = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            interval="1d",
            auto_adjust=False,
            actions=True,
            progress=False,
            threads=False,
            timeout=30,
            ignore_tz=True
        )

        if data.empty:
            print(f"ADVERTENCIA: No hay datos para {ticker}")
            continue

        if "Adj Close" not in data.columns:
            print(f"ADVERTENCIA: No existe Adj Close para {ticker}")
            continue

        price_data[ticker] = data["Adj Close"].squeeze()

        print(f"{ticker}: descarga exitosa")

    except Exception as e:
        print(f"ERROR descargando {ticker}: {e}")

# ------------------------------------------
# 3. CONSTRUCCIÓN DE MATRIZ DE PRECIOS
# ------------------------------------------

# Construir matriz de precios ajustados
adjusted_prices = pd.concat(
    price_data,
    axis=1
)

# Asignar nombres correctos
adjusted_prices.columns = list(price_data.keys())

# Ordenar activos
adjusted_prices = adjusted_prices.reindex(columns=TICKERS)

# Ordenar fechas
adjusted_prices = adjusted_prices.sort_index()

print("\nDimensiones de los precios:")
print(adjusted_prices.shape)

print("\nValores faltantes:")
print(adjusted_prices.isna().sum())

# Ordenar columnas
adjusted_prices = adjusted_prices.reindex(columns=TICKERS)

# Revisar activos descargados
missing_tickers = [
    ticker for ticker in TICKERS
    if ticker not in adjusted_prices.columns
    or adjusted_prices[ticker].isna().all()
]

if missing_tickers:
    raise ValueError(
        f"No se pudieron descargar estos activos: {missing_tickers}"
    )

print("\nDescarga completada.")
print("Dimensiones:", adjusted_prices.shape)

print("\nValores faltantes:")
print(adjusted_prices.isna().sum())


# ------------------------------------------
# 4. REVISIÓN DE CALIDAD DE LOS DATOS
# ------------------------------------------

print("\nDimensiones iniciales:")
print(adjusted_prices.shape)

print("\nValores faltantes por activo:")
print(adjusted_prices.isna().sum())

print("\nPrimeras observaciones:")
print(adjusted_prices.head())

# Eliminar fechas donde falte información
adjusted_prices = adjusted_prices.dropna(how="any")

# Comprobar que todos los activos tengan datos
if adjusted_prices.empty:
    raise ValueError("No existen observaciones completas.")

if adjusted_prices.isna().any().any():
    raise ValueError("Persisten valores faltantes.")

if (adjusted_prices <= 0).any().any():
    raise ValueError("Se encontraron precios no positivos.")

# ------------------------------------------
# 5. CALCULAR RENDIMIENTOS DIARIOS
# ------------------------------------------

daily_returns = adjusted_prices.pct_change(
    fill_method=None
).dropna()

# ------------------------------------------
# 6. ESTADÍSTICAS DESCRIPTIVAS
# ------------------------------------------

descriptive_stats = pd.DataFrame({
    "Rendimiento_diario_promedio": daily_returns.mean(),
    "Volatilidad_diaria": daily_returns.std(),
    "Rendimiento_anualizado": daily_returns.mean() * 252,
    "Volatilidad_anualizada": daily_returns.std() * np.sqrt(252)
})

print("\nEstadísticas descriptivas:")
print(descriptive_stats)

# ------------------------------------------
# 7. MATRIZ DE COVARIANZAS
# ------------------------------------------

covariance_matrix = daily_returns.cov()

print("\nMatriz de covarianzas:")
print(covariance_matrix)

# ------------------------------------------
# 8. EXPORTAR ARCHIVOS CSV
# ------------------------------------------

adjusted_prices.to_csv(
    OUTPUT_DIR / "adjusted_historical_prices.csv"
)

daily_returns.to_csv(
    OUTPUT_DIR / "daily_returns.csv"
)

descriptive_stats.to_csv(
    OUTPUT_DIR / "descriptive_statistics.csv"
)

covariance_matrix.to_csv(
    OUTPUT_DIR / "covariance_matrix.csv"
)

# ------------------------------------------
# 9. VISUALIZACIÓN DE PRECIOS
# ------------------------------------------

normalized_prices = (
    adjusted_prices / adjusted_prices.iloc[0]
) * 100

plt.figure(figsize=(14, 7))

for ticker in TICKERS:
    plt.plot(
        normalized_prices.index,
        normalized_prices[ticker],
        label=ticker
    )

plt.title("Evolución histórica de los 10 activos")
plt.xlabel("Fecha")
plt.ylabel("Valor de inversión (base 100)")
plt.legend(ncol=2)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# ------------------------------------------
# 10. MAPA DE CORRELACIONES
# ------------------------------------------

plt.figure(figsize=(11, 8))

sns.heatmap(
    daily_returns.corr(),
    annot=True,
    cmap="coolwarm",
    center=0,
    fmt=".2f"
)

plt.title("Matriz de correlaciones de los activos")
plt.tight_layout()
plt.show()

print("\n¡Preparación de datos completada!")
