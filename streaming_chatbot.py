import os
import json
import dotenv
from datetime import datetime
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich import print as rprint
import time

dotenv.load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
console = Console()

def save_conversation_to_log(conversation, log_file_path):
    """Guarda la conversación completa en un archivo de log"""
    try:
        with open(log_file_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"LOG DE CONVERSACIÓN STREAMING - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            for i, message in enumerate(conversation, 1):
                role = message["role"]
                content = message["content"]
                timestamp = datetime.now().strftime('%H:%M:%S')

                if role == "user":
                    f.write(f"[{timestamp}] USUARIO: {content}\n")
                elif role == "assistant":
                    f.write(f"[{timestamp}] ASISTENTE: {content}\n")

                f.write("-" * 80 + "\n")

            f.write(f"\nFin del log - {len(conversation)} mensajes registrados\n")
            f.write(f"Archivo generado: {log_file_path}\n")
    except Exception as e:
        console.print(f"[red]Error al guardar el log: {e}[/red]")

def save_conversation_to_json(conversation, json_file_path):
    """Guarda la conversación completa en un archivo JSON"""
    try:
        conversation_data = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "total_messages": len(conversation),
                "model_used": "claude-sonnet-4-20250514",
                "api_provider": "anthropic",
                "features": "streaming",
                "version": "1.0"
            },
            "conversation": conversation
        }

        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        console.print(f"[red]Error al guardar el JSON: {e}[/red]")

def get_log_filename():
    """Genera el nombre del archivo de log"""
    now = datetime.now()
    return f"log_streaming_{now.strftime('%Y%m%d')}_{now.strftime('%H%M%S')}.txt"

def get_json_filename():
    """Genera el nombre del archivo JSON"""
    now = datetime.now()
    return f"log_streaming_{now.strftime('%Y%m%d')}_{now.strftime('%H%M%S')}.json"

def show_streaming_demo():
    """Muestra un demo de las capacidades de streaming"""
    console.print("\n[bold cyan]🎬 DEMO DE STREAMING[/bold cyan]")
    console.print("=" * 50)

    demos = [
        "Escribe una historia corta sobre un robot",
        "Explica cómo funciona la inteligencia artificial",
        "Crea una lista de 10 consejos para programar mejor",
        "Describe las ventajas del streaming en tiempo real"
    ]

    console.print("\n[bold yellow]Ejemplos de prompts para probar streaming:[/bold yellow]")
    for i, demo in enumerate(demos, 1):
        console.print(f"[dim]{i}. {demo}[/dim]")

    console.print("\n[bold green]💡 Consejos:[/bold green]")
    console.print("[dim]• Las respuestas aparecerán en tiempo real[/dim]")
    console.print("[dim]• Puedes ver cómo Claude 'piensa' mientras escribe[/dim]")
    console.print("[dim]• El streaming es especialmente útil para respuestas largas[/dim]")
    console.print("[dim]• Usa Ctrl+C para cancelar una respuesta en progreso[/dim]")

def stream_response(user_input, conversation, log_path, json_path):
    """Streams a response from Claude in real-time"""
    try:
        # Añadir mensaje del usuario
        conversation.append({"role": "user", "content": user_input})

        # Display user message
        user_panel = Panel(
            user_input,
            title="[blue]👤 Usuario[/blue]",
            border_style="blue"
        )
        console.print(user_panel)

        # Crear panel para la respuesta del asistente
        assistant_content = ""
        assistant_panel = Panel(
            "[dim]Claude está escribiendo...[/dim]",
            title="[green]🤖 Claude (Streaming)[/green]",
            border_style="green"
        )

        # Usar Live para actualizar en tiempo real
        with Live(assistant_panel, console=console, refresh_per_second=10) as live:
            # Llamar a la API con streaming
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=conversation
            ) as stream:
                for chunk in stream:
                    if chunk.type == "content_block_delta":
                        # Añadir texto al contenido
                        assistant_content += chunk.delta.text

                        # Actualizar el panel en tiempo real
                        live.update(Panel(
                            assistant_content + "[dim]▊[/dim]",  # Cursor parpadeante
                            title="[green]🤖 Claude (Streaming)[/green]",
                            border_style="green"
                        ))

                        # Pequeña pausa para efecto visual
                        time.sleep(0.01)

        # Añadir respuesta completa a la conversación
        conversation.append({"role": "assistant", "content": assistant_content})

        # Guardar conversación actualizada
        save_conversation_to_log(conversation, log_path)
        save_conversation_to_json(conversation, json_path)

        # Mostrar panel final sin cursor
        final_panel = Panel(
            assistant_content,
            title="[green]🤖 Claude (Completado)[/green]",
            border_style="green"
        )
        console.print(final_panel)

        return True

    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Respuesta cancelada por el usuario[/yellow]")
        return False
    except Exception as e:
        error_panel = Panel(
            f"[bold red]Error:[/bold red] {e}",
            title="[red]❌ Error[/red]",
            border_style="red"
        )
        console.print(error_panel)
        return False

