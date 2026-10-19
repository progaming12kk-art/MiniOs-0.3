from cpu import CPU
from ensamblador import Ensamblador
from memoria import Memoria
from disco import Disco
from constantes import Constantes
from colores import Colores
from logger import Logger


class API:
    def __init__(self, disco=None, constantes=None, centro=None):
        self.constantes = constantes if constantes is not None else Constantes()
        self.disco = disco if disco is not None else Disco()
        self.centro = centro
        self.ensamblador = Ensamblador()
        self.memoria = Memoria()
        self.color = Colores()
        self.log = Logger()
        self.cwd = "/" # Inicio 

    def pwd(self):
        return self.cwd # Ruta actual 

    def cd(self, ruta):
        normalizada = self.disco._normalizar(ruta, self.cwd)
        if normalizada is None:
            print(self.log.error("API", "Ruta no valida"))
            return False
        if not self.disco.ruta_existe(normalizada, cwd="/"):
            print(self.log.error("API", f"Ruta no existe: {normalizada}"))
            return False
        if normalizada != "/" and not self.disco.existe_carpeta(normalizada, cwd="/"):
            print(self.log.error("API", "Es un archivo"))
            return False
        self.cwd = normalizada
        return True

    def crear_archivo(self, ruta, datos):
        return self.disco.crear(ruta, datos, cwd=self.cwd)

    def leer_archivo(self, ruta):
        return self.disco.leer(ruta, cwd=self.cwd)

    def borrar_archivo(self, ruta):
        return self.disco.borrar(ruta, cwd=self.cwd)

    def listar(self, ruta=None):
        objetivo = ruta if ruta is not None else self.cwd
        return self.disco.listar(objetivo, cwd=self.cwd)

    def existe_archivo(self, ruta):
        return self.disco.existe(ruta, cwd=self.cwd)

    def crear_carpeta(self, ruta):
        return self.disco.crear_carpeta(ruta, cwd=self.cwd)

    def borrar_carpeta(self, ruta):
        return self.disco.borrar_carpeta(ruta, cwd=self.cwd)

    def existe_carpeta(self, ruta):
        return self.disco.existe_carpeta(ruta, cwd=self.cwd)

    def ruta_existe(self, ruta):
        return self.disco.ruta_existe(ruta, cwd=self.cwd)

    def arbol(self, ruta=None):
        objetivo = ruta if ruta is not None else self.cwd
        return self.disco.arbol(objetivo)

    # Disco
    def numero_archivos(self):
        return self.disco.numero_archivos()

    def numero_carpetas(self):
        return self.disco.numero_carpetas()

    def bytes_disco(self):
        return self.disco.bytes_totales()

    def guardar_disco(self):
        return self.disco.guardar()

    def cargar_disco(self):
        return self.disco.cargar()

    def ruta_disco(self):
        return self.disco.ruta

    def celdas_disco(self):
        return len(self.disco.memoria)

    def archivos_disco(self):
        return [
            {
                "hash": hash_archivo,
                "nombre": info["nombre"],
                "ruta": info["ruta"],
                "inicio": info["inicio"],
                "longitud": info["longitud"],
            }
            for hash_archivo, info in self.disco.archivos.items()
        ]

    # Ensamblador y CPU
    def ensamblar(self, fuente):
        return self.ensamblador.ensamblar(fuente)

    def _crear_proceso(self, binario, modo):
        programa = binario.split()
        if modo:
            return {"pc": 0, "programa": programa, "pila": [], "muerto": False}
        return {
            "memoria": [0] * self.memoria.CELDAS,
            "pc": 0,
            "programa": programa,
            "pila": [],
            "muerto": False,
        }

    def _ejecutar_fuente(self, fuente, modo):
        binario = self.ensamblar(fuente)
        if binario is None:
            return None
        proceso = self._crear_proceso(binario, modo)
        cpu = CPU(proceso, self.memoria.memoria) if modo else CPU(proceso)
        cpu.ejecutar()
        return cpu.a_dict()

    def ejecutar_asm(self, ruta, modo=False):
        if not self.existe_archivo(ruta):
            print(self.log.error("API", "Archivo no existe"))
            return None
        datos = self.leer_archivo(ruta)
        if datos is None:
            print(self.log.error("API", "Contenido inválido "))
            return None
        return self._ejecutar_fuente(datos, modo)

    def ejecutar_asm_inmediato(self, fuente, modo=False):
        return self._ejecutar_fuente(fuente, modo)

    # Constantes y utilidades
    def version(self):
        return self.constantes.vercion

    def usuario(self):
        return self.constantes.usuario

    def ayuda(self):
        return self.constantes.ayuda

    def bienvenida(self):
        return self.constantes.bienvenida

    def arbol_constantes(self):
        return self.constantes.arbol

    def comandos(self):
        return list(self.constantes.comandos)

    def limpiar_pantalla(self):
        print("\033[H\033[J", end="")

    def color_ansi(self, nombre):
        return getattr(self.color, nombre, "")

    def log_modulo(self, modulo, gravedad, mensaje):
        return self.log.log(modulo, gravedad, mensaje)

    # Memoria 
    def numero_celdas_usadas(self):
        return self.memoria.celdas_usadas()

    def porcentaje_celdas_usadas(self):
        return self.memoria.porcentaje_usado()

    def total_celdas(self):
        return self.memoria.CELDAS

    def ver_memoria(self):
        for indice, valor in self.memoria.celdas_no_cero().items():
            print(f"mem[{indice}] = {valor}")

    def guardar_memoria(self):
        return self.memoria.guardar()

    def cargar_memoria(self):
        return self.memoria.cargar()

    def limpiar_memoria(self):
        return self.memoria.limpiar()

    def memoria_celda(self, indice):
        return self.memoria.leer(indice)

    def memoria_escribir(self, indice, valor):
        return self.memoria.escribir(indice, valor)

    def memoria_no_cero(self):
        return self.memoria.celdas_no_cero()