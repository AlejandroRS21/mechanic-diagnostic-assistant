# 🌐 Multi-Language Support - Detección Automática de Idioma

**Fecha**: Diciembre 5, 2025  
**Feature**: Detección automática de idioma y respuesta multilingüe

---

## 📝 Resumen

El agente ahora detecta automáticamente el idioma en el que el usuario realiza la pregunta y responde en el **mismo idioma**. Esto proporciona una mejor experiencia para usuarios en diferentes idiomas.

---

## 🎯 Idiomas Soportados

| Código | Idioma | Ejemplo |
|--------|--------|---------|
| `es` | Español | "¿Tengo un código P0420, qué significa?" |
| `en` | English | "What does the P0420 code mean?" |
| `pt` | Português | "O que significa o código P0420?" |
| `fr` | Français | "Que signifie le code P0420?" |

---

## 🔧 Implementación Técnica

### 1. **Nuevo Módulo: `src/utils/language_detector.py`**

Proporciona dos clases principales:

#### `LanguageDetector`
- Detecta el idioma usando patrones regex
- Basado en palabras clave y caracteres específicos del idioma
- Retorna código ISO 639-1 (es, en, pt, fr)

```python
from src.utils.language_detector import LanguageDetector

lang = LanguageDetector.detect_language("¿Hola, cómo estás?")
# Retorna: "es"
```

#### `LanguageInstructions`
- Proporciona instrucciones específicas para cada idioma
- Se agregan al prompt del LLM
- Aseguran que el modelo responda en el idioma correcto

```python
instruction = LanguageInstructions.get_language_instruction("es")
# Retorna instrucción en español para el LLM
```

### 2. **Actualización: `src/agent/mechanic_agent.py`**

**Cambios**:
- Importa `LanguageDetector` y `LanguageInstructions`
- En el método `chat()`, detecta el idioma del usuario
- Adjunta la instrucción de idioma al input del LLM

```python
def chat(self, message: str) -> Dict[str, Any]:
    # Detectar idioma
    detected_language = LanguageDetector.detect_language(message)
    language_instruction = LanguageInstructions.get_language_instruction(detected_language)
    
    # Agregar instrucción al prompt
    full_input = f"{message}\n\n[SYSTEM: {language_instruction}]"
    
    # ... resto del procesamiento
```

### 3. **Actualización: `src/agent/prompts.py`**

El `SYSTEM_PROMPT` ahora incluye:
- Instrucción de "LANGUAGE AWARENESS"
- Indicación de prestar atención a instrucciones de idioma
- Énfasis en mantener el mismo idioma en respuestas

```python
SYSTEM_PROMPT = """
...
LANGUAGE AWARENESS: Pay attention to any [SYSTEM: ...] instructions about language.
If the user communicated in Spanish, Portuguese, or French, you MUST respond in that SAME language.
...
"""
```

### 4. **Actualización: `app.py`**

**Cambios en `chat_with_agent()`**:
- Detecta idioma de entrada del usuario
- Muestra idioma detectado en el UI
- Status bar ahora incluye: `🤖 {modelo} | 🌐 {idioma}`

```python
detected_lang = LanguageDetector.detect_language(message)
lang_name = LanguageDetector.get_language_name(detected_lang)
status_msg = f"🤖 {model_name} | 🌐 {lang_name}"
```

---

## 🎨 Interfaz Gráfica

### Antes
```
ℹ️ Modelo actual: mistralai/mistral-7b-instruct:free
```

### Después
```
🤖 mistralai/mistral-7b-instruct:free | 🌐 Spanish
```

El usuario ve claramente:
1. Qué modelo se está usando (🤖)
2. Qué idioma detectó (🌐)

---

## 📊 Flujo de Detección

```
Usuario escribe: "¿Tengo un código P0420?"
        ↓
LanguageDetector.detect_language()
        ↓
Busca patrones en el texto:
  - Palabras clave: "tengo", "código"
  - Caracteres: "¿"
  - Otros indicadores
        ↓
Retorna: "es" (Spanish)
        ↓
LanguageInstructions.get_language_instruction("es")
        ↓
Adjunta al LLM:
"¿Tengo un código P0420?

[SYSTEM: Importante: El usuario escribió en español, así que DEBES responder completamente en español...]"
        ↓
LLM responde en español
```

---

## ✅ Ejemplos de Uso

