import os
from archivos import Archivos
from logger import Logger


class Memoria:
    CELDAS = 100000

    def __init__(self, ruta="memoria.json"):
        self.ruta = ruta
        self.memoria = [0] * self.CELDAS
        self.archivos = Archivos()
        self.log = Logger()
        self.cargar()

    def guardar(self):
        if self.archivos.escribir_json(self.ruta, self.memoria):
            return True
        print(self.log.error("MEMORIA", "No se pudo guardar"))
        return False

    def cargar(self):
        if not os.path.exists(self.ruta):
            return False
        datos = self.archivos.leer_json(self.ruta)
        if not isinstance(datos, list):
            print(self.log.warn("MEMORIA", "Backup inválido, memoria limpia"))
            return False
        if len(datos) != self.CELDAS:
            print(self.log.warn("MEMORIA", "Backup con tamaño incorrecto"))
            return False
        for valor in datos:
            if not isinstance(valor, (int, float)):
                print(self.log.warn("MEMORIA", "Backup con valores inválidos"))
                return False
        self.memoria = datos
        return True

    def limpiar(self):
        self.memoria = [0] * self.CELDAS
        return True

    def celdas_usadas(self):
        return sum(1 for celda in self.memoria if celda != 0)

    def porcentaje_usado(self):
        return (self.celdas_usadas() / self.CELDAS) * 100

    def leer(self, indice):
        if not isinstance(indice, int) or indice < 0 or indice >= self.CELDAS:
            print(self.log.error("MEMORIA", f"Índice inválido: {indice}"))
            return None
        return self.memoria[indice]

    def escribir(self, indice, valor):
        if not isinstance(indice, int) or indice < 0 or indice >= self.CELDAS:
            print(self.log.error("MEMORIA", f"Índice inválido: {indice}"))
            return False
        self.memoria[indice] = valor
        return True

    def celdas_no_cero(self):
        return {i: v for i, v in enumerate(self.memoria) if v != 0}