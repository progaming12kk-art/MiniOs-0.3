from api import API
from ejecutor import Ejecutor
from dashboard import Dashboard


def main():
    api = API()
    print(f"--- Mini OS v{api.version()} ---")
    print(api.bienvenida())

    while True:
        try:
            comando = input(api.color_ansi("verde") + "@MiniOs " + api.pwd() + ": ")
            if comando.strip().lower() in ("end", "salir", "exit"):
                break
            elif comando.strip().lower() == "dashboard":
                Dashboard(api).dashboard()
            Ejecutor(comando, api).ejecutar()
        except (KeyboardInterrupt, EOFError):
            input(api.color_ansi("amarillo") + "[CONFIRMACION DE SALIDA]")
            print(api.color_ansi("rojo") + "Saliendo...")
            break


if __name__ == "__main__":
    main()