import os
import json
import dotenv
from datetime import datetime
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from rich import print as rprint

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
console = Console()

def save_conversation_to_log(conversation, log_file_path):
    """Guarda la conversación completa en un archivo de log"""
    try:
        with open(log_file_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"LOG DE CONVERSACIÓN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            for i, message in enumerate(conversation, 1):
                role = message["role"]
                content = message["content"]
                # Usar timestamp actual para cada guardado
                timestamp = datetime.now().strftime('%H:%M:%S')

                if role == "system":
                    f.write(f"[{timestamp}] SISTEMA: {content}\n")
                elif role == "user":
                    f.write(f"[{timestamp}] USUARIO: {content}\n")
                elif role == "assistant":
                    f.write(f"[{timestamp}] ASISTENTE: {content}\n")

                f.write("-" * 80 + "\n")

            f.write(f"\nFin del log - {len(conversation)} mensajes registrados\n")
            f.write(f"Archivo generado: {log_file_path}\n")
    except Exception as e:
        console.print(f"[red]Error al guardar el log: {e}[/red]")

def get_log_filename():
    """Genera el nombre del archivo de log con formato log_dia_hora.txt"""
    now = datetime.now()
    return f"log_{now.strftime('%Y%m%d')}_{now.strftime('%H%M%S')}.txt"

def save_conversation_to_json(conversation, json_file_path):
    """Guarda la conversación completa en un archivo JSON"""
    try:
        # Crear estructura de datos con metadatos
        conversation_data = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "total_messages": len(conversation),
                "model_used": "gpt-4o-mini",
                "version": "1.0"
            },
            "conversation": conversation
        }

        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        console.print(f"[red]Error al guardar el JSON: {e}[/red]")

def get_json_filename():
    """Genera el nombre del archivo JSON con formato log_dia_hora.json"""
    now = datetime.now()
    return f"log_{now.strftime('%Y%m%d')}_{now.strftime('%H%M%S')}.json"

def list_available_conversations():
    """Lista todas las conversaciones JSON disponibles en la carpeta logs"""
    try:
        if not os.path.exists("logs"):
            return []

        json_files = []
        for filename in os.listdir("logs"):
            if filename.endswith(".json") and filename.startswith("log_"):
                file_path = os.path.join("logs", filename)
                # Obtener información del archivo
                stat = os.stat(file_path)
                created_time = datetime.fromtimestamp(stat.st_ctime)
                json_files.append({
                    "filename": filename,
                    "filepath": file_path,
                    "created": created_time,
                    "size": stat.st_size
                })

        # Ordenar por fecha de creación (más reciente primero)
        json_files.sort(key=lambda x: x["created"], reverse=True)
        return json_files
    except Exception as e:
        console.print(f"[red]Error al listar conversaciones: {e}[/red]")
        return []

