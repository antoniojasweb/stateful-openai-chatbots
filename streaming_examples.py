#!/usr/bin/env python3
"""
Ejemplos de uso de streaming con Claude
Este script demuestra diferentes formas de usar streaming
"""

import os
import json
import time
import dotenv
from datetime import datetime
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

dotenv.load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
console = Console()

def example_basic_streaming():
    """Ejemplo básico de streaming"""
    console.print("\n[bold cyan]🎬 EJEMPLO 1: Streaming Básico[/bold cyan]")
    console.print("=" * 50)

    prompt = "Escribe una historia corta sobre un robot que aprende a soñar"

    console.print(f"[bold]Prompt:[/bold] {prompt}")
    console.print("\n[bold green]Respuesta en streaming:[/bold green]")

    try:
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            response_text = ""
            for chunk in stream:
                if chunk.type == "content_block_delta":
                    response_text += chunk.delta.text
                    console.print(chunk.delta.text, end="", flush=True)
                    time.sleep(0.02)  # Efecto de escritura

        console.print(f"\n\n[dim]✅ Streaming completado. Total: {len(response_text)} caracteres[/dim]")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

def example_streaming_with_panel():
    """Ejemplo de streaming con panel visual"""
    console.print("\n[bold cyan]🎬 EJEMPLO 2: Streaming con Panel[/bold cyan]")
    console.print("=" * 50)

    prompt = "Explica cómo funciona la inteligencia artificial de manera simple"

    console.print(f"[bold]Prompt:[/bold] {prompt}")

    try:
        response_text = ""
        panel = Panel(
            "[dim]Claude está escribiendo...[/dim]",
            title="[green]🤖 Claude (Streaming)[/green]",
            border_style="green"
        )

        with Live(panel, console=console, refresh_per_second=10) as live:
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for chunk in stream:
                    if chunk.type == "content_block_delta":
                        response_text += chunk.delta.text
                        live.update(Panel(
                            response_text + "[dim]▊[/dim]",
                            title="[green]🤖 Claude (Streaming)[/green]",
                            border_style="green"
                        ))
                        time.sleep(0.01)

        # Panel final
        final_panel = Panel(
            response_text,
            title="[green]🤖 Claude (Completado)[/green]",
            border_style="green"
        )
        console.print(final_panel)

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

def example_streaming_with_progress():
    """Ejemplo de streaming con barra de progreso"""
    console.print("\n[bold cyan]🎬 EJEMPLO 3: Streaming con Progreso[/bold cyan]")
    console.print("=" * 50)

    prompt = "Crea una lista de 10 consejos para programar mejor en Python"

    console.print(f"[bold]Prompt:[/bold] {prompt}")

    try:
        response_text = ""

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Claude está escribiendo...", total=None)

            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for chunk in stream:
                    if chunk.type == "content_block_delta":
                        response_text += chunk.delta.text
                        progress.update(task, description=f"Escribiendo... {len(response_text)} caracteres")
                        time.sleep(0.01)

        # Mostrar resultado final
        result_panel = Panel(
            response_text,
            title="[green]✅ Lista de Consejos Completada[/green]",
            border_style="green"
        )
        console.print(result_panel)

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

def example_streaming_conversation():
    """Ejemplo de streaming en conversación"""
    console.print("\n[bold cyan]🎬 EJEMPLO 4: Conversación con Streaming[/bold cyan]")
    console.print("=" * 50)

    conversation = [
        {"role": "user", "content": "Hola, ¿puedes ayudarme a entender qué es el streaming?"},
        {"role": "assistant", "content": "¡Hola! Claro, te ayudo a entender el streaming. El streaming es una técnica que permite transmitir datos de forma continua en tiempo real, en lugar de esperar a que se complete toda la transmisión."}
    ]

    console.print("[bold]Conversación existente:[/bold]")
    for msg in conversation:
        role = "👤 Usuario" if msg["role"] == "user" else "🤖 Claude"
        console.print(f"[dim]{role}: {msg['content'][:100]}...[/dim]")

    new_prompt = "¿Cuáles son las ventajas del streaming en aplicaciones de chat?"
    console.print(f"\n[bold]Nueva pregunta:[/bold] {new_prompt}")

    try:
        response_text = ""

        with Live(
            Panel(
                "[dim]Claude está respondiendo...[/dim]",
                title="[green]🤖 Claude (Conversación)[/green]",
                border_style="green"
            ),
            console=console,
            refresh_per_second=10
        ) as live:
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=conversation + [{"role": "user", "content": new_prompt}]
            ) as stream:
                for chunk in stream:
                    if chunk.type == "content_block_delta":
                        response_text += chunk.delta.text
                        live.update(Panel(
                            response_text + "[dim]▊[/dim]",
                            title="[green]🤖 Claude (Conversación)[/green]",
                            border_style="green"
                        ))
                        time.sleep(0.01)

        # Mostrar respuesta final
        final_panel = Panel(
            response_text,
            title="[green]✅ Respuesta Completada[/green]",
            border_style="green"
        )
        console.print(final_panel)

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

