class Comandos:
    def __init__(self, partes, api):
        self.partes = partes
        self.api = api

    def _error(self, mensaje):
        print(self.api.log_modulo("SHELL", "ERROR", mensaje))

    def _warn(self, mensaje):
        print(self.api.log_modulo("SHELL", "WARN", mensaje))

    def _info(self, mensaje):
        print(self.api.log_modulo("SHELL", "INFO", mensaje))

    def a_int(self, string):
        try:
            return int(string)
        except (ValueError, TypeError):
            self._error("Se intentó usar un string como int")
            return None

    def unir(self, desde):
        resultado = []
        dentro = False
        for palabra in self.partes[desde:]:
            if palabra == "{":
                dentro = True
                continue
            if palabra == "}":
                break
            if dentro:
                resultado.append(palabra)
        return " ".join(resultado)

    def matriz(self, datos, ancho):
        if ancho <= 0:
            return []
        return [datos[i:i + ancho] for i in range(0, len(datos), ancho)]

    def ver_img(self, img):
        colores = {
            "0": "\033[48;5;0m  \033[0m",
            "2": "\033[48;5;88m  \033[0m",
            "3": "\033[48;5;160m  \033[0m",
            "4": "\033[48;5;196m  \033[0m",
            "5": "\033[48;5;211m  \033[0m",
        }
        for fila in img:
            print("".join(colores.get(v, "  ") for v in fila))

    # ------------------------- Carpetas y navegación -------------------------
    def pwd(self):
        print(self.api.pwd())

    def cd(self):
        if len(self.partes) < 2:
            self._info(f"Directorio actual: {self.api.pwd()}")
            return
        if self.api.cd(self.partes[1]):
            self._info(f"Directorio actual: {self.api.pwd()}")
        else:
            self._error(f"No se pudo cambiar a '{self.partes[1]}'")

    def mkdir(self):
        if len(self.partes) < 2:
            self._error("MKDIR sin argumentos")
            return
        if self.api.crear_carpeta(self.partes[1]):
            self._info("Carpeta creada")
        else:
            self._error("No se pudo crear la carpeta")

    def rmdir(self):
        if len(self.partes) < 2:
            self._error("RMDIR sin argumentos")
            return
        if self.api.borrar_carpeta(self.partes[1]):
            self._info("Carpeta eliminada")
        else:
            self._error("No se pudo eliminar la carpeta")

    def ls(self):
        ruta = self.partes[1] if len(self.partes) > 1 else None
        entradas = self.api.listar(ruta)
        if not entradas:
            self._info("Directorio vacío")
            return
        for entrada in entradas:
            if entrada["tipo"] == "carpeta":
                print(f"{self.api.color_ansi('azul')}[DIR] {entrada['nombre']}{self.api.color_ansi('reset')}")
            else:
                print(f"{self.api.color_ansi('cian')}[FILE] {entrada['nombre']} "
                      f"({entrada['longitud']} B){self.api.color_ansi('reset')}")

    def tree(self):
        """
        Dibuja el árbol de carpetas con conectores Unicode.
        Uso:
            tree          -> desde el directorio actual
            tree <ruta>   -> desde la ruta indicada
        """
        ruta = self.partes[1] if len(self.partes) > 1 else None
        nodo = self.api.arbol(ruta)
        if nodo is None:
            self._error("Ruta no existe")
            return

        cian = self.api.color_ansi("cian")
        azul = self.api.color_ansi("azul")
        gris = self.api.color_ansi("gris")
        reset = self.api.color_ansi("reset")

        print(f"{azul}{nodo['ruta']}{reset}")

        def _dibujar(hijos, prefijo=""):
            for i, hijo in enumerate(hijos):
                ultimo = (i == len(hijos) - 1)
                conector = "└── " if ultimo else "├── "
                if hijo["tipo"] == "carpeta":
                    etiqueta = f"{azul}{hijo['nombre']}/{reset}"
                else:
                    etiqueta = f"{cian}{hijo['nombre']}{reset} {gris}({hijo['longitud']} B){reset}"
                print(f"{prefijo}{conector}{etiqueta}")
                if hijo["tipo"] == "carpeta" and hijo["hijos"]:
                    extension = "    " if ultimo else "│   "
                    _dibujar(hijo["hijos"], prefijo + extension)

        if nodo["hijos"]:
            _dibujar(nodo["hijos"])

    # ------------------------- Sistema -------------------------
    def clear(self):
        self.api.limpiar_pantalla()

    def help(self):
        print(self.api.ayuda())

    def time(self):
        import time
        print(time.strftime("%Y-%m-%d %H:%M:%S"))

    def whoami(self):
        print(self.api.usuario())

    def version(self):
        print(self.api.version())

    def save(self):
        if self.api.guardar_disco():
            self._info("Disco guardado")
        else:
            self._error("No se pudo guardar el disco")

    def cargar(self):
        if self.api.cargar_disco():
            self._info("Disco cargado")
        else:
            self._warn("No se pudo cargar el disco")

    # ------------------------- Archivos -------------------------
    def write(self):
        if len(self.partes) < 2:
            self._error("WRITE sin argumentos")
            return
        ruta = self.partes[1]
        datos = self.unir(2).encode()
        if self.api.crear_archivo(ruta, datos):
            self._info(f"Archivo '{ruta}' creado")
        else:
            self._error(f"No se pudo crear '{ruta}'")

    def remove(self):
        if len(self.partes) < 2:
            self._error("REMOVE sin argumentos")
            return
        if self.api.borrar_archivo(self.partes[1]):
            self._info("Archivo eliminado")
        else:
            self._warn("Archivo no encontrado")

    def cat(self):
        if len(self.partes) < 2:
            self._error("CAT sin argumentos")
            return
        datos = self.api.leer_archivo(self.partes[1])
        if datos is None:
            self._warn("Archivo no encontrado")
            return
        try:
            print(datos.decode())
        except UnicodeDecodeError:
            print(datos)

    def touch(self):
        if len(self.partes) < 2:
            self._error("TOUCH sin argumentos")
            return
        if self.api.crear_archivo(self.partes[1], b""):
            self._info("Archivo vacío creado")
        else:
            self._error("No se pudo crear el archivo")

    def echo(self):
        if len(self.partes) < 1:
            self._error("ECHO sin argumentos")
            return
        print(self.unir(1))

    # ------------------------- Matemáticas -------------------------
    def _dos_numeros(self):
        if len(self.partes) < 3:
            self._error("Faltan argumentos")
            return None
        a = self.a_int(self.partes[1])
        b = self.a_int(self.partes[2])
        if a is None or b is None:
            return None
        return a, b

    def sum(self):
        par = self._dos_numeros()
        if par: print(par[0] + par[1])

    def rest(self):
        par = self._dos_numeros()
        if par: print(par[0] - par[1])

    def mult(self):
        par = self._dos_numeros()
        if par: print(par[0] * par[1])

    def div(self):
        par = self._dos_numeros()
        if not par: return
        if par[1] == 0:
            self._error("División inválida entre 0")
            return
        print(par[0] / par[1])

    def mod(self):
        par = self._dos_numeros()
        if not par: return
        if par[1] == 0:
            self._error("División inválida entre 0")
            return
        print(par[0] % par[1])

    def pow(self):
        par = self._dos_numeros()
        if par: print(par[0] ** par[1])

    def sqrt(self):
        if len(self.partes) < 2:
            self._error("Faltan argumentos")
            return
        n = self.a_int(self.partes[1])
        if n is None: return
        if n < 0:
            self._error("Raíz de negativo no soportada")
            return
        print(n ** 0.5)

    # ------------------------- Texto -------------------------
    def _texto(self):
        if len(self.partes) < 2:
            self._error("Faltan argumentos")
            return None
        return self.unir(1)

    def upper(self):
        t = self._texto()
        if t is not None: print(t.upper())

    def lower(self):
        t = self._texto()
        if t is not None: print(t.lower())

    def reverse(self):
        t = self._texto()
        if t is not None: print(t[::-1])

    def len(self):
        t = self._texto()
        if t is not None: print(len(t))

    def words(self):
        t = self._texto()
        if t is not None: print(len(t.split()))

    # ------------------------- Ejecución -------------------------
    def asm(self):
        if len(self.partes) < 2:
            self._error("ASM sin argumentos")
            return
        resultado = self.api.ejecutar_asm(self.partes[1], modo=True)
        if resultado is None:
            self._error("Falló la ejecución")

    def python(self):
        if len(self.partes) < 2:
            self._error("PYTHON sin argumentos")
            return
        datos = self.api.leer_archivo(self.partes[1])
        if not datos:
            self._warn("Archivo no encontrado")
            return
        try:
            codigo = datos.decode()
        except UnicodeDecodeError:
            self._error("Archivo no decodificable")
            return
        try:
            exec(codigo)
        except Exception as e:
            self._error(f"Error al ejecutar: {e}")

    # ------------------------- Imagen -------------------------
    def img(self):
        if len(self.partes) < 2:
            self._error("IMG sin argumentos")
            return
        cmd = self.partes[1]

        if cmd == "crear":
            if len(self.partes) < 5:
                self._error("img crear <n> <ancho> <alto>")
                return
            try:
                ancho = int(self.partes[3])
                alto = int(self.partes[4])
            except ValueError:
                self._error("Ancho y alto deben ser enteros")
                return
            if ancho <= 0 or alto <= 0:
                self._error("Ancho y alto deben ser positivos")
                return
            contenido = f"{self.partes[2]} {ancho} " + "0 " * (ancho * alto)
            self.api.crear_archivo(self.partes[2], contenido.encode())

        elif cmd == "ver":
            if len(self.partes) < 3:
                self._error("img ver <n>")
                return
            datos = self.api.leer_archivo(self.partes[2])
            if not datos:
                self._warn("Imagen no encontrada")
                return
            tokens = datos.decode().split()
            try:
                ancho = int(tokens[1])
            except (IndexError, ValueError):
                self._error("Cabecera de imagen inválida")
                return
            self.ver_img(self.matriz(tokens[2:], ancho))

        elif cmd == "pintar":
            if len(self.partes) < 6:
                self._error("img pintar <n> <x> <y> <color>")
                return
            datos = self.api.leer_archivo(self.partes[2])
            if not datos:
                self._warn("Imagen no encontrada")
                return
            tokens = datos.decode().split()
            try:
                ancho = int(tokens[1])
                x = int(self.partes[3])
                y = int(self.partes[4])
            except (IndexError, ValueError):
                self._error("Parámetros inválidos")
                return
            img = self.matriz(tokens[2:], ancho)
            if y < 0 or y >= len(img) or x < 0 or x >= len(img[y]):
                self._error("Coordenadas fuera de rango")
                return
            img[y][x] = self.partes[5]
            resultado = tokens[0] + " " + tokens[1] + " "
            for fila in img:
                resultado += " ".join(fila) + " "
            self.api.crear_archivo(self.partes[2], resultado.encode())

        else:
            self._error(f"Subcomando IMG desconocido: {cmd}")

    # ------------------------- Memoria -------------------------
    def mem(self):
        self.api.ver_memoria()

    def memload(self):
        if self.api.cargar_memoria():
            self._info("Memoria cargada")
        else:
            self._warn("No se pudo cargar memoria")

    def memsave(self):
        if self.api.guardar_memoria():
            self._info("Memoria guardada")
        else:
            self._error("No se pudo guardar memoria")

    def memclear(self):
        self.api.limpiar_memoria()
        self._info("Memoria limpiada")