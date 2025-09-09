import sys
from typing import Optional
from api import SuelosAPI

class SuelosUI:
    """Interfaz de usuario en consola para consulta de variables edáficas."""

    def __init__(self, api: SuelosAPI):
        self.api = api

    def mostrar_banner(self):
        print("\n" + "="*70)
        print("ANÁLISIS DE VARIABLES EDÁFICAS - SUELOS COLOMBIA".center(70))
        print("="*70)

    def mostrar_menu_principal(self):
        print("\nMenú Principal")
        print("-"*40)
        print("1. Consultar variables edáficas")
        print("2. Salir")
        print("-"*40)

    def obtener_opcion_menu(self) -> int:
        while True:
            try:
                opcion = int(input("Seleccione opción (1-2): "))
                if opcion in [1, 2]:
                    return opcion
                print("Opción inválida.")
            except ValueError:
                print("Ingrese un número válido.")

    def seleccionar_departamento(self) -> Optional[str]:
        departamentos = self.api.obtener_departamentos()
        if not departamentos:
            print("No hay departamentos disponibles.")
            return None
        print("\nDepartamentos disponibles:")
        for i, d in enumerate(departamentos, 1):
            print(f"{i}. {d}")
        while True:
            try:
                op = int(input(f"Seleccione departamento (1-{len(departamentos)}): "))
                if 1 <= op <= len(departamentos):
                    return departamentos[op-1]
            except ValueError:
                pass
            print("Opción inválida.")

    def seleccionar_municipio(self, departamento: str) -> Optional[str]:
        municipios = self.api.obtener_municipios(departamento)
        if not municipios:
            print("No hay municipios disponibles.")
            return None
        print(f"\nMunicipios en {departamento}:")
        for i, m in enumerate(municipios, 1):
            print(f"{i}. {m}")
        while True:
            try:
                op = int(input(f"Seleccione municipio (1-{len(municipios)}): "))
                if 1 <= op <= len(municipios):
                    return municipios[op-1]
            except ValueError:
                pass
            print("Opción inválida.")

    def seleccionar_cultivo(self, departamento: str, municipio: str) -> Optional[str]:
        cultivos = self.api.obtener_cultivos(departamento, municipio)
        if not cultivos:
            print("No hay cultivos disponibles.")
            return None
        print(f"\nCultivos en {municipio}, {departamento}:")
        for i, c in enumerate(cultivos, 1):
            print(f"{i}. {c}")
        while True:
            try:
                op = int(input(f"Seleccione cultivo (1-{len(cultivos)}): "))
                if 1 <= op <= len(cultivos):
                    return cultivos[op-1]
            except ValueError:
                pass
            print("Opción inválida.")

    def obtener_numero_registros(self, departamento: str, municipio: str, cultivo: str) -> int:
        """Pregunta cuántos registros usar según el total disponible."""
        try:
            df = self.api.consultar_datos_edaficos(departamento, municipio, cultivo, num_registros=1000000)
            total = len(df)
        except Exception:
            print("No se pudo determinar la cantidad de registros disponibles.")
            return 0

        print(f"\nSe encontraron {total} registros disponibles para {cultivo} en {municipio}, {departamento}.")

        while True:
            try:
                n = int(input(f"Ingrese número de registros a consultar (1-{total}): "))
                if 1 <= n <= total:
                    return n
            except ValueError:
                pass
            print(f"Ingrese un número válido entre 1 y {total}.")

    def mostrar_tabla_resultados(self, departamento: str, municipio: str, cultivo: str, num_registros: int):
        try:
            medianas = self.api.calcular_medianas(departamento, municipio, cultivo, num_registros)
            topologia = self.api.obtener_topologia(departamento, municipio, cultivo)

            print("\nRESULTADOS DE LA CONSULTA")
            print("="*70)
            print(f"Departamento : {departamento}")
            print(f"Municipio    : {municipio}")
            print(f"Cultivo      : {cultivo}")
            print(f"Topología    : {topologia}")
            print("-"*70)
            print("Medianas de Variables Edáficas")
            print("-"*70)
            for var in ["pH", "Fósforo(P)", "Potasio(K)"]:
                valor = medianas.get(var, None)
                if valor is not None:
                    print(f"{var:<12}: {valor:.3f}")
                else:
                    print(f"{var:<12}: N/A")
            print("="*70)
            print(f"Registros usados: {num_registros}")
        except Exception as e:
            print(f"Error mostrando resultados: {e}")

    def ejecutar_consulta(self):
        departamento = self.seleccionar_departamento()
        if not departamento:
            return
        municipio = self.seleccionar_municipio(departamento)
        if not municipio:
            return
        cultivo = self.seleccionar_cultivo(departamento, municipio)
        if not cultivo:
            return
        num_registros = self.obtener_numero_registros(departamento, municipio, cultivo)
        self.mostrar_tabla_resultados(departamento, municipio, cultivo, num_registros)

    def ejecutar(self):
        self.mostrar_banner()
        while True:
            self.mostrar_menu_principal()
            opcion = self.obtener_opcion_menu()
            if opcion == 1:
                self.ejecutar_consulta()
            elif opcion == 2:
                print("\nFin del programa.")
                sys.exit(0)

