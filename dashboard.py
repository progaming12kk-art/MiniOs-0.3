from api import API
from colores import Colores
from logger import Logger
import time
import os
import platform


class Dashboard:
    def __init__(self, api):
        self.api = api
        self.color = api.color
        self.log = api.log
        self.inicio = time.time()
        self.ancho = 30
        self.max_eventos = 10
        self.eventos = []

    def _linea(self):
        return self.color.gris + "-" * self.ancho + self.color.reset

    def _linea_doble(self):
        return self.color.cian + self.color.gruesa + "*" * self.ancho + self.color.reset

    def _titulo(self, texto):
        return self.color.cian + self.color.gruesa + texto.center(self.ancho) + self.color.reset

    def _subtitulo(self, texto):
        return f"  {self.color.gruesa}{self.color.azul}[{texto}]{self.color.reset}"

    def _campo(self, etiqueta, valor, ancho_etiq=12):
        return f"  {self.color.gris}{etiqueta:<{ancho_etiq}}{self.color.reset} {self.color.verde}{valor}{self.color.reset}"

    def _barra(self, porcentaje, ancho=20):
        porcentaje = max(0.0, min(100.0, porcentaje))
        llenos = int((porcentaje / 100) * ancho)
        vacios = ancho - llenos
        if porcentaje < 50:
            color = self.color.verde
        elif porcentaje < 80:
            color = self.color.amarillo
        else:
            color = self.color.rojo
        return color + "#" * llenos + self.color.gris + "." * vacios + self.color.reset

    def _estado(self, valor):
        return f"{self.color.verde}[OK]{self.color.reset}" if valor else f"{self.color.rojo}[NO]{self.color.reset}"

    def _formato_bytes(self, n):
        if n < 1024:
            return f"{n} B"
        if n < 1024 * 1024:
            return f"{n / 1024:.2f} KB"
        if n < 1024 * 1024 * 1024:
            return f"{n / (1024 * 1024):.2f} MB"
        return f"{n / (1024 * 1024 * 1024):.2f} GB"

    def _uptime(self):
        segundos = int(time.time() - self.inicio)
        h = segundos // 3600
        m = (segundos % 3600) // 60
        s = segundos % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def _registrar(self, modulo, gravedad, mensaje):
        self.eventos.append((time.strftime("%H:%M:%S"), modulo, gravedad, mensaje))
        if len(self.eventos) > self.max_eventos:
            self.eventos.pop(0)

    def _cabecera(self):
        print()
        print(self._linea_doble())
        print(self._titulo("MINI OS"))
        print(self._titulo("DASHBOARD"))
        print(self._linea_doble())

    def _sistema(self):
        print(self._linea())
        print(self._campo("Usuario:", self.api.usuario()))
        print(self._campo("Version:", f"v{self.api.version()}"))
        print(self._campo("Hora:", time.strftime("%Y-%m-%d %H:%M:%S")))
        print(self._campo("Uptime:", self._uptime()))
        print(self._campo("Plataforma:", platform.system()))
        print(self._campo("Python:", platform.python_version()))
        print(self._campo("PID:", os.getpid()))
        print(self._linea())

    def _memoria(self):
        usadas = self.api.numero_celdas_usadas()
        porcentaje = self.api.porcentaje_celdas_usadas()
        total = self.api.total_celdas()
        libres = total - usadas
        print(f"\n{self._subtitulo('MEMORIA')}")
        print(self._linea())
        print(self._campo("Total:", total))
        print(self._campo("Usadas:", usadas))
        print(self._campo("Libres:", libres))
        print(self._campo("Uso:", f"{porcentaje:.4f}%"))
        print(f"  {self._barra(porcentaje)} {porcentaje:.2f}%")
        print(self._linea())

    def _disco(self):
        num_archivos = self.api.numero_archivos()
        num_carpetas = self.api.numero_carpetas()
        celdas_disco = self.api.celdas_disco()
        total_bytes = self.api.bytes_disco()
        print(f"\n{self._subtitulo('DISCO')}")
        print(self._linea())
        print(self._campo("Backup:", self.api.ruta_disco()))
        print(self._campo("Archivos:", num_archivos))
        print(self._campo("Carpetas:", num_carpetas))
        print(self._campo("Celdas:", celdas_disco))
        print(self._campo("Bytes:", self._formato_bytes(total_bytes)))
        print(self._linea())
        if num_archivos > 0:
            print(f"\n{self._subtitulo('ARCHIVOS')}")
            print(self._linea())
            for info in self.api.archivos_disco():
                print(f"  {self.color.cian}{info['ruta']:<24}{self.color.reset} "
                      f"{self.color.gris}{self._formato_bytes(info['longitud'])}{self.color.reset}")
            print(self._linea())

    def _modulos(self):
        print(f"\n{self._subtitulo('MODULOS')}")
        print(self._linea())
        modulos = [
            "API", "CPU", "Ensamblador", "Memoria", "Disco", "Comandos",
            "Ejecutor", "Archivos", "Logger", "Colores", "Constantes", "Dashboard",
        ]
        for nombre in modulos:
            print(f"  {self._estado(True)} {self.color.cian}{nombre}{self.color.reset}")
        print(self._linea())

    def _log(self):
        print(f"\n{self._subtitulo('EVENTOS')}")
        print(self._linea())
        self._registrar("DASHBOARD", "INFO", "Dashboard renderizado")
        self._registrar("DISCO", "INFO", f"{self.api.numero_archivos()} archivos")
        self._registrar("MEMORIA", "INFO", f"{self.api.numero_celdas_usadas()} celdas")
        for hora, modulo, gravedad, mensaje in self.eventos:
            print(f"  {self.color.gris}{hora}{self.color.reset} "
                  f"{self.log.log(modulo, gravedad, mensaje)}")
        print(self._linea())

    def _pie(self):
        print(self._linea_doble())
        print(self.color.amarillo + "  Usa 'help' para ayuda" + self.color.reset)
        print(self.color.gris + f"  Mini OS v{self.api.version()} - {self.api.usuario()}" + self.color.reset)
        print(self._linea_doble())
        print()

    def dashboard(self):
        self._cabecera()
        self._sistema()
        self._memoria()
        self._disco()
        self._modulos()
        self._log()
        self._pie()