def load_conversation_from_json(json_file_path):
    """Carga una conversación desde un archivo JSON"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Verificar que tiene la estructura esperada
        if "conversation" in data and isinstance(data["conversation"], list):
            conversation = data["conversation"]
            metadata = data.get("metadata", {})

            console.print(f"[green]✅ Conversación cargada exitosamente[/green]")
            console.print(f"[dim]📄 Archivo: {os.path.basename(json_file_path)}[/dim]")
            console.print(f"[dim]📊 Mensajes: {len(conversation)}[/dim]")
            if "created_at" in metadata:
                console.print(f"[dim]📅 Creada: {metadata['created_at']}[/dim]")

            return conversation
        else:
            console.print(f"[red]❌ Formato de archivo inválido[/red]")
            return None

    except Exception as e:
        console.print(f"[red]❌ Error al cargar la conversación: {e}[/red]")
        return None

def show_startup_menu():
    """Muestra el menú de inicio para elegir entre nuevo chat o continuar uno anterior"""
    console.print("\n")
    welcome_panel = Panel(
        "[bold blue]🤖 Stateful Chatbot[/bold blue]\n[dim]API de Completions - Escribe 'exit' para salir[/dim]\n[dim]Las conversaciones se guardan automáticamente en ./logs/ (TXT + JSON)[/dim]",
        title="[green]Bienvenido[/green]",
        border_style="blue"
    )
    console.print(welcome_panel)

    # Mostrar opciones
    console.print("\n[bold cyan]¿Qué deseas hacer?[/bold cyan]")
    console.print("[bold green]1.[/bold green] Iniciar un nuevo chat")
    console.print("[bold yellow]2.[/bold yellow] Continuar una conversación anterior")

    while True:
        try:
            choice = Prompt.ask("\n[bold]Selecciona una opción (1 o 2)[/bold]", choices=["1", "2"])
            if choice == "1":
                return "new"
            elif choice == "2":
                return "continue"
        except KeyboardInterrupt:
            console.print("\n[yellow]Saliendo...[/yellow]")
            return "exit"

def show_conversation_list():
    """Muestra la lista de conversaciones disponibles y permite seleccionar una"""
    conversations = list_available_conversations()

    if not conversations:
        console.print("[yellow]⚠️ No hay conversaciones anteriores disponibles.[/yellow]")
        console.print("[dim]Iniciando un nuevo chat...[/dim]")
        return None

    console.print(f"\n[bold cyan]📋 Conversaciones disponibles ({len(conversations)}):[/bold cyan]")

    # Crear tabla con las conversaciones
    table = Table(title="[bold blue]Conversaciones Anteriores[/bold blue]")
    table.add_column("Nº", style="bold", width=4)
    table.add_column("Archivo", style="dim", width=25)
    table.add_column("Fecha", style="cyan", width=20)
    table.add_column("Tamaño", style="green", width=10)

    for i, conv in enumerate(conversations, 1):
        table.add_row(
            str(i),
            conv["filename"],
            conv["created"].strftime("%Y-%m-%d %H:%M:%S"),
            f"{conv['size']} bytes"
        )

    console.print(table)

    while True:
        try:
            choice = Prompt.ask(f"\n[bold]Selecciona una conversación (1-{len(conversations)}) o 'n' para nuevo chat[/bold]")

            if choice.lower() == 'n':
                return None

            choice_num = int(choice)
            if 1 <= choice_num <= len(conversations):
                selected_conv = conversations[choice_num - 1]
                return selected_conv["filepath"]
            else:
                console.print("[red]❌ Número inválido. Intenta de nuevo.[/red]")

        except ValueError:
            console.print("[red]❌ Por favor ingresa un número válido.[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Saliendo...[/yellow]")
            return "exit"

def main():
    # Mostrar menú de inicio
    startup_choice = show_startup_menu()

    if startup_choice == "exit":
        return

    model = "gpt-4o-mini"
    conversation = []
    log_path = ""
    json_path = ""

    if startup_choice == "new":
        # Iniciar nuevo chat
        conversation = [
            {"role": "system", "content": "Eres un asistente útil. Responde siempre en español y proporciona explicaciones claras y detalladas en español."}
        ]

        # Crear los archivos de log iniciales
        log_filename = get_log_filename()
        json_filename = get_json_filename()
        log_path = os.path.join("logs", log_filename)
        json_path = os.path.join("logs", json_filename)
        console.print(f"[dim]📝 Log TXT guardado en: {log_path}[/dim]")
        console.print(f"[dim]📄 Log JSON guardado en: {json_path}[/dim]")

    elif startup_choice == "continue":
        # Continuar conversación anterior
        selected_file = show_conversation_list()

        if selected_file == "exit":
            return
        elif selected_file is None:
            # No hay conversaciones, iniciar nuevo chat
            conversation = [
                {"role": "system", "content": "Eres un asistente útil. Responde siempre en español y proporciona explicaciones claras y detalladas en español."}
            ]

            log_filename = get_log_filename()
            json_filename = get_json_filename()
            log_path = os.path.join("logs", log_filename)
            json_path = os.path.join("logs", json_filename)
            console.print(f"[dim]📝 Log TXT guardado en: {log_path}[/dim]")
            console.print(f"[dim]📄 Log JSON guardado en: {json_path}[/dim]")
        else:
            # Cargar conversación seleccionada
            conversation = load_conversation_from_json(selected_file)
            if conversation is None:
                console.print("[red]❌ No se pudo cargar la conversación. Iniciando nuevo chat...[/red]")
                conversation = [
                    {"role": "system", "content": "Eres un asistente útil. Responde siempre en español y proporciona explicaciones claras y detalladas en español."}
                ]

            # Usar el mismo archivo para continuar la conversación
            log_path = selected_file.replace('.json', '.txt')
            json_path = selected_file
            console.print(f"[dim]📝 Continuando en: {log_path}[/dim]")
            console.print(f"[dim]📄 Continuando en: {json_path}[/dim]")

    # Mostrar comandos disponibles
    commands_panel = Panel(
        "[dim]Comandos disponibles:[/dim]\n[bold]• 'contexto'[/bold] - Ver historial de la conversación\n[bold]• 'guardar'[/bold] - Guardar manualmente\n[bold]• 'exit'[/bold] - Salir del programa",
        title="[blue]ℹ️ Información[/blue]",
        border_style="blue"
    )
    console.print(commands_panel)
    while True:
        user_input = Prompt.ask("[bold cyan]Tú[/bold cyan]")
        if user_input.lower() in {"exit", "quit"}:
            # Guardar la conversación final antes de salir
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

        # Check for "Contexto" command
        if user_input.lower() == "contexto":
            # Create a table for context display
            context_table = Table(title="[bold blue]📋 Contexto de la Conversación[/bold blue]")
            context_table.add_column("Rol", style="bold", width=12)
            context_table.add_column("Mensaje", style="dim")

            for message in conversation:
                role = message["role"]
                content = message["content"]
                if role == "system":
                    context_table.add_row("[red]Sistema[/red]", content)
                elif role == "user":
                    context_table.add_row("[blue]Usuario[/blue]", content)
                elif role == "assistant":
                    context_table.add_row("[green]Asistente[/green]", content)

            console.print(context_table)
            continue

        # Check for "Guardar" command
        if user_input.lower() in {"guardar", "save"}:
            save_conversation_to_log(conversation, log_path)
            save_conversation_to_json(conversation, json_path)
            console.print(f"[green]✅ Conversación guardada manualmente en TXT: {log_path}[/green]")
            console.print(f"[green]✅ Conversación guardada manualmente en JSON: {json_path}[/green]")
            continue

        conversation.append({"role": "user", "content": user_input})

        # Display user message in a panel
        user_panel = Panel(
            user_input,
            title="[blue]👤 Usuario[/blue]",
            border_style="blue"
        )
        console.print(user_panel)

        try:
            # Show loading indicator
            with console.status("[bold green]Pensando...", spinner="dots"):
                response = client.chat.completions.create(
                    model=model,
                    messages=conversation
                )

            text = response.choices[0].message.content.strip()
            conversation.append({"role": "assistant", "content": text})

            # Guardar la conversación actualizada en ambos formatos
            save_conversation_to_log(conversation, log_path)
            save_conversation_to_json(conversation, json_path)

            # Display bot response in a panel
            bot_panel = Panel(
                text,
                title="[green]🤖 Asistente[/green]",
                border_style="green"
            )
            console.print(bot_panel)

        except Exception as e:
            error_panel = Panel(
                f"[bold red]Error:[/bold red] {e}",
                title="[red]❌ Error[/red]",
                border_style="red"
            )
            console.print(error_panel)

if __name__ == "__main__":
    main()