def example_streaming_with_tools():
    """Ejemplo de streaming con herramientas (simulado)"""
    console.print("\n[bold cyan]🎬 EJEMPLO 5: Streaming con Herramientas[/bold cyan]")
    console.print("=" * 50)

    prompt = "Calcula 15 * 23 y luego explica el proceso paso a paso"

    console.print(f"[bold]Prompt:[/bold] {prompt}")
    console.print("[dim]Nota: Este ejemplo simula el uso de herramientas con streaming[/dim]")

    try:
        # Simular cálculo
        result = 15 * 23
        console.print(f"\n[bold blue]🔧 Herramienta ejecutada:[/bold blue] calculate(15 * 23)")
        console.print(f"[green]✅ Resultado: {result}[/green]")

        # Ahora streaming de la explicación
        explanation_prompt = f"El resultado de 15 * 23 es {result}. Explica el proceso de multiplicación paso a paso de manera didáctica."

        response_text = ""

        with Live(
            Panel(
                "[dim]Claude está explicando el proceso...[/dim]",
                title="[green]🤖 Claude (Explicación)[/green]",
                border_style="green"
            ),
            console=console,
            refresh_per_second=10
        ) as live:
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=400,
                messages=[{"role": "user", "content": explanation_prompt}]
            ) as stream:
                for chunk in stream:
                    if chunk.type == "content_block_delta":
                        response_text += chunk.delta.text
                        live.update(Panel(
                            response_text + "[dim]▊[/dim]",
                            title="[green]🤖 Claude (Explicación)[/green]",
                            border_style="green"
                        ))
                        time.sleep(0.01)

        # Mostrar explicación final
        final_panel = Panel(
            response_text,
            title="[green]✅ Explicación Completada[/green]",
            border_style="green"
        )
        console.print(final_panel)

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")

def show_streaming_benefits():
    """Muestra las ventajas del streaming"""
    console.print("\n[bold cyan]💡 VENTAJAS DEL STREAMING[/bold cyan]")
    console.print("=" * 50)

    benefits = [
        "🚀 **Respuesta inmediata**: El usuario ve la respuesta en tiempo real",
        "⏱️ **Mejor experiencia**: No hay espera larga para respuestas completas",
        "👀 **Transparencia**: Se puede ver cómo el modelo 'piensa' mientras escribe",
        "🔄 **Interactividad**: Posibilidad de cancelar respuestas en progreso",
        "📱 **UX moderna**: Similar a aplicaciones de chat populares",
        "⚡ **Eficiencia**: Mejor percepción de velocidad de respuesta",
        "🎯 **Engagement**: Mantiene la atención del usuario",
        "🛠️ **Debugging**: Más fácil identificar dónde ocurren problemas"
    ]

    for benefit in benefits:
        console.print(f"[dim]{benefit}[/dim]")

    console.print(f"\n[bold green]🎬 ¡El streaming hace que la IA se sienta más humana y responsiva![/bold green]")

def main():
    """Función principal del demo de streaming"""
    console.print("[bold blue]🎬 DEMO DE STREAMING CON CLAUDE[/bold blue]")
    console.print("=" * 60)

    # Verificar API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]❌ Error: ANTHROPIC_API_KEY no encontrada[/red]")
        console.print("[dim]Configura tu API key en el archivo .env[/dim]")
        return

    while True:
        console.print("\n[bold cyan]¿Qué ejemplo quieres ver?[/bold cyan]")
        console.print("1. Streaming Básico")
        console.print("2. Streaming con Panel Visual")
        console.print("3. Streaming con Barra de Progreso")
        console.print("4. Conversación con Streaming")
        console.print("5. Streaming con Herramientas (Simulado)")
        console.print("6. Ver Ventajas del Streaming")
        console.print("7. Ejecutar Todos los Ejemplos")
        console.print("8. Salir")

        choice = input("\nSelecciona una opción (1-8): ").strip()

        if choice == "1":
            example_basic_streaming()
        elif choice == "2":
            example_streaming_with_panel()
        elif choice == "3":
            example_streaming_with_progress()
        elif choice == "4":
            example_streaming_conversation()
        elif choice == "5":
            example_streaming_with_tools()
        elif choice == "6":
            show_streaming_benefits()
        elif choice == "7":
            console.print("\n[bold yellow]🎬 Ejecutando todos los ejemplos...[/bold yellow]")
            example_basic_streaming()
            example_streaming_with_panel()
            example_streaming_with_progress()
            example_streaming_conversation()
            example_streaming_with_tools()
            show_streaming_benefits()
        elif choice == "8":
            console.print("\n[bold green]👋 ¡Hasta luego![/bold green]")
            break
        else:
            console.print("[red]❌ Opción inválida. Intenta de nuevo.[/red]")

        input("\nPresiona Enter para continuar...")
        console.print("\n" + "="*60)

if __name__ == "__main__":
    main()
