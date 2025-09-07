# 🔧 Uso de Herramientas con Claude (Tools)

Este chatbot demuestra cómo usar herramientas (tools) con la API de Anthropic para que Claude pueda interactuar con funciones externas y realizar tareas específicas.

## 📋 ¿Qué son las Herramientas?

Las herramientas permiten que Claude:
- **Ejecute funciones** específicas del sistema
- **Acceda a APIs externas** para obtener datos
- **Realice cálculos** complejos
- **Interactúe con archivos** del sistema
- **Procese información** de manera programática

## 🛠️ Herramientas Implementadas

### 1. 🌤️ **get_weather** - Clima
**Descripción**: Obtiene el clima actual de una ciudad específica

**Parámetros**:
- `city` (string): Nombre de la ciudad

**Ejemplo de uso**:
```
Usuario: ¿Qué clima hace en Madrid?
Claude: [Usa get_weather] El clima en Madrid es soleado, 22°C, humedad 45%
```

**Ciudades disponibles**: Madrid, Barcelona, London, Paris, Tokyo

### 2. 🧮 **calculate** - Calculadora
**Descripción**: Realiza cálculos matemáticos básicos

**Parámetros**:
- `expression` (string): Expresión matemática a calcular

**Ejemplo de uso**:
```
Usuario: Calcula 2 + 2 * 3
Claude: [Usa calculate] Resultado: 8

Usuario: ¿Cuál es la raíz cuadrada de 16?
Claude: [Usa calculate] Resultado: 4.0
```

**Funciones soportadas**:
- Operaciones básicas: `+`, `-`, `*`, `/`, `**`
- Funciones trigonométricas: `sin()`, `cos()`, `tan()`
- Logaritmos: `log()`, `exp()`
- Raíz cuadrada: `sqrt()`
- Constantes: `pi`, `e`

### 3. 📁 **get_file_info** - Información de Archivos
**Descripción**: Obtiene información detallada sobre un archivo

**Parámetros**:
- `file_path` (string): Ruta del archivo a analizar

**Ejemplo de uso**:
```
Usuario: ¿Qué información tienes del archivo README.md?
Claude: [Usa get_file_info]
Información del archivo: README.md
- Tamaño: 1024 bytes
- Modificado: 2025-01-06 14:30:15
- Creado: 2025-01-06 14:30:15
- Es archivo: True
- Es directorio: False
```

### 4. 📝 **create_note** - Crear Notas
**Descripción**: Crea una nota y la guarda en un archivo

**Parámetros**:
- `title` (string): Título de la nota
- `content` (string): Contenido de la nota

**Ejemplo de uso**:
```
Usuario: Crea una nota llamada "Ideas" con "Tengo que comprar leche"
Claude: [Usa create_note] Nota creada exitosamente: notes/Ideas_20250106_143025.txt
```

## 🚀 Cómo Usar

### 1. Ejecutar el Chatbot con Herramientas

```bash
python tools_chatbot.py
```

### 2. Comandos Especiales

- **`herramientas`** - Muestra todas las herramientas disponibles
- **`contexto`** - Ve el historial de la conversación
- **`exit`** - Salir del programa

### 3. Ejemplos de Conversación

```
🤖 Chatbot con Herramientas (Claude + Tools)
Tú: ¿Qué clima hace en Barcelona?

🔧 Ejecutando herramienta: get_weather
✅ Resultado: Clima en Barcelona: 24°C, parcialmente nublado, humedad 60%

🤖 Claude: El clima en Barcelona está parcialmente nublado con una temperatura de 24°C y una humedad del 60%. Es un día bastante agradable para estar al aire libre.
```

## 🔄 Flujo de Trabajo

### 1. **Usuario hace pregunta**
```
Usuario: Calcula la raíz cuadrada de 144
```

### 2. **Claude identifica herramienta necesaria**
```
Claude: [Identifica que necesita calculate]
```

### 3. **Claude llama a la herramienta**
```
🔧 Ejecutando herramienta: calculate
✅ Resultado: Resultado: 12.0
```

### 4. **Claude procesa el resultado**
```
🤖 Claude: La raíz cuadrada de 144 es 12.0
```

## 📁 Estructura de Archivos

