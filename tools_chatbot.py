import os
import json
import math
import dotenv
from datetime import datetime
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import print as rprint

dotenv.load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
console = Console()

# Definir las herramientas disponibles
TOOLS = [
    {
        "name": "get_weather",
        "description": "Obtiene el clima actual de una ciudad específica",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Nombre de la ciudad para consultar el clima"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "calculate",
        "description": "Realiza cálculos matemáticos básicos",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Expresión matemática a calcular (ej: '2 + 2', 'sqrt(16)', 'sin(pi/2)')"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_file_info",
        "description": "Obtiene información sobre un archivo en el sistema",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Ruta del archivo a analizar"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "create_note",
        "description": "Crea una nota y la guarda en un archivo",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Título de la nota"
                },
                "content": {
                    "type": "string",
                    "description": "Contenido de la nota"
                }
            },
            "required": ["title", "content"]
        }
    }
]

def get_weather(city):
    """Obtiene el clima actual de una ciudad (simulado)"""
    try:
        # Simulación de API del clima (en un caso real usarías una API real)
        weather_data = {
            "madrid": {"temp": 22, "condition": "soleado", "humidity": 45},
            "barcelona": {"temp": 24, "condition": "parcialmente nublado", "humidity": 60},
            "london": {"temp": 15, "condition": "lluvioso", "humidity": 80},
            "paris": {"temp": 18, "condition": "nublado", "humidity": 70},
            "tokyo": {"temp": 28, "condition": "soleado", "humidity": 55}
        }

        city_lower = city.lower()
        if city_lower in weather_data:
            data = weather_data[city_lower]
            return f"Clima en {city}: {data['temp']}°C, {data['condition']}, humedad {data['humidity']}%"
        else:
            return f"No tengo datos del clima para {city}. Ciudades disponibles: Madrid, Barcelona, London, Paris, Tokyo"
    except Exception as e:
        return f"Error al obtener el clima: {e}"

def calculate(expression):
    """Realiza cálculos matemáticos básicos"""
    try:
        # Reemplazar funciones matemáticas comunes
        expression = expression.replace("sqrt", "math.sqrt")
        expression = expression.replace("sin", "math.sin")
        expression = expression.replace("cos", "math.cos")
        expression = expression.replace("tan", "math.tan")
        expression = expression.replace("pi", "math.pi")
        expression = expression.replace("e", "math.e")
        expression = expression.replace("log", "math.log")
        expression = expression.replace("exp", "math.exp")

        # Evaluar la expresión de forma segura
        allowed_names = {
            "math": math,
            "__builtins__": {}
        }

        result = eval(expression, allowed_names)
        return f"Resultado: {result}"
    except Exception as e:
        return f"Error en el cálculo: {e}"

def get_file_info(file_path):
    """Obtiene información sobre un archivo"""
    try:
        if not os.path.exists(file_path):
            return f"El archivo no existe: {file_path}"

        stat = os.stat(file_path)
        size = stat.st_size
        modified = datetime.fromtimestamp(stat.st_mtime)
        created = datetime.fromtimestamp(stat.st_ctime)

        info = f"""
Información del archivo: {file_path}
- Tamaño: {size} bytes
- Modificado: {modified.strftime('%Y-%m-%d %H:%M:%S')}
- Creado: {created.strftime('%Y-%m-%d %H:%M:%S')}
- Es archivo: {os.path.isfile(file_path)}
- Es directorio: {os.path.isdir(file_path)}
        """.strip()

        return info
    except Exception as e:
        return f"Error al obtener información del archivo: {e}"

def create_note(title, content):
    """Crea una nota y la guarda en un archivo"""
    try:
        # Crear directorio de notas si no existe
        os.makedirs("notes", exist_ok=True)

        # Crear nombre de archivo seguro
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')
        filename = f"{safe_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = os.path.join("notes", filename)

        # Escribir la nota
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Título: {title}\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n")
            f.write(content)

        return f"Nota creada exitosamente: {file_path}"
    except Exception as e:
        return f"Error al crear la nota: {e}"

def execute_tool(tool_name, parameters):
    """Ejecuta una herramienta específica"""
    try:
        if tool_name == "get_weather":
            return get_weather(parameters.get("city", ""))
        elif tool_name == "calculate":
            return calculate(parameters.get("expression", ""))
        elif tool_name == "get_file_info":
            return get_file_info(parameters.get("file_path", ""))
        elif tool_name == "create_note":
            return create_note(parameters.get("title", ""), parameters.get("content", ""))
        else:
            return f"Herramienta desconocida: {tool_name}"
    except Exception as e:
        return f"Error al ejecutar la herramienta {tool_name}: {e}"

