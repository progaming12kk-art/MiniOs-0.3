from logger import Logger


class Ensamblador:
    OPCODES = {
        "SUMA":  "00001",
        "RESTA": "00010",
        "MULTI": "00011",
        "DIV":   "00100",
        "MOD":   "00101",
        "LOAD":  "00110",
        "JC":    "00111",
        "JUMP":  "01001",
        "JUMPI": "01010",
        "STORE": "01011",
        "SHL":   "01100",
        "SHR":   "01101",
        "SEE":   "01110",
        "OUT":   "01111",
        "CALL":  "10000",
        "RET":   "10001",
        "HALT":  "11111",
        ";":     "00000",
    }

    def __init__(self):
        self.log = Logger()

    def ensamblar(self, fuente):
        if isinstance(fuente, bytes):
            try:
                fuente = fuente.decode()
            except UnicodeDecodeError:
                print(self.log.error("ASM", "Fuente no decodificable"))
                return None
        if not isinstance(fuente, str):
            print(self.log.error("ASM", "Fuente debe ser string o bytes"))
            return None

        tokens = fuente.split()
        etiquetas = {}
        limpio = []

        for token in tokens:
            if token.endswith(":"):
                nombre = token[:-1]
                if not nombre:
                    print(self.log.error("ASM", "Etiqueta vacía"))
                    return None
                if nombre in etiquetas:
                    print(self.log.error("ASM", f"Etiqueta duplicada: '{nombre}'"))
                    return None
                etiquetas[nombre] = len(limpio)
            else:
                limpio.append(token)

        salida = []
        for token in limpio:
            if token in self.OPCODES:
                salida.append(self.OPCODES[token])
                continue
            if token in etiquetas:
                salida.append(bin(etiquetas[token])[2:])
                continue
            if token.isdigit():
                salida.append(bin(int(token))[2:])
                continue
            print(self.log.error("ASM", f"Símbolo no definido: '{token}'"))
            return None

        return " ".join(salida)