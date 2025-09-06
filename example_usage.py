#!/usr/bin/env python3
"""
Ejemplo de uso del Analizador de Imágenes con Claude
Este script demuestra cómo usar el analizador programáticamente
"""

import os
import sys
from image_analyzer import analyze_image, encode_image_to_base64, get_image_media_type

def example_analysis():
    """Ejemplo de análisis de imagen"""

    # Verificar que existe la API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY no encontrada")
        print("Por favor, configura tu API key en el archivo .env")
        return

    # Ejemplo de imagen (reemplaza con una ruta real)
    image_path = input("Ingresa la ruta de una imagen para analizar: ").strip()

    if not os.path.exists(image_path):
        print(f"❌ Archivo no encontrado: {image_path}")
        return

    # Preguntas de ejemplo
    questions = [
        "Describe esta imagen en detalle",
        "¿Qué objetos principales ves en esta imagen?",
        "Analiza los colores y la composición visual",
        "¿Qué emociones o sensaciones transmite esta imagen?",
        "Identifica cualquier texto o signos visibles"
    ]

    print(f"\n🖼️ Analizando: {os.path.basename(image_path)}")
    print("=" * 50)

    for i, question in enumerate(questions, 1):
        print(f"\n📝 Pregunta {i}: {question}")
        print("-" * 30)

        # Realizar análisis
        analysis = analyze_image(image_path, question)

        if analysis:
            print(f"🤖 Respuesta de Claude:\n{analysis}")
        else:
            print("❌ No se pudo analizar la imagen")

        print("\n" + "=" * 50)

        # Pausa entre análisis
        input("Presiona Enter para continuar con la siguiente pregunta...")

def test_image_formats():
    """Prueba diferentes formatos de imagen"""

    formats = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']

    print("🔍 Formatos de imagen soportados:")
    for fmt in formats:
        print(f"  ✅ {fmt}")

    print(f"\n📊 Total de formatos: {len(formats)}")

def show_usage_tips():
    """Muestra consejos de uso"""

    tips = [
        "💡 Usa imágenes de alta calidad para mejores resultados",
        "💡 Las preguntas específicas dan respuestas más detalladas",
        "💡 Claude puede analizar texto, objetos, personas y emociones",
        "💡 Los análisis se guardan automáticamente en ./logs/",
        "💡 Puedes ver el historial de análisis en el menú principal",
        "💡 Usa Ctrl+C para cancelar cualquier operación"
    ]

    print("💡 Consejos de uso:")
    for tip in tips:
        print(f"  {tip}")

if __name__ == "__main__":
    print("🖼️ Ejemplo de Uso - Analizador de Imágenes con Claude")
    print("=" * 60)

    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Analizar una imagen (ejemplo completo)")
        print("2. Ver formatos soportados")
        print("3. Ver consejos de uso")
        print("4. Salir")

        choice = input("\nSelecciona una opción (1-4): ").strip()

        if choice == "1":
            example_analysis()
        elif choice == "2":
            test_image_formats()
        elif choice == "3":
            show_usage_tips()
        elif choice == "4":
            print("¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")