def save_conversation_to_log(conversation, log_file_path):
    """Guarda la conversación con herramientas en un archivo de log"""
    try:
        with open(log_file_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"LOG DE CONVERSACIÓN CON HERRAMIENTAS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
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
    """Guarda la conversación con herramientas en formato JSON"""
    try:
        conversation_data = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "total_messages": len(conversation),
                "model_used": "claude-sonnet-4-20250514",
                "api_provider": "anthropic",
                "features": "tools_integration",
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
    return f"log_tools_{now.strftime('%Y%m%d')}_{now.strftime('%H%M%S')}.txt"

def get_json_filename():
    """Genera el nombre del archivo JSON"""
    now = datetime.now()
    return f"log_tools_{now.strftime('%Y%m%d')}_{now.strftime('%H%M%S')}.json"

def show_tools_info():
    """Muestra información sobre las herramientas disponibles"""
    console.print("\n[bold cyan]🔧 Herramientas Disponibles:[/bold cyan]")

    tools_table = Table(title="[bold blue]Herramientas del Chatbot[/bold blue]")
    tools_table.add_column("Herramienta", style="bold", width=15)
    tools_table.add_column("Descripción", style="dim", width=40)
    tools_table.add_column("Ejemplo", style="green", width=30)

    examples = [
        "¿Qué clima hace en Madrid?",
        "Calcula 2 + 2 * 3",
        "¿Qué información tienes del archivo README.md?",
        "Crea una nota llamada 'Ideas' con 'Tengo que comprar leche'"
    ]

    for i, tool in enumerate(TOOLS):
        tools_table.add_row(
            tool["name"],
            tool["description"],
            examples[i] if i < len(examples) else "N/A"
        )

    console.print(tools_table)

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
        "[bold blue]🤖 Chatbot con Herramientas (Claude + Tools)[/bold blue]\n[dim]Claude puede usar herramientas para realizar tareas específicas[/dim]\n[dim]Escribe 'herramientas' para ver las disponibles, 'exit' para salir[/dim]",
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

        # Comando especial para mostrar herramientas
        if user_input.lower() in {"herramientas", "tools", "ayuda"}:
            show_tools_info()
            continue

        # Comando para ver contexto
        if user_input.lower() == "contexto":
            if not conversation:
                console.print("[yellow]⚠️ No hay mensajes en el contexto actual.[/yellow]")
                continue

            context_table = Table(title="[bold blue]📋 Contexto de la Conversación[/bold blue]")
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
            continue

        # Añadir mensaje del usuario
        conversation.append({"role": "user", "content": user_input})

        # Display user message
        user_panel = Panel(
            user_input,
            title="[blue]👤 Usuario[/blue]",
            border_style="blue"
        )
        console.print(user_panel)

        try:
            # Llamar a Claude con herramientas
            with console.status("[bold green]Claude está pensando y usando herramientas...", spinner="dots"):
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    messages=conversation,
                    tools=TOOLS
                )

            # Procesar la respuesta
            assistant_message = ""
            tool_results = []

            for content in response.content:
                if content.type == "text":
                    assistant_message += content.text
                elif content.type == "tool_use":
                    # Ejecutar la herramienta
                    tool_name = content.name
                    tool_input = content.input

                    console.print(f"[dim]🔧 Ejecutando herramienta: {tool_name}[/dim]")

                    result = execute_tool(tool_name, tool_input)
                    tool_results.append({
                        "tool_use_id": content.id,
                        "name": tool_name,
                        "input": tool_input,
                        "result": result
                    })

                    console.print(f"[dim]✅ Resultado: {result}[/dim]")

            # Si hay resultados de herramientas, enviarlos de vuelta a Claude
            if tool_results:
                tool_messages = []
                for tool_result in tool_results:
                    tool_messages.append({
                        "type": "tool_result",
                        "tool_use_id": tool_result["tool_use_id"],
                        "content": tool_result["result"]
                    })

                # Llamar a Claude nuevamente con los resultados
                with console.status("[bold green]Claude procesando resultados de herramientas...", spinner="dots"):
                    final_response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1000,
                        messages=conversation + [{"role": "assistant", "content": response.content}] + [{"role": "user", "content": tool_messages}]
                    )

                # Obtener la respuesta final
                final_message = ""
                for content in final_response.content:
                    if content.type == "text":
                        final_message += content.text

                assistant_message = final_message

            # Añadir respuesta del asistente
            conversation.append({"role": "assistant", "content": assistant_message})

            # Guardar conversación actualizada
            save_conversation_to_log(conversation, log_path)
            save_conversation_to_json(conversation, json_path)

            # Display assistant response
            bot_panel = Panel(
                assistant_message,
                title="[green]🤖 Claude (con Herramientas)[/green]",
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
