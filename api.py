import pandas as pd
from typing import List, Dict

class SuelosAPI:
    """Módulo API para análisis de variables edáficas."""

    def __init__(self, dataframe: pd.DataFrame = None):
        self.df = None
        if dataframe is not None:
            self.df = dataframe.copy()
            self._normalizar_columnas()

    def _normalizar_columnas(self):
        self.df.columns = self.df.columns.str.strip().str.lower()

    def _norm(self, serie: pd.Series) -> pd.Series:
        return serie.astype(str).str.strip().str.casefold()

    def obtener_departamentos(self) -> List[str]:
        if self.df is None or "departamento" not in self.df.columns:
            return []
        return sorted(self.df["departamento"].dropna().unique().tolist())

    def obtener_municipios(self, departamento: str) -> List[str]:
        if self.df is None:
            return []
        mask = self._norm(self.df["departamento"]) == departamento.casefold()
        return sorted(self.df.loc[mask, "municipio"].dropna().unique().tolist())

    def obtener_cultivos(self, departamento: str, municipio: str) -> List[str]:
        if self.df is None:
            return []
        mask = (
            (self._norm(self.df["departamento"]) == departamento.casefold()) &
            (self._norm(self.df["municipio"]) == municipio.casefold())
        )
        return sorted(self.df.loc[mask, "cultivo"].dropna().unique().tolist())

    def consultar_datos_edaficos(self, departamento: str, municipio: str, cultivo: str, num_registros: int = 10):
        if self.df is None:
            raise Exception("No hay datos cargados")
        mask = (
            (self._norm(self.df["departamento"]) == departamento.casefold()) &
            (self._norm(self.df["municipio"]) == municipio.casefold()) &
            (self._norm(self.df["cultivo"]) == cultivo.casefold())
        )
        df_filtrado = self.df.loc[mask].copy()
        if df_filtrado.empty:
            raise Exception("No se encontraron datos para esos parámetros")
        return df_filtrado.head(num_registros)

    def calcular_medianas(self, departamento: str, municipio: str, cultivo: str, num_registros: int = None) -> Dict[str, float]:
        df_datos = self.consultar_datos_edaficos(departamento, municipio, cultivo, num_registros)
        medianas = {}

        col_ph = [c for c in df_datos.columns if "ph" in c.lower()]
        col_p = [c for c in df_datos.columns if "fosforo" in c.lower() or "fósforo" in c.lower() or c.lower() == "p"]
        col_k = [c for c in df_datos.columns if "potasio" in c.lower() or c.lower() == "k"]

        if col_ph:
            valores = pd.to_numeric(df_datos[col_ph[0]], errors="coerce").dropna()
            if not valores.empty:
                medianas["pH"] = valores.median()

        if col_p:
            valores = pd.to_numeric(df_datos[col_p[0]], errors="coerce").dropna()
            if not valores.empty:
                medianas["Fósforo(P)"] = valores.median()

        if col_k:
            valores = pd.to_numeric(df_datos[col_k[0]], errors="coerce").dropna()
            if not valores.empty:
                medianas["Potasio(K)"] = valores.median()

        return medianas

    def obtener_topologia(self, departamento: str, municipio: str, cultivo: str) -> str:
        try:
            df_datos = self.consultar_datos_edaficos(departamento, municipio, cultivo, 1)
            if "topologia" in df_datos.columns:
                return df_datos["topologia"].iloc[0]
            elif "topografia" in df_datos.columns:
                return df_datos["topografia"].iloc[0]
            return "N/A"
        except:
            return "N/A"


