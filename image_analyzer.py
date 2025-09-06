import os
import json
import base64
import dotenv
from datetime import datetime
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import print as rprint
from pathlib import Path

dotenv.load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
console = Console()

def encode_image_to_base64(image_path):
    """Codifica una imagen a base64 para enviar a la API"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        console.print(f"[red]Error al codificar la imagen: {e}[/red]")
        return None

def get_image_media_type(image_path):
    """Determina el tipo de media de la imagen basado en la extensión"""
    extension = Path(image_path).suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp'
    }
    return media_types.get(extension, 'image/jpeg')

def analyze_image(image_path, question="Describe esta imagen en detalle"):
    """Analiza una imagen usando Claude"""
    try:
        # Verificar que el archivo existe
        if not os.path.exists(image_path):
            console.print(f"[red]❌ El archivo no existe: {image_path}[/red]")
            return None

        # Verificar que es una imagen
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
        if not any(image_path.lower().endswith(ext) for ext in valid_extensions):
            console.print(f"[red]❌ Formato de imagen no soportado. Usa: {', '.join(valid_extensions)}[/red]")
            return None

        # Codificar imagen
        console.print(f"[dim]📷 Procesando imagen: {os.path.basename(image_path)}[/dim]")
        image_data = encode_image_to_base64(image_path)
        if not image_data:
            return None

        # Llamar a la API de Anthropic
        with console.status("[bold green]Claude analizando la imagen...", spinner="dots"):
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": question
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": get_image_media_type(image_path),
                                    "data": image_data
                                }
                            }
                        ]
                    }
                ]
            )

        return response.content[0].text.strip()

    except Exception as e:
        console.print(f"[red]❌ Error al analizar la imagen: {e}[/red]")
        return None

def save_image_analysis(image_path, question, analysis, log_file_path):
    """Guarda el análisis de imagen en un archivo de log"""
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"ANÁLISIS DE IMAGEN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Imagen: {image_path}\n")
            f.write(f"Pregunta: {question}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Análisis:\n{analysis}\n")
            f.write("=" * 80 + "\n\n")
    except Exception as e:
        console.print(f"[red]Error al guardar el análisis: {e}[/red]")

def save_image_analysis_to_json(image_path, question, analysis, json_file_path):
    """Guarda el análisis de imagen en formato JSON"""
    try:
        # Cargar datos existentes o crear nuevos
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "total_analyses": 0,
                    "model_used": "claude-sonnet-4-20250514",
                    "api_provider": "anthropic",
                    "version": "1.0"
                },
                "analyses": []
            }

        # Añadir nuevo análisis
        analysis_data = {
            "timestamp": datetime.now().isoformat(),
            "image_path": image_path,
            "question": question,
            "analysis": analysis
        }

        data["analyses"].append(analysis_data)
        data["metadata"]["total_analyses"] = len(data["analyses"])
        data["metadata"]["last_updated"] = datetime.now().isoformat()

        # Guardar archivo
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        console.print(f"[red]Error al guardar el JSON: {e}[/red]")

def get_image_log_filename():
    """Genera el nombre del archivo de log para análisis de imágenes"""
    now = datetime.now()
    return f"image_analysis_{now.strftime('%Y%m%d')}_{now.strftime('%H%M%S')}.txt"

def get_image_json_filename():
    """Genera el nombre del archivo JSON para análisis de imágenes"""
    now = datetime.now()
    return f"image_analysis_{now.strftime('%Y%m%d')}_{now.strftime('%H%M%S')}.json"

def show_image_menu():
    """Muestra el menú principal para análisis de imágenes"""
    console.print("\n")
    welcome_panel = Panel(
        "[bold blue]🖼️ Analizador de Imágenes con Claude[/bold blue]\n[dim]Análisis inteligente de imágenes usando IA[/dim]\n[dim]Formatos soportados: JPG, PNG, GIF, WebP, BMP[/dim]",
        title="[green]Bienvenido[/green]",
        border_style="blue"
    )
    console.print(welcome_panel)

    console.print("\n[bold cyan]¿Qué deseas hacer?[/bold cyan]")
    console.print("[bold green]1.[/bold green] Analizar una imagen")
    console.print("[bold yellow]2.[/bold yellow] Ver análisis anteriores")
    console.print("[bold red]3.[/bold red] Salir")

    while True:
        try:
            choice = Prompt.ask("\n[bold]Selecciona una opción (1, 2 o 3)[/bold]", choices=["1", "2", "3"])
            return choice
        except KeyboardInterrupt:
            console.print("\n[yellow]Saliendo...[/yellow]")
            return "3"

def get_image_path():
    """Solicita la ruta de la imagen al usuario"""
    while True:
        image_path = Prompt.ask("\n[bold]Ruta de la imagen[/bold]")

        # Expandir ruta si es relativa
        if not os.path.isabs(image_path):
            image_path = os.path.abspath(image_path)

        if os.path.exists(image_path):
            return image_path
        else:
            console.print(f"[red]❌ Archivo no encontrado: {image_path}[/red]")
            console.print("[dim]Intenta con una ruta diferente o usa Ctrl+C para salir[/dim]")

def get_analysis_question():
    """Solicita la pregunta de análisis al usuario"""
    console.print("\n[bold cyan]Pregunta de análisis:[/bold cyan]")
    console.print("[dim]Ejemplos:[/dim]")
    console.print("[dim]• 'Describe esta imagen en detalle'[/dim]")
    console.print("[dim]• '¿Qué objetos veo en esta imagen?'[/dim]")
    console.print("[dim]• 'Analiza los colores y la composición'[/dim]")
    console.print("[dim]• '¿Qué emociones transmite esta imagen?'[/dim]")

    question = Prompt.ask("\n[bold]Tu pregunta[/bold]")
    return question if question.strip() else "Describe esta imagen en detalle"

def list_previous_analyses():
    """Lista los análisis anteriores disponibles"""
    try:
        if not os.path.exists("logs"):
            console.print("[yellow]⚠️ No hay análisis anteriores disponibles.[/yellow]")
            return

        json_files = []
        for filename in os.listdir("logs"):
            if filename.endswith(".json") and filename.startswith("image_analysis_"):
                file_path = os.path.join("logs", filename)
                stat = os.stat(file_path)
                created_time = datetime.fromtimestamp(stat.st_ctime)
                json_files.append({
                    "filename": filename,
                    "filepath": file_path,
                    "created": created_time,
                    "size": stat.st_size
                })

        if not json_files:
            console.print("[yellow]⚠️ No hay análisis anteriores disponibles.[/yellow]")
            return

        # Ordenar por fecha (más reciente primero)
        json_files.sort(key=lambda x: x["created"], reverse=True)

        console.print(f"\n[bold cyan]📋 Análisis anteriores disponibles ({len(json_files)}):[/bold cyan]")

        table = Table(title="[bold blue]Análisis de Imágenes Anteriores[/bold blue]")
        table.add_column("Nº", style="bold", width=4)
        table.add_column("Archivo", style="dim", width=30)
        table.add_column("Fecha", style="cyan", width=20)
        table.add_column("Tamaño", style="green", width=10)

        for i, analysis in enumerate(json_files, 1):
            table.add_row(
                str(i),
                analysis["filename"],
                analysis["created"].strftime("%Y-%m-%d %H:%M:%S"),
                f"{analysis['size']} bytes"
            )

        console.print(table)

        # Permitir ver un análisis específico
        try:
            choice = Prompt.ask(f"\n[bold]Selecciona un análisis para ver (1-{len(json_files)}) o Enter para continuar[/bold]")
            if choice.strip():
                choice_num = int(choice)
                if 1 <= choice_num <= len(json_files):
                    view_analysis_details(json_files[choice_num - 1]["filepath"])
        except (ValueError, KeyboardInterrupt):
            pass

    except Exception as e:
        console.print(f"[red]Error al listar análisis: {e}[/red]")

def view_analysis_details(json_file_path):
    """Muestra los detalles de un análisis específico"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        console.print(f"\n[bold blue]📄 Análisis: {os.path.basename(json_file_path)}[/bold blue]")
        console.print(f"[dim]📅 Creado: {data['metadata']['created_at']}[/dim]")
        console.print(f"[dim]📊 Total de análisis: {data['metadata']['total_analyses']}[/dim]")

        for i, analysis in enumerate(data['analyses'], 1):
            console.print(f"\n[bold green]--- Análisis {i} ---[/bold green]")
            console.print(f"[bold]Imagen:[/bold] {analysis['image_path']}")
            console.print(f"[bold]Pregunta:[/bold] {analysis['question']}")
            console.print(f"[bold]Análisis:[/bold] {analysis['analysis']}")

    except Exception as e:
        console.print(f"[red]Error al ver el análisis: {e}[/red]")