def show_context(conversation):
    """Muestra el contexto de la conversación"""
    if not conversation:
        console.print("[yellow]⚠️ No hay mensajes en el contexto actual.[/yellow]")
        return

    context_table = Table(title="[bold blue]📋 Contexto de la Conversación (Streaming)[/bold blue]")
    context_table.add_column("Rol", style="bold", width=12)
    context_table.add_column("Mensaje", style="dim")

    for message in conversation:
        role = message["role"]
        content = message["content"]
        if role == "user":
            context_table.add_row("[blue]Usuario[/blue]", content)
        elif role == "assistant":
            context_table.add_row("[green]Asistente[/green]", content)

    console.print(context_table)

def show_streaming_stats(conversation):
    """Muestra estadísticas de la conversación"""
    if not conversation:
        console.print("[yellow]⚠️ No hay conversación para analizar.[/yellow]")
        return

    user_messages = [msg for msg in conversation if msg["role"] == "user"]
    assistant_messages = [msg for msg in conversation if msg["role"] == "assistant"]

    total_chars = sum(len(msg["content"]) for msg in conversation)
    avg_response_length = sum(len(msg["content"]) for msg in assistant_messages) / len(assistant_messages) if assistant_messages else 0

    stats_table = Table(title="[bold blue]📊 Estadísticas de Streaming[/bold blue]")
    stats_table.add_column("Métrica", style="bold")
    stats_table.add_column("Valor", style="green")

    stats_table.add_row("Mensajes del usuario", str(len(user_messages)))
    stats_table.add_row("Respuestas del asistente", str(len(assistant_messages)))
    stats_table.add_row("Total de caracteres", str(total_chars))
    stats_table.add_row("Promedio de respuesta", f"{avg_response_length:.1f} caracteres")
    stats_table.add_row("Tiempo de sesión", f"{datetime.now().strftime('%H:%M:%S')}")

    console.print(stats_table)

def main():
    # Verificar API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]❌ Error: ANTHROPIC_API_KEY no encontrada en el archivo .env[/red]")
        console.print("[dim]Por favor, añade tu API key de Anthropic al archivo .env[/dim]")
        return

    # Crear directorio de logs si no existe
    os.makedirs("logs", exist_ok=True)

    # Mensaje de bienvenida
    welcome_panel = Panel(
        "[bold blue]🎬 Chatbot con Streaming (Claude)[/bold blue]\n[dim]Respuestas en tiempo real con efecto de escritura[/dim]\n[dim]Escribe 'demo' para ver ejemplos, 'stats' para estadísticas, 'exit' para salir[/dim]",
        title="[green]Bienvenido[/green]",
        border_style="blue"
    )
    console.print(welcome_panel)

    # Crear archivos de log
    log_filename = get_log_filename()
    json_filename = get_json_filename()
    log_path = os.path.join("logs", log_filename)
    json_path = os.path.join("logs", json_filename)
    console.print(f"[dim]📝 Log TXT guardado en: {log_path}[/dim]")
    console.print(f"[dim]📄 Log JSON guardado en: {json_path}[/dim]")

    conversation = []

    while True:
        user_input = Prompt.ask("[bold cyan]Tú[/bold cyan]")

        if user_input.lower() in {"exit", "quit"}:
            # Guardar conversación final
            if conversation:
                save_conversation_to_log(conversation, log_path)
                save_conversation_to_json(conversation, json_path)
                console.print(f"[green]✅ Conversación guardada en TXT: {log_path}[/green]")
                console.print(f"[green]✅ Conversación guardada en JSON: {json_path}[/green]")

            goodbye_panel = Panel(
                "[bold green]¡Hasta luego![/bold green]",
                title="[red]Despedida[/red]",
                border_style="red"
            )
            console.print(goodbye_panel)
            break

        # Comando especial para demo
        if user_input.lower() in {"demo", "ejemplos"}:
            show_streaming_demo()
            continue

        # Comando para ver contexto
        if user_input.lower() == "contexto":
            show_context(conversation)
            continue

        # Comando para ver estadísticas
        if user_input.lower() in {"stats", "estadisticas", "estadísticas"}:
            show_streaming_stats(conversation)
            continue

        # Comando para limpiar contexto
        if user_input.lower() in {"limpiar", "clear", "nuevo"}:
            conversation = []
            console.print("[green]✅ Contexto limpiado. Nueva conversación iniciada.[/green]")
            continue

        # Procesar entrada normal con streaming
        success = stream_response(user_input, conversation, log_path, json_path)

        if not success:
            # Si hubo error o cancelación, continuar
            continue

if __name__ == "__main__":
    main()
