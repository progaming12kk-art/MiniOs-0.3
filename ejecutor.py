from comandos import Comandos


class Ejecutor:
    def __init__(self, comando, api):
        self.api = api
        self.partes = comando.strip().split()
        self.comandos = Comandos(self.partes, self.api)
        self.tabla = {
            "ls": self.comandos.ls,
            "pwd": self.comandos.pwd,
            "cd": self.comandos.cd,
            "mkdir": self.comandos.mkdir,
            "rmdir": self.comandos.rmdir,
            "tree": self.comandos.tree,
            "write": self.comandos.write,
            "remove": self.comandos.remove,
            "cat": self.comandos.cat,
            "touch": self.comandos.touch,
            "echo": self.comandos.echo,
            "clear": self.comandos.clear,
            "help": self.comandos.help,
            "time": self.comandos.time,
            "whoami": self.comandos.whoami,
            "version": self.comandos.version,
            "sum": self.comandos.sum,
            "rest": self.comandos.rest,
            "mult": self.comandos.mult,
            "div": self.comandos.div,
            "mod": self.comandos.mod,
            "pow": self.comandos.pow,
            "sqrt": self.comandos.sqrt,
            "upper": self.comandos.upper,
            "lower": self.comandos.lower,
            "reverse": self.comandos.reverse,
            "len": self.comandos.len,
            "words": self.comandos.words,
            "asm": self.comandos.asm,
            "python": self.comandos.python,
            "save": self.comandos.save,
            "cargar": self.comandos.cargar,
            "img": self.comandos.img,
            "mem": self.comandos.mem,
            "memsave": self.comandos.memsave,
            "memload": self.comandos.memload,
            "memclear": self.comandos.memclear,
        }

    def ejecutar(self):
        if not self.partes:
            return
        cmd = self.partes[0].lower()
        if cmd in self.tabla:
            try:
                self.tabla[cmd]()
            except Exception as e:
                print(self.api.log_modulo("SHELL", "ERROR", f"Error interno: {e}"))
        else:
            print(self.api.log_modulo("SHELL", "ERROR", f"Comando '{cmd}' no reconocido"))