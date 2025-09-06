# 🖼️ Analizador de Imágenes con Claude

Este analizador utiliza la API de Anthropic para analizar imágenes usando Claude, proporcionando descripciones detalladas y respuestas a preguntas específicas sobre el contenido visual.

## 📋 Características

- **Análisis inteligente** de imágenes con Claude Sonnet 4
- **Múltiples formatos** soportados (JPG, PNG, GIF, WebP, BMP)
- **Preguntas personalizadas** sobre las imágenes
- **Guardado automático** de análisis en TXT y JSON
- **Historial de análisis** con interfaz visual
- **Interfaz Rich** atractiva y fácil de usar

## 🔧 Requisitos

1. **API Key de Anthropic**: Necesaria para usar Claude
2. **Python 3.9+**: Versión compatible
3. **Dependencias**: Instaladas automáticamente
4. **Imágenes**: En formatos soportados

## 🚀 Instalación

### 1. Instalar Dependencias

```bash
# Usando uv (recomendado)
uv sync

# O usando pip
pip install anthropic rich python-dotenv
```

### 2. Configurar API Key

Añade tu API key de Anthropic al archivo `.env`:

```env
ANTHROPIC_API_KEY=tu_api_key_de_anthropic_aqui
```

## 🎮 Uso

### Ejecutar el Analizador

```bash
python image_analyzer.py
```

### Menú Principal

Al ejecutar el programa verás:

```
🖼️ Analizador de Imágenes con Claude
¿Qué deseas hacer?
1. Analizar una imagen
2. Ver análisis anteriores
3. Salir
```

### Analizar una Imagen

1. **Selecciona opción 1**
2. **Proporciona la ruta** de la imagen
3. **Escribe tu pregunta** (o usa la predeterminada)
4. **Claude analizará** la imagen
5. **Ve el resultado** en un panel visual
6. **El análisis se guarda** automáticamente

### Ejemplos de Preguntas

- `"Describe esta imagen en detalle"`
- `"¿Qué objetos veo en esta imagen?"`
- `"Analiza los colores y la composición"`
- `"¿Qué emociones transmite esta imagen?"`
- `"Identifica las personas en la imagen"`
- `"¿Qué actividad está ocurriendo?"`

## 📁 Formatos Soportados

| Formato | Extensión | Descripción |
|---------|-----------|-------------|
| **JPEG** | .jpg, .jpeg | Imágenes fotográficas |
| **PNG** | .png | Imágenes con transparencia |
| **GIF** | .gif | Imágenes animadas |
| **WebP** | .webp | Formato moderno |
| **BMP** | .bmp | Mapa de bits |

## 💾 Sistema de Guardado

### Archivos Generados

```
./logs/
├── image_analysis_20250106_143825.txt
├── image_analysis_20250106_143825.json
├── image_analysis_20250106_144512.txt
├── image_analysis_20250106_144512.json
└── ...
```

### Formato TXT

```
================================================================================
ANÁLISIS DE IMAGEN - 2025-01-06 14:38:25
================================================================================
Imagen: /ruta/a/imagen.jpg
Pregunta: Describe esta imagen en detalle
--------------------------------------------------------------------------------
Análisis:
[Descripción detallada de Claude]
================================================================================
```

### Formato JSON

```json
{
  "metadata": {
    "created_at": "2025-01-06T14:38:25.123456",
    "total_analyses": 1,
    "model_used": "claude-sonnet-4-20250514",
    "api_provider": "anthropic",
    "version": "1.0",
    "last_updated": "2025-01-06T14:38:25.123456"
  },
  "analyses": [
    {
      "timestamp": "2025-01-06T14:38:25.123456",
      "image_path": "/ruta/a/imagen.jpg",
      "question": "Describe esta imagen en detalle",
      "analysis": "[Análisis de Claude]"
    }
  ]
}
```

## 🔍 Ver Análisis Anteriores

### Opción 2: Historial

- **Lista visual** de todos los análisis
- **Información detallada** (fecha, tamaño, archivo)
- **Ver análisis específicos** seleccionando por número
- **Navegación fácil** entre análisis

## ⚙️ Configuración Avanzada

### Límites de la API

- **Máximo 1000 tokens** por análisis
- **Tamaño de imagen**: Limitado por la API de Anthropic
- **Formatos**: Solo los soportados por Claude

### Personalización

Puedes modificar el archivo `image_analyzer.py` para:

- **Cambiar el modelo** de Claude
- **Ajustar tokens** máximos
- **Modificar preguntas** predeterminadas
- **Personalizar** la interfaz

## 🐛 Solución de Problemas

### Error: "Archivo no encontrado"

- **Verifica la ruta** de la imagen
- **Usa rutas absolutas** si es necesario
- **Confirma** que el archivo existe

### Error: "Formato no soportado"

- **Convierte la imagen** a un formato soportado
- **Usa herramientas** como GIMP o Photoshop
- **Verifica la extensión** del archivo

### Error: "API Key no encontrada"

- **Verifica** el archivo `.env`
- **Confirma** que la variable está correcta
- **Reinicia** el programa

### Error de API

- **Verifica** tu API key
- **Confirma** que tienes créditos
- **Revisa** la conexión a internet

## 📊 Casos de Uso

### 🎨 Análisis Artístico

- **Composición** y elementos visuales
- **Colores** y paleta
- **Estilo** y técnica
- **Emociones** transmitidas

### 🔍 Identificación de Objetos

- **Objetos** presentes en la imagen
- **Personas** y sus actividades
- **Lugares** y entornos
- **Textos** y signos

### 📸 Análisis Fotográfico

- **Calidad** técnica de la foto
- **Iluminación** y exposición
- **Enfoque** y profundidad
- **Composición** fotográfica

### 🏥 Análisis Médico (Básico)

- **Estructuras** visibles
- **Patrones** y formas
- **Colores** y texturas
- **Nota**: No reemplaza diagnóstico médico

## 🆚 Comparación con Otros Analizadores

| Característica | Este Analizador | Otros |
|----------------|-----------------|-------|
| **Modelo** | Claude Sonnet 4 | Varios |
| **Interfaz** | Rich (Visual) | Básica |
| **Guardado** | TXT + JSON | Variable |
| **Historial** | Completo | Limitado |
| **Formatos** | 5 soportados | Variable |
| **Preguntas** | Personalizables | Fijas |

## 📞 Soporte

Para problemas específicos:

- **Documentación Anthropic**: [docs.anthropic.com](https://docs.anthropic.com)
- **Console Anthropic**: [console.anthropic.com](https://console.anthropic.com)
- **Issues del proyecto**: Crear issue en GitHub

## 🔄 Actualizaciones

### Versión 1.0
- ✅ Análisis básico de imágenes
- ✅ Múltiples formatos soportados
- ✅ Interfaz Rich
- ✅ Guardado automático
- ✅ Historial de análisis

### Próximas Versiones
- 🔄 Análisis por lotes
- 🔄 Comparación de imágenes
- 🔄 Exportación a PDF
- 🔄 Integración con APIs de almacenamiento
