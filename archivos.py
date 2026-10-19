import os
import json


class Archivos:
    def crear(self, nombre, contenido):
        if os.path.exists(nombre):
            return False
        try:
            with open(nombre, "w", encoding="utf-8") as f:
                f.write(contenido)
            return True
        except (OSError, TypeError):
            return False

    def leer(self, nombre):
        if not os.path.exists(nombre):
            return None
        try:
            with open(nombre, "r", encoding="utf-8") as f:
                return f.read()
        except (OSError, UnicodeDecodeError):
            return None

    def escribir(self, nombre, contenido):
        if not os.path.exists(nombre):
            return False
        try:
            with open(nombre, "w", encoding="utf-8") as f:
                f.write(contenido)
            return True
        except (OSError, TypeError):
            return False

    def json(self, nombre, diccionario):
        if os.path.exists(nombre):
            return False
        try:
            with open(nombre, "w", encoding="utf-8") as f:
                json.dump(diccionario, f, indent=4)
            return True
        except (OSError, TypeError):
            return False

    def leer_json(self, nombre):
        if not os.path.exists(nombre):
            return None
        try:
            with open(nombre, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return None

    def escribir_json(self, nombre, diccionario):
        if not os.path.exists(nombre):
            return False
        try:
            with open(nombre, "w", encoding="utf-8") as f:
                json.dump(diccionario, f, indent=4)
            return True
        except (OSError, TypeError):
            return False