# 🤖 Chatbot con API de Anthropic (Claude)

Este chatbot utiliza la API de Anthropic para interactuar con Claude, el modelo de IA de Anthropic.

## 📋 Requisitos

1. **API Key de Anthropic**: Necesitas una clave API de Anthropic
2. **Python 3.9+**: Versión compatible
3. **Dependencias**: Instaladas automáticamente

## 🔧 Configuración

### 1. Obtener API Key de Anthropic

1. Ve a [console.anthropic.com](https://console.anthropic.com)
2. Crea una cuenta o inicia sesión
3. Ve a la sección "API Keys"
4. Genera una nueva API key

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con:

```env
# Anthropic API Key
ANTHROPIC_API_KEY=tu_api_key_de_anthropic_aqui
```

### 3. Instalar Dependencias

```bash
# Usando uv (recomendado)
uv sync

# O usando pip
pip install anthropic rich python-dotenv
```

## 🚀 Uso

### Ejecutar el Chatbot

```bash
python anthropic_chatbot.py
```

### Características

- **Interfaz visual atractiva** con Rich
- **Guardado automático** en TXT y JSON
- **Carga de conversaciones anteriores**
- **Comandos especiales**:
  - `contexto` - Ver historial
  - `guardar` - Guardar manualmente
  - `exit` - Salir

### Modelo Utilizado

- **Claude Sonnet 4** (claude-sonnet-4-20250514) - Modelo más reciente
- **Máximo 1000 tokens** por respuesta
- **Optimizado para conversaciones** en español
- **Mejoras en rendimiento** y capacidades

## 📁 Estructura de Archivos

```
./logs/
├── log_anthropic_20250106_143825.txt
├── log_anthropic_20250106_143825.json
├── log_anthropic_20250106_144512.txt
├── log_anthropic_20250106_144512.json
└── ...
```

## 🔄 Flujo de Trabajo

1. **Inicio**: Menú para nuevo chat o continuar anterior
2. **Selección**: Lista de conversaciones disponibles
3. **Chat**: Interacción normal con Claude
4. **Guardado**: Automático después de cada respuesta
5. **Salida**: Guardado final al salir

## ⚠️ Notas Importantes

- **API Key requerida**: Sin ella el programa no funcionará
- **Archivos separados**: Los logs de Anthropic tienen prefijo `log_anthropic_`
- **Formato JSON**: Incluye metadatos específicos de Anthropic
- **Manejo de errores**: Robusto ante fallos de API

## 🆚 Diferencias con OpenAI

| Característica | OpenAI | Anthropic |
|----------------|--------|-----------|
| Modelo | GPT-4o-mini | Claude Sonnet 4 |
| API | openai | anthropic |
| Prefijo logs | `log_` | `log_anthropic_` |
| Estructura | Completions | Messages |
| Tokens | Variable | 1000 max |

## 🐛 Solución de Problemas

### Error: "ANTHROPIC_API_KEY no encontrada"
- Verifica que el archivo `.env` existe
- Confirma que la variable está correctamente escrita
- Reinicia el programa después de añadir la key

### Error de API
- Verifica que tu API key es válida
- Confirma que tienes créditos disponibles
- Revisa la conexión a internet

## 📞 Soporte

Para problemas específicos de Anthropic:
- [Documentación oficial](https://docs.anthropic.com)
- [Console de Anthropic](https://console.anthropic.com)