def main():
    # Verificar API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]❌ Error: ANTHROPIC_API_KEY no encontrada en el archivo .env[/red]")
        console.print("[dim]Por favor, añade tu API key de Anthropic al archivo .env[/dim]")
        return

    # Crear directorio de logs si no existe
    os.makedirs("logs", exist_ok=True)

    while True:
        choice = show_image_menu()

        if choice == "1":
            # Analizar imagen
            try:
                image_path = get_image_path()
                question = get_analysis_question()

                # Realizar análisis
                analysis = analyze_image(image_path, question)

                if analysis:
                    # Mostrar resultado
                    result_panel = Panel(
                        analysis,
                        title="[green]🤖 Análisis de Claude[/green]",
                        border_style="green"
                    )
                    console.print(result_panel)

                    # Guardar análisis
                    log_filename = get_image_log_filename()
                    json_filename = get_image_json_filename()
                    log_path = os.path.join("logs", log_filename)
                    json_path = os.path.join("logs", json_filename)

                    save_image_analysis(image_path, question, analysis, log_path)
                    save_image_analysis_to_json(image_path, question, analysis, json_path)

                    console.print(f"[green]✅ Análisis guardado en: {log_path}[/green]")
                    console.print(f"[green]✅ Análisis guardado en JSON: {json_path}[/green]")
                else:
                    console.print("[red]❌ No se pudo analizar la imagen[/red]")

            except KeyboardInterrupt:
                console.print("\n[yellow]Análisis cancelado[/yellow]")
                continue

        elif choice == "2":
            # Ver análisis anteriores
            list_previous_analyses()

        elif choice == "3":
            # Salir
            goodbye_panel = Panel(
                "[bold green]¡Hasta luego![/bold green]",
                title="[red]Despedida[/red]",
                border_style="red"
            )
            console.print(goodbye_panel)
            break

if __name__ == "__main__":
    main()
