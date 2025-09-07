# 🔧 Ejemplo Completo de Herramientas con Claude

Este proyecto demuestra cómo implementar y usar herramientas (tools) con la API de Anthropic para que Claude pueda ejecutar funciones específicas y realizar tareas programáticas.

## 📁 Archivos del Proyecto

### 🤖 Chatbots Principales
- **`statefulchat-old.py`** - Chatbot OpenAI con logging y persistencia
- **`anthropic_chatbot.py`** - Chatbot Anthropic básico
- **`image_analyzer.py`** - Analizador de imágenes con Claude
- **`tools_chatbot.py`** - Chatbot con herramientas integradas

### 📚 Documentación
- **`ANTHROPIC_SETUP.md`** - Guía de configuración de Anthropic
- **`IMAGE_ANALYZER_SETUP.md`** - Guía del analizador de imágenes
- **`TOOLS_USAGE.md`** - Documentación completa de herramientas
- **`README_TOOLS.md`** - Este archivo

### 🎮 Ejemplos y Demos
- **`example_usage.py`** - Ejemplos de uso del analizador de imágenes
- **`tools_example.py`** - Demos interactivos de herramientas

## 🛠️ Herramientas Implementadas

### 1. 🌤️ **get_weather** - Consulta de Clima
```python
# Ejemplo de uso
result = get_weather("Madrid")
# Resultado: "Clima en Madrid: 22°C, soleado, humedad 45%"
```

**Ciudades soportadas**: Madrid, Barcelona, London, Paris, Tokyo

### 2. 🧮 **calculate** - Calculadora Matemática
```python
# Ejemplos de uso
calculate("2 + 2 * 3")        # Resultado: 8
calculate("sqrt(16)")         # Resultado: 4.0
calculate("sin(pi/2)")        # Resultado: 1.0
calculate("log(10)")          # Resultado: 2.302585092994046
```

**Funciones soportadas**:
- Operaciones básicas: `+`, `-`, `*`, `/`, `**`
- Trigonométricas: `sin()`, `cos()`, `tan()`
- Logaritmos: `log()`, `exp()`
- Raíz cuadrada: `sqrt()`
- Constantes: `pi`, `e`

### 3. 📁 **get_file_info** - Información de Archivos
```python
# Ejemplo de uso
result = get_file_info("README.md")
# Resultado: Información detallada del archivo
```

**Información proporcionada**:
- Tamaño del archivo
- Fecha de modificación
- Fecha de creación
- Tipo de archivo/directorio

### 4. 📝 **create_note** - Creación de Notas
```python
# Ejemplo de uso
result = create_note("Mi Nota", "Contenido de la nota")
# Resultado: "Nota creada exitosamente: notes/Mi_Nota_20250106_143025.txt"
```

**Características**:
- Título y contenido personalizables
- Timestamp automático
- Nombres de archivo seguros
- Guardado en directorio `./notes/`

## 🚀 Cómo Usar

### 1. Configuración Inicial

```bash
# Instalar dependencias
uv sync

# Configurar API key en .env
echo "ANTHROPIC_API_KEY=tu_api_key_aqui" >> .env
```

### 2. Ejecutar Chatbot con Herramientas

```bash
python tools_chatbot.py
```

### 3. Comandos Disponibles

- **`herramientas`** - Ver todas las herramientas
- **`contexto`** - Ver historial de conversación
- **`exit`** - Salir del programa

### 4. Ejemplos de Conversación

```
Tú: ¿Qué clima hace en Barcelona?
🤖 Claude: [Usa get_weather] El clima en Barcelona está parcialmente nublado con 24°C y humedad del 60%.

Tú: Calcula la raíz cuadrada de 144
🤖 Claude: [Usa calculate] La raíz cuadrada de 144 es 12.0.

Tú: Crea una nota llamada "Ideas" con "Desarrollar una app móvil"
🤖 Claude: [Usa create_note] Nota creada exitosamente: notes/Ideas_20250106_143025.txt
```

## 🎮 Demos Interactivos

### Demo de Herramientas
```bash
python tools_example.py
```

**Opciones disponibles**:
1. Demo de Clima
2. Demo de Calculadora
3. Demo de Información de Archivos
4. Demo de Creación de Notas
5. Demo de Ejecución de Herramientas
6. Ver Herramientas Disponibles
7. Demo Interactivo

