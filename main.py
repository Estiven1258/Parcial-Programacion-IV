#!/usr/bin/env python3
"""
Proyecto Fundamentos Básicos de Python - Programación 4
Análisis de Variables Edáficas de Suelos en Colombia
"""

import sys
import pandas as pd

# Importar módulos propios
try:
    from api import SuelosAPI
    from ui import SuelosUI
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    sys.exit(1)


def verificar_dependencias():
    """Verifica que las dependencias necesarias estén instaladas."""
    dependencias = ['pandas', 'numpy']
    faltantes = []

    for dep in dependencias:
        try:
            __import__(dep)
        except ImportError:
            faltantes.append(dep)

    if faltantes:
        print("Faltan dependencias: " + ", ".join(faltantes))
        print(f"Instálelas con: pip install {' '.join(faltantes)}")
        return False
    return True


def cargar_datos_csv():
    """Carga los datos desde el CSV real, con detección flexible de separador/encoding."""
    ruta_csv = "datos_parcial.csv"
    print("\nCARGANDO DATOS REALES DE SUELOS")
    print("=" * 50)

    try:
        try:
            df = pd.read_csv(ruta_csv, sep=";", encoding="utf-8", engine="python", on_bad_lines="skip")
        except Exception:
            df = pd.read_csv(ruta_csv, sep=";", encoding="latin1", engine="python", on_bad_lines="skip")

        # Normalizar encabezados
        df.columns = [c.strip().lower() for c in df.columns]

        print(f"Datos cargados correctamente: {len(df)} registros.")
        return df

    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta_csv}")
        sys.exit(1)
    except Exception as e:
        print(f"Error cargando CSV: {e}")
        sys.exit(1)


def main():
    print("="*70)
    print("ANÁLISIS DE VARIABLES EDÁFICAS - SUELOS COLOMBIA".center(70))
    print("Universidad Tecnológica de Pereira".center(70))
    print("="*70)

    try:
        if not verificar_dependencias():
            sys.exit(1)

        # Cargar datos reales desde CSV
        df_datos = cargar_datos_csv()

        # Inicializar API
        api = SuelosAPI(dataframe=df_datos)

        # Ejecutar UI
        ui = SuelosUI(api)
        ui.ejecutar()

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError crítico: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

