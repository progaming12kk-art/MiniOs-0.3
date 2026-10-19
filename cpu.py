from logger import Logger


class CPU:
    def __init__(self, proceso, compartida=None):
        self.memoria = compartida if compartida is not None else proceso.get("memoria", [])
        self.pc = proceso.get("pc", 0)
        self.programa = proceso.get("programa", [])
        self.pila = proceso.get("pila", [])
        self.muerto = proceso.get("muerto", False)
        self.log = Logger()

        self.instrucciones = {
            "00001": (self.suma, 4),
            "00010": (self.resta, 4),
            "00011": (self.mult, 4),
            "00100": (self.div, 4),
            "00101": (self.mod, 4),
            "00110": (self.load, 3),
            "00111": (self.jc, 0),
            "01001": (self.jump, 0),
            "01010": (self.jumpi, 0),
            "01011": (self.store, 3),
            "01100": (self.shl, 4),
            "01101": (self.shr, 4),
            "01110": (self.see, 1),
            "01111": (self.out, 2),
            "10000": (self.call, 0),
            "10001": (self.ret, 0),
            "11111": (self.halt, 0),
        }

    def leer_indice(self, posicion):
        if posicion < 0 or posicion >= len(self.programa):
            return None
        try:
            return int(self.programa[posicion], 2)
        except (ValueError, TypeError):
            print(self.log.error("CPU", f"Índice inválido en posición {posicion}"))
            return None

    def verificar_memoria(self, *indices):
        for i in indices:
            if i is None or i < 0 or i >= len(self.memoria):
                print(self.log.error("CPU", "Índice de memoria fuera de rango"))
                return False
        return True

    def verificar_programa(self, destino):
        if destino is None or destino < 0 or destino >= len(self.programa):
            print(self.log.error("CPU", "Salto fuera de rango de programa"))
            return False
        return True

    def _tres_operandos(self):
        a = self.leer_indice(self.pc + 1)
        b = self.leer_indice(self.pc + 2)
        c = self.leer_indice(self.pc + 3)
        if None in (a, b, c):
            return None
        if not self.verificar_memoria(a, b, c):
            return None
        return a, b, c

    def suma(self):
        ops = self._tres_operandos()
        if ops is None: return
        a, b, c = ops
        self.memoria[c] = self.memoria[a] + self.memoria[b]

    def resta(self):
        ops = self._tres_operandos()
        if ops is None: return
        a, b, c = ops
        self.memoria[c] = self.memoria[a] - self.memoria[b]

    def mult(self):
        ops = self._tres_operandos()
        if ops is None: return
        a, b, c = ops
        self.memoria[c] = self.memoria[a] * self.memoria[b]

    def div(self):
        ops = self._tres_operandos()
        if ops is None: return
        a, b, c = ops
        if self.memoria[b] == 0:
            print(self.log.error("CPU", "División entre 0"))
            return
        self.memoria[c] = self.memoria[a] // self.memoria[b]

    def mod(self):
        ops = self._tres_operandos()
        if ops is None: return
        a, b, c = ops
        if self.memoria[b] == 0:
            print(self.log.error("CPU", "Módulo entre 0"))
            return
        self.memoria[c] = self.memoria[a] % self.memoria[b]

    def shl(self):
        ops = self._tres_operandos()
        if ops is None: return
        a, b, c = ops
        self.memoria[c] = self.memoria[a] << self.memoria[b]

    def shr(self):
        ops = self._tres_operandos()
        if ops is None: return
        a, b, c = ops
        self.memoria[c] = self.memoria[a] >> self.memoria[b]

    def jump(self):
        destino = self.leer_indice(self.pc + 1)
        if not self.verificar_programa(destino): return
        self.pc = destino

    def jumpi(self):
        indice = self.leer_indice(self.pc + 1)
        if not self.verificar_memoria(indice): return
        destino = self.memoria[indice]
        if not isinstance(destino, int):
            print(self.log.error("CPU", "Destino indirecto no entero"))
            return
        if not self.verificar_programa(destino): return
        self.pc = destino

    def jc(self):
        registro = self.leer_indice(self.pc + 1)
        if not self.verificar_memoria(registro): return
        if self.memoria[registro] == 0:
            destino = self.leer_indice(self.pc + 2)
        else:
            destino = self.leer_indice(self.pc + 3)
        if not self.verificar_programa(destino): return
        self.pc = destino

    def call(self):
        destino = self.leer_indice(self.pc + 1)
        if not self.verificar_programa(destino): return
        self.pila.append(self.pc + 2)
        self.pc = destino

    def ret(self):
        if not self.pila:
            print(self.log.error("CPU", "RET sin CALL"))
            self.muerto = True
            return
        self.pc = self.pila.pop()

    def load(self):
        i = self.leer_indice(self.pc + 1)
        v = self.leer_indice(self.pc + 2)
        if None in (i, v): return
        if not self.verificar_memoria(i): return
        self.memoria[i] = v

    def store(self):
        a = self.leer_indice(self.pc + 1)
        b = self.leer_indice(self.pc + 2)
        if None in (a, b): return
        if not self.verificar_memoria(a, b): return
        self.memoria[b] = self.memoria[a]

    def see(self):
        print({i: v for i, v in enumerate(self.memoria) if v != 0})

    def out(self):
        i = self.leer_indice(self.pc + 1)
        if not self.verificar_memoria(i): return
        print(self.memoria[i])

    def halt(self):
        self.muerto = True

    def ejecutar_instruccion(self):
        if self.pc < 0 or self.pc >= len(self.programa):
            self.muerto = True
            return
        opcode = self.programa[self.pc]
        if opcode not in self.instrucciones:
            print(self.log.error("CPU", f"Opcode desconocido '{opcode}'"))
            self.muerto = True
            return
        funcion, salto = self.instrucciones[opcode]
        funcion()
        if opcode in ("00111", "01001", "01010", "10000", "10001"):
            return
        self.pc += salto

    def ejecutar(self):
        while self.pc < len(self.programa) and not self.muerto:
            self.ejecutar_instruccion()

    def a_dict(self):
        return {
            "memoria": self.memoria,
            "pc": self.pc,
            "programa": self.programa,
            "pila": self.pila,
            "muerto": self.muerto,
        }