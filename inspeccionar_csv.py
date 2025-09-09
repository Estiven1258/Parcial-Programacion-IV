#!/usr/bin/env python3
"""
Script para inspeccionar el archivo datos_parcial.csv
y mostrar su estructura real.
"""

import pandas as pd

def inspeccionar_csv():
    """Inspecciona el archivo CSV y muestra información detallada."""
    
    try:
        print("🔍 INSPECCIONANDO ARCHIVO: datos_parcial.csv")
        print("=" * 60)
        
        # Intentar cargar con diferentes encodings
        encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv('datos_parcial.csv', encoding=encoding)
                print(f"✅ Archivo cargado exitosamente con encoding: {encoding}")
                break
            except UnicodeDecodeError:
                print(f"❌ Error con encoding: {encoding}")
                continue
        
        if df is None:
            print("❌ No se pudo cargar el archivo con ningún encoding")
            return
        
        # Información básica
        print(f"\n📊 INFORMACIÓN GENERAL")
        print("-" * 40)
        print(f"Forma del dataset: {df.shape}")
        print(f"Total registros: {len(df)}")
        print(f"Total columnas: {len(df.columns)}")
        
        # Mostrar todas las columnas
        print(f"\n📋 COLUMNAS DISPONIBLES ({len(df.columns)} total)")
        print("-" * 40)
        for i, col in enumerate(df.columns, 1):
            print(f"{i:2d}. {col}")
        
        # Buscar columnas clave
        print(f"\n🔍 BÚSQUEDA DE COLUMNAS CLAVE")
        print("-" * 40)
        
        # Departamento
        dept_cols = [col for col in df.columns if any(term in col.lower() for term in ['departamento', 'depto', 'dept'])]
        print(f"Departamento: {dept_cols if dept_cols else 'No encontrado'}")
        
        # Municipio
        mun_cols = [col for col in df.columns if any(term in col.lower() for term in ['municipio', 'mpio', 'municipality'])]
        print(f"Municipio: {mun_cols if mun_cols else 'No encontrado'}")
        
        # Cultivo
        cult_cols = [col for col in df.columns if any(term in col.lower() for term in ['cultivo', 'crop', 'cultura'])]
        print(f"Cultivo: {cult_cols if cult_cols else 'No encontrado'}")
        
        # Variables edáficas
        ph_cols = [col for col in df.columns if 'ph' in col.lower()]
        p_cols = [col for col in df.columns if any(term in col.lower() for term in ['fosforo', 'fósforo', 'p', 'phosphorus'])]
        k_cols = [col for col in df.columns if any(term in col.lower() for term in ['potasio', 'k', 'potassium'])]
        
        print(f"pH: {ph_cols if ph_cols else 'No encontrado'}")
        print(f"Fósforo: {p_cols if p_cols else 'No encontrado'}")
        print(f"Potasio: {k_cols if k_cols else 'No encontrado'}")
        
        # Topología
        topo_cols = [col for col in df.columns if any(term in col.lower() for term in ['topologia', 'topography', 'relieve'])]
        print(f"Topología: {topo_cols if topo_cols else 'No encontrado'}")
        
        # Mostrar muestra de datos
        print(f"\n📄 MUESTRA DE DATOS (primeras 3 filas)")
        print("-" * 40)
        print(df.head(3).to_string())
        
        # Estadísticas básicas
        if dept_cols:
            print(f"\n📈 ESTADÍSTICAS")
            print("-" * 40)
            dept_col = dept_cols[0]
            print(f"Departamentos únicos: {df[dept_col].nunique()}")
            print(f"Departamentos: {list(df[dept_col].unique()[:10])}")  # Primeros 10
            
            if mun_cols:
                mun_col = mun_cols[0]
                print(f"Municipios únicos: {df[mun_col].nunique()}")
            
            if cult_cols:
                cult_col = cult_cols[0]
                print(f"Cultivos únicos: {df[cult_col].nunique()}")
                print(f"Cultivos: {list(df[cult_col].unique()[:10])}")  # Primeros 10
        
    except FileNotFoundError:
        print("❌ No se encontró el archivo 'datos_parcial.csv'")
        print("Asegúrese de que esté en el mismo directorio que este script")
    
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")


if __name__ == "__main__":
    inspeccionar_csv()