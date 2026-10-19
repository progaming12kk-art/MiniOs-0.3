class Logger:
    RESET = "\033[0m"

    TABLA = {
        "DEBUG": "\033[90m",
        "INFO": "\033[92m",
        "WARN": "\033[93m",
        "ERROR": "\033[91m",
    }

    def log(self, modulo, gravedad, mensaje):
        color = self.TABLA.get(gravedad, self.RESET)
        return f"{color}[{modulo}][{gravedad}]: {mensaje}{self.RESET}"

    def debug(self, modulo, mensaje):
        return self.log(modulo, "DEBUG", mensaje)

    def info(self, modulo, mensaje):
        return self.log(modulo, "INFO", mensaje)

    def warn(self, modulo, mensaje):
        return self.log(modulo, "WARN", mensaje)

    def error(self, modulo, mensaje):
        return self.log(modulo, "ERROR", mensaje)