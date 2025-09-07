#!/usr/bin/env python3
"""
Ejemplo práctico de uso de herramientas con Claude
Este script demuestra diferentes escenarios de uso de las herramientas
"""

import os
import sys
from tools_chatbot import (
    get_weather, calculate, get_file_info, create_note,
    execute_tool, TOOLS
)

def demo_weather_tool():
    """Demuestra el uso de la herramienta de clima"""
    print("🌤️ DEMO: Herramienta de Clima")
    print("=" * 40)

    cities = ["Madrid", "Barcelona", "London", "Paris", "Tokyo"]

    for city in cities:
        result = get_weather(city)
        print(f"📍 {city}: {result}")

    print()

def demo_calculator_tool():
    """Demuestra el uso de la herramienta de calculadora"""
    print("🧮 DEMO: Herramienta de Calculadora")
    print("=" * 40)

    expressions = [
        "2 + 2 * 3",
        "sqrt(16)",
        "sin(pi/2)",
        "log(10)",
        "2**8",
        "sqrt(144) + 5*3"
    ]

    for expr in expressions:
        result = calculate(expr)
        print(f"🔢 {expr} = {result}")

    print()

def demo_file_info_tool():
    """Demuestra el uso de la herramienta de información de archivos"""
    print("📁 DEMO: Herramienta de Información de Archivos")
    print("=" * 40)

    # Crear un archivo de ejemplo
    test_file = "test_file.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("Este es un archivo de prueba para demostrar la herramienta de información de archivos.")

    result = get_file_info(test_file)
    print(f"📄 {test_file}:")
    print(result)

    # Limpiar archivo de prueba
    os.remove(test_file)
    print()

def demo_note_creation_tool():
    """Demuestra el uso de la herramienta de creación de notas"""
    print("📝 DEMO: Herramienta de Creación de Notas")
    print("=" * 40)

    notes = [
        ("Ideas de Proyecto", "Desarrollar una app móvil, aprender Python, crear un blog"),
        ("Lista de Compras", "Leche, pan, huevos, frutas, verduras"),
        ("Tareas del Día", "Reunión a las 10am, llamar al cliente, revisar código")
    ]

    for title, content in notes:
        result = create_note(title, content)
        print(f"📋 {title}: {result}")

    print()

def demo_tool_execution():
    """Demuestra la ejecución de herramientas a través del sistema"""
    print("🔧 DEMO: Ejecución de Herramientas")
    print("=" * 40)

    test_cases = [
        ("get_weather", {"city": "Madrid"}),
        ("calculate", {"expression": "sqrt(25) + 3*2"}),
        ("get_file_info", {"file_path": "README.md"}),
        ("create_note", {"title": "Demo Note", "content": "Esta es una nota de demostración"})
    ]

    for tool_name, parameters in test_cases:
        print(f"🔧 Ejecutando: {tool_name}")
        result = execute_tool(tool_name, parameters)
        print(f"✅ Resultado: {result}")
        print()

def show_available_tools():
    """Muestra todas las herramientas disponibles"""
    print("🛠️ HERRAMIENTAS DISPONIBLES")
    print("=" * 40)

    for i, tool in enumerate(TOOLS, 1):
        print(f"{i}. {tool['name']}")
        print(f"   📝 {tool['description']}")
        print(f"   📋 Parámetros: {list(tool['input_schema']['properties'].keys())}")
        print()

def interactive_demo():
    """Demo interactivo de herramientas"""
    print("🎮 DEMO INTERACTIVO DE HERRAMIENTAS")
    print("=" * 40)
    print("Escribe comandos para probar las herramientas:")
    print("- 'clima <ciudad>' - Obtener clima")
    print("- 'calc <expresión>' - Calcular expresión")
    print("- 'archivo <ruta>' - Información de archivo")
    print("- 'nota <título> | <contenido>' - Crear nota")
    print("- 'salir' - Terminar demo")
    print()

    while True:
        try:
            command = input("🔧 Comando: ").strip()

            if command.lower() == 'salir':
                print("👋 ¡Demo terminado!")
                break

            parts = command.split(' ', 1)
            if len(parts) < 2:
                print("❌ Formato: 'comando <parámetros>'")
                continue

            cmd, params = parts[0].lower(), parts[1]

            if cmd == 'clima':
                result = get_weather(params)
                print(f"🌤️ {result}")
            elif cmd == 'calc':
                result = calculate(params)
                print(f"🧮 {result}")
            elif cmd == 'archivo':
                result = get_file_info(params)
                print(f"📁 {result}")
            elif cmd == 'nota':
                if '|' in params:
                    title, content = params.split('|', 1)
                    result = create_note(title.strip(), content.strip())
                    print(f"📝 {result}")
                else:
                    print("❌ Formato: 'nota <título> | <contenido>'")
            else:
                print("❌ Comando no reconocido")

            print()

        except KeyboardInterrupt:
            print("\n👋 ¡Demo terminado!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Función principal del demo"""
    print("🔧 DEMO DE HERRAMIENTAS CON CLAUDE")
    print("=" * 50)
    print()

    while True:
        print("¿Qué demo quieres ver?")
        print("1. Herramienta de Clima")
        print("2. Herramienta de Calculadora")
        print("3. Herramienta de Información de Archivos")
        print("4. Herramienta de Creación de Notas")
        print("5. Ejecución de Herramientas")
        print("6. Ver Herramientas Disponibles")
        print("7. Demo Interactivo")
        print("8. Salir")

        choice = input("\nSelecciona una opción (1-8): ").strip()

        if choice == "1":
            demo_weather_tool()
        elif choice == "2":
            demo_calculator_tool()
        elif choice == "3":
            demo_file_info_tool()
        elif choice == "4":
            demo_note_creation_tool()
        elif choice == "5":
            demo_tool_execution()
        elif choice == "6":
            show_available_tools()
        elif choice == "7":
            interactive_demo()
        elif choice == "8":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

        input("\nPresiona Enter para continuar...")
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
