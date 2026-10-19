class Constantes:
    def __init__(self):
        self.vercion = 0.04
        self.usuario = "Kevin"
        self.ayuda = f"""
Ayuda del Mini OS v{self.vercion}

Sistema:
  help, clear, version, time, whoami, save, cargar

Carpetas:
  pwd                -> Muestra el directorio actual
  cd <ruta>          -> Cambia de directorio
  ls [ruta]          -> Lista contenido
  mkdir <ruta>       -> Crea carpeta
  rmdir <ruta>       -> Borra carpeta vacía
  tree [ruta]        -> Diagrama del árbol de carpetas

Archivos:
  cat <ruta>         -> Muestra contenido
  write <ruta> {{...}} -> Crea archivo
  remove <ruta>      -> Elimina archivo
  touch <ruta>       -> Crea archivo vacío

Ejecución:
  asm <ruta>         -> Ensambla y ejecuta ASM
  python <ruta>      -> Ejecuta Python

Texto: echo, upper, lower, reverse, len, words

Matemáticas: sum, rest, mult, div, mod, pow, sqrt

Imagen:
  img crear <n> <ancho> <alto>
  img ver <n>
  img pintar <n> <x> <y> <color>

Memoria: mem, memsave, memload, memclear
"""
        self.comandos = [
            "ls", "pwd", "cd", "mkdir", "rmdir", "tree",
            "write", "remove", "cat", "touch", "echo",
            "clear", "help", "time", "whoami", "version",
            "sum", "rest", "mult", "div", "mod", "pow", "sqrt",
            "upper", "lower", "reverse", "len", "words",
            "asm", "python", "save", "cargar",
            "img", "mem", "memsave", "memload", "memclear",
        ]
        self.bienvenida = (
            f"Mini OS v{self.vercion}\n"
            f"Usuario: {self.usuario}\n"
        )
        self.arbol = (
            "MiniOs\n"
            "├── main.py\n"
            "├── api.py\n"
            "├── disco.py\n"
            "├── memoria.py\n"
            "├── cpu.py\n"
            "└── ...\n"
        )