### Demo de Análisis de Imágenes
```bash
python image_analyzer.py
```

**Características**:
- Análisis de imágenes con Claude
- Múltiples formatos soportados
- Preguntas personalizables
- Historial de análisis

## 📊 Flujo de Trabajo de Herramientas

### 1. **Definición de Herramientas**
```python
TOOLS = [
    {
        "name": "mi_herramienta",
        "description": "Descripción de la herramienta",
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
]
```

### 2. **Implementación de Función**
```python
def mi_herramienta(parametro):
    """Implementación de la herramienta"""
    try:
        # Lógica de la herramienta
        return "Resultado"
    except Exception as e:
        return f"Error: {e}"
```

### 3. **Integración con Claude**
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=conversation,
    tools=TOOLS  # Pasar herramientas
)
```

### 4. **Procesamiento de Respuestas**
```python
for content in response.content:
    if content.type == "text":
        # Respuesta de texto
        assistant_message += content.text
    elif content.type == "tool_use":
        # Llamada a herramienta
        result = execute_tool(content.name, content.input)
```

## 📁 Estructura de Archivos Generados

```
./logs/
├── log_tools_20250106_143825.txt      # Logs de herramientas
├── log_tools_20250106_143825.json     # JSON de herramientas
├── image_analysis_20250106_143825.txt # Logs de análisis de imágenes
├── image_analysis_20250106_143825.json # JSON de análisis de imágenes
└── ...

./notes/
├── Ideas_20250106_143025.txt          # Notas creadas
├── Tareas_20250106_143045.txt
└── ...
```

## 🔧 Añadir Nuevas Herramientas

### Paso 1: Definir la Herramienta
```python
new_tool = {
    "name": "mi_nueva_herramienta",
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

# Añadir a la lista TOOLS
TOOLS.append(new_tool)
```

### Paso 2: Implementar la Función
```python
def mi_nueva_herramienta(parametro):
    """Implementación de la nueva herramienta"""
    try:
        # Lógica de la herramienta
        return "Resultado exitoso"
    except Exception as e:
        return f"Error: {e}"
```

### Paso 3: Añadir al Ejecutor
```python
def execute_tool(tool_name, parameters):
    if tool_name == "mi_nueva_herramienta":
        return mi_nueva_herramienta(parameters.get("parametro", ""))
    # ... otras herramientas existentes
```

## 🎯 Casos de Uso Prácticos

### 1. **Asistente de Productividad**
- Crear notas automáticamente
- Calcular fechas y tiempos
- Gestionar archivos

### 2. **Consultor Técnico**
- Realizar cálculos complejos
- Analizar archivos del sistema
- Proporcionar información técnica

### 3. **Asistente de Datos**
- Consultar APIs externas
- Procesar información
- Generar reportes

### 4. **Bot de Automatización**
- Ejecutar tareas repetitivas
- Integrar con sistemas externos
- Automatizar flujos de trabajo

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'requests'"
- **Solución**: El módulo `requests` no es necesario, ya fue removido

### Error: "ANTHROPIC_API_KEY no encontrada"
- **Solución**: Configurar la API key en el archivo `.env`

### Error: "Herramienta desconocida"
- **Solución**: Verificar que la herramienta esté definida en `TOOLS` e implementada en `execute_tool`

### Error: "Parámetros inválidos"
- **Solución**: Revisar el esquema de entrada de la herramienta

## 📈 Ventajas de las Herramientas

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

## 🚀 Próximos Pasos

### Mejoras Sugeridas
- [ ] Añadir más herramientas (búsqueda web, email, etc.)
- [ ] Implementar autenticación para APIs externas
- [ ] Añadir validación de parámetros más robusta
- [ ] Crear interfaz web para las herramientas
- [ ] Implementar logging más detallado

### Herramientas Adicionales
- [ ] **Web Search** - Búsqueda en internet
- [ ] **Email** - Envío de correos
- [ ] **Database** - Consultas a bases de datos
- [ ] **Calendar** - Gestión de calendario
- [ ] **Translation** - Traducción de textos

¡El sistema de herramientas está completamente funcional y listo para usar! 🎉