### Entrada en Español
```
Usuario: "¿Tengo un código P0420 en mi Honda. Qué significa?"

Detector: Español (es)
Agente responde completamente en español:
"El código P0420 se refiere a: Catalytic System Efficiency Below Threshold...
En tu Honda, esto usualmente significa que el convertidor catalítico necesita reemplazo..."
```

### Entrada en Inglés
```
Usuario: "What does code P0420 mean in my Honda?"

Detector: English (en)
Agente responde completamente en inglés:
"The P0420 code indicates: Catalytic System Efficiency Below Threshold...
In your Honda, this typically means the catalytic converter needs replacement..."
```

### Entrada en Portugués
```
Usuario: "O que significa o código P0420 no meu carro?"

Detector: Portuguese (pt)
Agente responde completamente en português:
"O código P0420 significa: Eficiência do Sistema Catalítico Abaixo do Limite...
No seu carro, isso geralmente significa que o conversor catalítico precisa de substituição..."
```

---

## 🔍 Detección Inteligente

El detector utiliza **múltiples estrategias**:

### 1. **Palabras Clave Específicas del Idioma**

**Español**: hola, tengo, qué, cómo, dónde, automático, convertidor
**English**: hello, I have, what, how, where, automatic, converter
**Portuguese**: olá, tenho, o que, como, onde, conversão
**French**: bonjour, ai, quoi, comment, où, conversion

### 2. **Caracteres Específicos del Idioma**

**Español**: á, é, í, ó, ú, ü, ñ, ¿, ¡
**Portuguese**: ã, õ, ê, ç
**French**: à, â, ä, ç, é, è, ê, ë
**English**: No caracteres especiales (a-z, A-Z)

### 3. **Scoring Ponderado**

Cada coincidencia suma puntos. El idioma con el score más alto gana.

---

## 🚀 Ventajas

1. ✅ **Experiencia Mejorada**: Usuarios reciben respuestas en su idioma
2. ✅ **Automático**: No requiere configuración del usuario
3. ✅ **Escalable**: Fácil agregar más idiomas
4. ✅ **Transparente**: UI muestra qué idioma detectó
5. ✅ **Robusto**: Patrones múltiples para detección confiable

---

## ⚙️ Configuración

### Para agregar un nuevo idioma:

1. **Editar `language_detector.py`**:
```python
LANGUAGE_PATTERNS = {
    "it": {  # Italiano
        "name": "Italian",
        "patterns": [
            r"\b(ciao|hello|cosa|come|dove|quando)\b",
            r"[àèéìòù]",  # Caracteres italianos
        ]
    },
}
```

2. **Agregar instrucción en `LanguageInstructions`**:
```python
INSTRUCTIONS = {
    "it": """Importante: L'utente ha scritto in italiano, quindi DEVI rispondere completamente in italiano...""",
}
```

3. **Agregar palabras clave en `mechanic_agent.py`**:
```python
keywords = [..., "codice", "guasto", "auto"]  # Italiano
```

---

## 🧪 Pruebas

### Ejecutar test de detección:
```bash
python src/utils/language_detector.py
```

**Salida esperada**:
```
Text: ¿Tengo un código P0420, qué significa?...
Detected: Spanish (es)

Text: Hello, what does the P0420 code mean?...
Detected: English (en)

Text: Olá, o que significa o código P0420?...
Detected: Portuguese (pt)

Text: Bonjour, que signifie le code P0420?...
Detected: French (fr)
```

---

## 📋 Notas Técnicas

### Limitaciones Conocidas

1. Textos muy cortos (< 3 caracteres) se asumen como English
2. Textos mixtos en múltiples idiomas: detecta el dominante
3. Jerga técnica uniforme (p.ej., "P0420") no afecta mucho

### Mejoras Futuras

- Usar librería `langdetect` para precisión mejorada
- Machine Learning para detección más sofisticada
- Soportar más idiomas (alemán, italiano, etc.)
- Detección de código-switching (cambio entre idiomas)

---

## 📄 Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `src/utils/language_detector.py` | ✅ Nuevo archivo |
| `src/agent/mechanic_agent.py` | ✅ Detecta idioma, adjunta instrucción |
| `src/agent/prompts.py` | ✅ Agregado LANGUAGE AWARENESS |
| `app.py` | ✅ Muestra idioma detectado en UI |

---

**Feature Completada**: 2025-12-05  
**Status**: ✅ LISTO PARA USAR  
**Idiomas**: 4 (ES, EN, PT, FR)
