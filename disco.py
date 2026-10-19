import json
import os
from logger import Logger


class Disco:
    TIPO_TXT = 505
    TIPO_PNG = 606
    TIPO_PY = 707
    TIPO_ASM = 808
    TIPO_DESCONOCIDO = 404
    CABECERA = 3

    def __init__(self, ruta="Backup.json"):
        self.ruta = ruta
        self.memoria = []
        self.archivos = {}
        self.carpetas = {}
        self.log = Logger()
        self._inicializar_raiz()
        self.cargar()

    def _inicializar_raiz(self):
        self.carpetas = {"/": {"nombre": "/", "padre": None}}

    def hash_nombre(self, nombre):
        if not isinstance(nombre, str):
            print(self.log.error("DISCO", "El nombre debe ser string"))
            return None
        total = 0
        for i, letra in enumerate(nombre):
            total += ord(letra) * (256 ** i)
        return total

    def detectar_tipo(self, nombre):
        if nombre.endswith(".txt"):
            return self.TIPO_TXT
        if nombre.endswith(".png"):
            return self.TIPO_PNG
        if nombre.endswith(".py"):
            return self.TIPO_PY
        if nombre.endswith(".asm"):
            return self.TIPO_ASM
        return self.TIPO_DESCONOCIDO

    def _normalizar(self, ruta, cwd="/"):
        if not isinstance(ruta, str) or not ruta:
            print(self.log.error("DISCO", "Ruta inválida"))
            return None
        if not ruta.startswith("/"):
            base = cwd.rstrip("/")
            ruta = (base + "/" + ruta) if base else "/" + ruta
        partes = [p for p in ruta.split("/") if p and p != "."]
        resultado = "/"
        for parte in partes:
            if parte == "..":
                resultado = resultado.rsplit("/", 1)[0] or "/"
            else:
                resultado = (resultado.rstrip("/") + "/" + parte) if resultado != "/" else "/" + parte
        return resultado

    def _padre(self, ruta):
        if ruta == "/":
            return None
        return ruta.rsplit("/", 1)[0] or "/"

    def _base(self, ruta):
        if ruta == "/":
            return "/"
        return ruta.rsplit("/", 1)[-1]

    def crear_carpeta(self, ruta, cwd="/"):
        ruta = self._normalizar(ruta, cwd)
        if ruta is None:
            return False
        if ruta == "/":
            print(self.log.warn("DISCO", "La raíz ya existe"))
            return False
        if ruta in self.carpetas:
            print(self.log.warn("DISCO", f"Carpeta ya existe: {ruta}"))
            return False
        padre = self._padre(ruta)
        if padre not in self.carpetas:
            print(self.log.error("DISCO", f"Padre no existe: {padre}"))
            return False
        self.carpetas[ruta] = {"nombre": self._base(ruta), "padre": padre}
        return True

    def borrar_carpeta(self, ruta, cwd="/"):
        ruta = self._normalizar(ruta, cwd)
        if ruta is None or ruta == "/":
            print(self.log.error("DISCO", "No se puede borrar la raíz"))
            return False
        if ruta not in self.carpetas:
            print(self.log.warn("DISCO", f"Carpeta no existe: {ruta}"))
            return False

        hijos = [r for r in self.carpetas if r.startswith(ruta + "/")]
        archivos_dentro = [
            h for h, info in self.archivos.items()
            if info["ruta"] == ruta or info["ruta"].startswith(ruta + "/")
        ]
        if hijos or archivos_dentro:
            print(self.log.error("DISCO", "Carpeta no vacía"))
            return False

        del self.carpetas[ruta]
        return True

    def existe_carpeta(self, ruta, cwd="/"):
        ruta = self._normalizar(ruta, cwd)
        return ruta is not None and ruta in self.carpetas

    def existe(self, ruta, cwd="/"):
        ruta = self._normalizar(ruta, cwd)
        if ruta is None:
            return False
        hash_nombre = self.hash_nombre(ruta)
        return hash_nombre in self.archivos

    def crear(self, ruta, datos, cwd="/"):
        ruta = self._normalizar(ruta, cwd)
        if ruta is None:
            return False
        if isinstance(datos, str):
            datos = datos.encode()
        if not isinstance(datos, (bytes, bytearray)):
            print(self.log.error("DISCO", "Datos deben ser bytes o string"))
            return False

        padre = self._padre(ruta)
        if padre not in self.carpetas:
            print(self.log.error("DISCO", f"Padre no existe: {padre}"))
            return False

        hash_nombre = self.hash_nombre(ruta)
        if hash_nombre in self.archivos:
            self.borrar(ruta)

        inicio = len(self.memoria)
        self.memoria.append(self.detectar_tipo(ruta))
        self.memoria.append(len(datos))
        self.memoria.append(hash_nombre)
        self.memoria.extend(datos)

        self.archivos[hash_nombre] = {
            "nombre": self._base(ruta),
            "ruta": ruta,
            "inicio": inicio,
            "longitud": len(datos),
        }
        return True

    def leer(self, ruta, cwd="/"):
        ruta = self._normalizar(ruta, cwd)
        if ruta is None:
            return None
        hash_nombre = self.hash_nombre(ruta)
        if hash_nombre not in self.archivos:
            return None
        info = self.archivos[hash_nombre]
        inicio = info["inicio"] + self.CABECERA
        fin = inicio + info["longitud"]
        if fin > len(self.memoria):
            print(self.log.error("DISCO", "Archivo corrupto en memoria"))
            return None
        return bytes(self.memoria[inicio:fin])

    def borrar(self, ruta, cwd="/"):
        ruta = self._normalizar(ruta, cwd)
        if ruta is None:
            return False
        hash_nombre = self.hash_nombre(ruta)
        if hash_nombre not in self.archivos:
            return False

        info = self.archivos[hash_nombre]
        inicio = info["inicio"]
        bloque = info["longitud"] + self.CABECERA
        del self.memoria[inicio:inicio + bloque]

        for otro in self.archivos.values():
            if otro["inicio"] > inicio:
                otro["inicio"] -= bloque

        del self.archivos[hash_nombre]
        return True

    def listar(self, ruta="/", cwd="/"):
        ruta = self._normalizar(ruta, cwd)
        if ruta is None:
            return []
        resultado = []
        for carpeta, info in self.carpetas.items():
            if carpeta == "/":
                continue
            if info["padre"] == ruta:
                resultado.append({"nombre": info["nombre"], "tipo": "carpeta", "ruta": carpeta})
        for info in self.archivos.values():
            padre = info["ruta"].rsplit("/", 1)[0] or "/"
            if padre == ruta:
                resultado.append({
                    "nombre": info["nombre"],
                    "tipo": "archivo",
                    "ruta": info["ruta"],
                    "longitud": info["longitud"],
                })
        resultado.sort(key=lambda e: (e["tipo"] != "carpeta", e["nombre"]))
        return resultado

    def numero_archivos(self):
        return len(self.archivos)

    def numero_carpetas(self):
        return len(self.carpetas) - 1

    def bytes_totales(self):
        return sum(info["longitud"] for info in self.archivos.values())

    def ruta_existe(self, ruta, cwd="/"):
        ruta = self._normalizar(ruta, cwd)
        if ruta is None:
            return False
        return ruta == "/" or ruta in self.carpetas or self.existe(ruta, cwd="/")

    def arbol(self, ruta="/"):
        """
        Devuelve una estructura anidada:
        {
            "nombre": "/",
            "tipo": "carpeta",
            "hijos": [
                {"nombre": "docs", "tipo": "carpeta", "hijos": [...]},
                {"nombre": "a.txt", "tipo": "archivo", "longitud": 12},
            ]
        }
        """
        ruta = self._normalizar(ruta, "/")
        if ruta is None:
            return None
        if ruta != "/" and ruta not in self.carpetas:
            return None

        def construir(actual):
            nodo = {
                "nombre": "/" if actual == "/" else self._base(actual),
                "tipo": "carpeta",
                "ruta": actual,
                "hijos": [],
            }
            for carpeta, info in self.carpetas.items():
                if carpeta == "/":
                    continue
                if info["padre"] == actual:
                    nodo["hijos"].append(construir(carpeta))
            for info in self.archivos.values():
                padre = info["ruta"].rsplit("/", 1)[0] or "/"
                if padre == actual:
                    nodo["hijos"].append({
                        "nombre": info["nombre"],
                        "tipo": "archivo",
                        "ruta": info["ruta"],
                        "longitud": info["longitud"],
                    })
            nodo["hijos"].sort(key=lambda e: (e["tipo"] != "carpeta", e["nombre"]))
            return nodo

        return construir(ruta)

    def guardar(self):
        datos = {
            "memoria": self.memoria,
            "carpetas": [
                {"ruta": r, "padre": info["padre"]}
                for r, info in self.carpetas.items()
            ],
            "archivos": [
                {
                    "hash": hash_archivo,
                    "nombre": info["nombre"],
                    "ruta": info["ruta"],
                    "inicio": info["inicio"],
                    "longitud": info["longitud"],
                }
                for hash_archivo, info in self.archivos.items()
            ],
        }
        try:
            with open(self.ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4)
            return True
        except OSError:
            print(self.log.error("DISCO", "No se pudo escribir backup"))
            return False

    def cargar(self):
        if not os.path.exists(self.ruta):
            return False
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except (OSError, json.JSONDecodeError):
            print(self.log.warn("DISCO", "Backup corrupto, disco vacío"))
            self._inicializar_raiz()
            self.memoria = []
            self.archivos = {}
            return False

        memoria = datos.get("memoria")
        carpetas = datos.get("carpetas")
        archivos = datos.get("archivos")

        if not isinstance(memoria, list):
            print(self.log.warn("DISCO", "Backup sin memoria válida"))
            memoria = []

        self._inicializar_raiz()

        if isinstance(carpetas, list):
            for entrada in carpetas:
                try:
                    ruta = entrada["ruta"]
                    padre = entrada["padre"]
                except (KeyError, TypeError):
                    continue
                if not isinstance(ruta, str) or ruta == "/":
                    continue
                if not isinstance(padre, (str, type(None))):
                    continue
                self.carpetas[ruta] = {"nombre": self._base(ruta), "padre": padre}

        self.memoria = memoria
        self.archivos = {}
        if isinstance(archivos, list):
            for entrada in archivos:
                try:
                    hash_archivo = entrada["hash"]
                    nombre = entrada["nombre"]
                    inicio = entrada["inicio"]
                    longitud = entrada["longitud"]
                except (KeyError, TypeError):
                    continue
                ruta = entrada.get("ruta")
                if not isinstance(ruta, str):
                    ruta = "/" + nombre
                if not isinstance(inicio, int) or not isinstance(longitud, int):
                    continue
                if inicio < 0 or longitud < 0:
                    continue
                if inicio + self.CABECERA + longitud > len(self.memoria):
                    continue
                self.archivos[hash_archivo] = {
                    "nombre": nombre,
                    "ruta": ruta,
                    "inicio": inicio,
                    "longitud": longitud,
                }
        return True