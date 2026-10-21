# MiniOs-0.3

Mini OS — ecosistema en Python con un procesador virtual, lenguaje ensamblador (KevASM), sistema de archivos jerárquico con persistencia en JSON e intérprete/CLI integrado. Proyecto educativo y experimental para aprender diseño de máquinas virtuales, ensambladores y sistemas de archivos simples.

## Características

- CPU virtual y ejecutor de programas.
- Ensamblador simple (KevASM) que traduce instrucciones a una representación binaria textual.
- Sistema de archivos jerárquico con persistencia en JSON.
- Shell interactivo con comandos para navegación, manipulación de archivos, ejecución de ASM/Python y utilidades.
- Módulos separados por responsabilidad (cpu, disco, memoria, ensamblador, comandos, etc.).

## Requisitos

- Python 3.8+.
- No se detectaron dependencias externas en el repositorio actual.

## Instalación rápida

1. Clona el repositorio:
   git clone https://github.com/progaming12kk-art/MiniOs-0.3.git

2. Entra en la carpeta:
   cd MiniOs-0.3

3. (Opcional) Crea y activa un entorno virtual:
   python -m venv .venv

   - Linux/macOS: source .venv/bin/activate
   - Windows (PowerShell): .venv\Scripts\Activate.ps1

4. (Opcional) Si más adelante añades dependencias, crea requirements.txt y ejecuta:
   pip install -r requirements.txt

## Ejecutar

Inicia la consola del Mini OS:

python main.py

Al iniciarse verás un prompt similar a:

@MiniOs /:

Escribe help para ver la ayuda disponible desde el shell.

## Comandos principales (resumen)

- Navegación y directorios
  - pwd — muestra directorio actual
  - cd <ruta> — cambia directorio
  - mkdir <nombre> — crea carpeta
  - rmdir <nombre> — borra carpeta
  - ls [ruta] — lista entradas de un directorio
  - tree [ruta] — muestra árbol de directorios

- Archivos
  - write <ruta> { contenido } — crea archivo con contenido (usa llaves para agrupar)
  - touch <ruta> — crea archivo vacío
  - cat <ruta> — muestra el contenido (intenta decodificar a texto)
  - remove <ruta> — borra archivo
  - save — guarda el estado del disco (persistencia JSON)
  - cargar — carga el estado del disco desde el archivo de persistencia

- Ejecución
  - asm <ruta> — ejecuta un archivo asm guardado
  - python <ruta> — ejecuta el contenido de un archivo como código Python (¡con precaución!)

- Imágenes simples
  - img crear <nombre> <ancho> <alto> — crea imagen simple
  - img ver <nombre> — renderiza imagen en terminal
  - img pintar <nombre> <x> <y> <color> — pinta un píxel en la imagen

- Utilidades
  - version, whoami, time, clear, help, dashboard

> Nota: Para ver la ayuda completa en tiempo de ejecución, ejecuta help en el shell.

## Ensamblador (KevASM) — breve

El ensamblador traduce tokens a códigos binarios definidos en ensamblador.py. Instrucciones soportadas (ejemplos): SUMA, RESTA, MULTI, DIV, MOD, LOAD, STORE, JC, JUMP, JUMPI, SEE, OUT, CALL, RET, HALT.

Ejemplo muy simple (archivo ejemplo.asm):

```
; Suma dos valores y muestra el resultado
LOAD 0
LOAD 1
SUMA
OUT
HALT
```

Guarda el ejemplo en el disco virtual y ejecuta con asm /ejemplo.asm desde el shell.

## Estructura del proyecto (resumen)

- main.py — punto de entrada (CLI)
- api.py — capa que orquesta CPU, disco, memoria y ensamblador
- cpu.py — implementación del procesador virtual
- ensamblador.py — traductor KevASM → "binario" textual
- disco.py, archivos.py — sistema de archivos y persistencia
- memoria.py — modelo de memoria de la máquina virtual
- ejecutor.py — parseo de comandos y ejecución
- comandos.py — implementación de comandos de shell
- dashboard.py — interfaz/detalles para inspección
- logger.py, colores.py, constantes.py — utilidades y configuración
- LICENSE — licencia del proyecto

## Desarrollo y pruebas

Recomendaciones para mejorar el proyecto:

1. Añadir tests (pytest) para CPU, ensamblador y operaciones de disco.
2. Agregar requirements.txt o pyproject.toml si se incorporan dependencias.
3. Añadir CI (GitHub Actions) para ejecutar tests y linters.
4. Refactorizar módulos grandes en submódulos para facilidad de pruebas y mantenimiento.
5. Añadir ejemplos en /examples con pequeños programas KevASM y salidas esperadas.

## Seguridad y advertencias

- El comando python <archivo> ejecuta código arbitrario: úsalo solo con archivos de confianza.
- Haz backup de los archivos de persistencia del disco antes de operaciones destructivas.

## Contribuir

Si quieres contribuir: abre issues o pull requests. Ideas de contribución: tests, documentación, refactorizaciones, nuevas instrucciones para la CPU, mejoras en la persistencia.

## Licencia

Este repositorio incluye un archivo LICENSE. Revísalo para conocer los términos exactos.