```
./logs/
├── log_tools_20250106_143825.txt
├── log_tools_20250106_143825.json
├── log_tools_20250106_144512.txt
├── log_tools_20250106_144512.json
└── ...

./notes/
├── Ideas_20250106_143025.txt
├── Tareas_20250106_143045.txt
└── ...
```

## 🎯 Casos de Uso Prácticos

### 1. **Asistente de Productividad**
```
Usuario: Crea una nota con mis tareas del día
Claude: [Usa create_note] Nota creada con tus tareas
```

### 2. **Calculadora Inteligente**
```
Usuario: Necesito calcular el área de un círculo con radio 5
Claude: [Usa calculate] El área es 78.54 unidades cuadradas
```

### 3. **Consultor de Clima**
```
Usuario: ¿Debería llevar paraguas a Londres?
Claude: [Usa get_weather] En Londres está lluvioso, sí deberías llevar paraguas
```

### 4. **Administrador de Archivos**
```
Usuario: ¿Qué información tienes del archivo config.json?
Claude: [Usa get_file_info] Te muestro los detalles del archivo...
```

## ⚙️ Configuración Técnica

### Definición de Herramientas

```python
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
    }
    # ... más herramientas
]
```

### Llamada a la API

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=conversation,
    tools=TOOLS  # Pasar las herramientas
)
```

### Procesamiento de Respuestas

```python
for content in response.content:
    if content.type == "text":
        # Respuesta de texto
        assistant_message += content.text
    elif content.type == "tool_use":
        # Llamada a herramienta
        result = execute_tool(content.name, content.input)
```

## 🔧 Añadir Nuevas Herramientas

### 1. **Definir la herramienta**
```python
{
    "name": "mi_herramienta",
    "description": "Descripción de lo que hace",
    "input_schema": {
        "type": "object",
        "properties": {
            "parametro": {
                "type": "string",
                "description": "Descripción del parámetro"
            }
        },
        "required": ["parametro"]
    }
}
```

### 2. **Implementar la función**
```python
def mi_herramienta(parametro):
    """Implementación de la herramienta"""
    try:
        # Lógica de la herramienta
        return "Resultado"
    except Exception as e:
        return f"Error: {e}"
```

### 3. **Añadir al ejecutor**
```python
def execute_tool(tool_name, parameters):
    if tool_name == "mi_herramienta":
        return mi_herramienta(parameters.get("parametro", ""))
    # ... otras herramientas
```

## 🐛 Solución de Problemas

### Error: "Herramienta desconocida"
- Verifica que la herramienta esté definida en `TOOLS`
- Confirma que esté implementada en `execute_tool`

### Error: "Parámetros inválidos"
- Revisa el esquema de entrada de la herramienta
- Verifica que los parámetros requeridos estén presentes

### Error: "API Key no encontrada"
- Configura `ANTHROPIC_API_KEY` en el archivo `.env`
- Reinicia el programa después de añadir la key

## 📊 Ventajas de las Herramientas

### 1. **Extensibilidad**
- Añade nuevas capacidades fácilmente
- Integra con APIs externas
- Personaliza el comportamiento

### 2. **Precisión**
- Claude puede usar herramientas específicas
- Resultados más precisos y confiables
- Menos errores en cálculos complejos

### 3. **Interactividad**
- Claude puede realizar acciones
- No solo responde, sino que actúa
- Experiencia más dinámica

### 4. **Modularidad**
- Herramientas independientes
- Fácil mantenimiento
- Reutilización de código

## 🎮 Ejemplos Avanzados

### Análisis de Datos
```
Usuario: Analiza el archivo data.csv y calcula el promedio
Claude: [Usa get_file_info] + [Usa calculate] Te muestro el análisis...
```

### Automatización
```
Usuario: Crea una nota con el clima de 3 ciudades
Claude: [Usa get_weather] 3 veces + [Usa create_note] Nota creada...
```

### Cálculos Complejos
```
Usuario: Calcula la hipotenusa de un triángulo con catetos 3 y 4
Claude: [Usa calculate] La hipotenusa es 5.0
```

¡Las herramientas hacen que Claude sea mucho más poderoso y útil! 🚀
