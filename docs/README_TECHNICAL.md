# 🔧 README Técnico - Asistente Diagnóstico Automotriz

## Descripción General

**Mechanic Diagnostic Assistant** es una aplicación de IA avanzada que utiliza patrones ReAct (Reasoning + Acting) con LangChain para proporcionar diagnósticos automotrices inteligentes. La aplicación integra:

- 🤖 **Agente ReAct**: Razonamiento y ejecución de herramientas autónomas
- 🔍 **RAG (Retrieval-Augmented Generation)**: Base de conocimiento vectorial con Qdrant
- 📊 **Monitoreo en Tiempo Real**: Trazabilidad completa con Langfuse
- 🌐 **Soporte Multilingüe**: Detección automática de idiomas (ES, EN, PT, FR)
- 🎯 **Interfaz Gradio**: UI web intuitiva y responsiva

---

## 🏗️ Arquitectura del Sistema

### Capas de la Aplicación

```
┌─────────────────────────────────────────────┐
│         Capa de Presentación                │
│     (Gradio Web Interface - 6.0.0)          │
│  ├─ Chat UI con historial                   │
│  ├─ Visualización de razonamiento           │
│  ├─ Timeline de herramientas                │
│  └─ Detección de idioma en UI               │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│       Capa de Orquestación                  │
│   (LangChain 0.3.0 + ReAct Agent)           │
│  ├─ AgentExecutor                           │
│  ├─ create_react_agent                      │
│  ├─ ConversationBufferMemory                │
│  └─ Tool invocation & routing               │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      Capa de Herramientas Autónomas         │
│              (5 Tools)                      │
│  ├─ search_diagnostic_code                  │
│  ├─ calculate_repair_cost                   │
│  ├─ find_replacement_parts                  │
│  ├─ query_known_issues                      │
│  └─ generate_estimate                       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│     Capa de Procesamiento (RAG)             │
│  ├─ Knowledge Retriever (Qdrant)            │
│  ├─ Document Loader                         │
│  ├─ Embeddings (HuggingFace)                │
│  └─ Language Detection & Instructions       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      Capa de Persistencia                   │
│  ├─ Qdrant Vector Store (Local)             │
│  ├─ Knowledge Base JSON Files               │
│  ├─ Langfuse Cloud Monitoring               │
│  └─ .env Configuration                      │
└─────────────────────────────────────────────┘
```

---

## 🔌 Componentes Principales

### 1. **Agente ReAct** (`src/agent/mechanic_agent.py`)

**Patrón:** Reasoning + Acting

```python
Agent Loop:
1. THINK    → Analiza input + contexto
2. ACT      → Selecciona herramienta más apropiada
3. OBSERVE  → Obtiene resultado de la herramienta
4. REPEAT   → Hasta resolver la consulta
```

**Características Clave:**
- Usa ChatOpenAI vía OpenRouter API
- Integración automática de contexto de KB
- Detección de idioma del usuario
- Memory persistente con ConversationBufferMemory
- Fallback automático de modelos

**Método Principal:**
```python
def chat(self, message: str) -> Dict[str, Any]:
    """
    Process user message through ReAct agent.
    
    Returns:
        - response: Respuesta en idioma del usuario
        - reasoning: Cadena de razonamiento del agente
        - tools_used: Herramientas invocadas
        - sources: Fuentes de KB consultadas
    """
```

### 2. **Herramientas Autónomas** (`src/tools_impl/`)

| Herramienta | Propósito | Entrada | Salida |
|---|---|---|---|
| `search_diagnostic_code` | Busca códigos OBD-II | Código (P0420) | Descripción + síntomas |
| `calculate_repair_cost` | Calcula costo de reparación | Tipo reparación | Rango de costo |
| `find_replacement_parts` | Busca piezas de reemplazo | Descripción parte | Catálogo de partes |
| `query_known_issues` | Consulta problemas conocidos | Síntomas del vehículo | Problemas similares |
| `generate_estimate` | Genera presupuesto | Reparaciones + partes | Presupuesto formateado |

**Implementación Base:**
```python
from langchain.tools import Tool

tool = Tool(
    name="tool_name",
    func=implementation_function,
    description="Descripción clara del propósito"
)
```

### 3. **Sistema RAG** (`src/rag/`)

#### Base de Conocimiento
- **42+ documentos**: OBD codes, repair guides, parts catalog, labor rates
- **Formatos**: JSON, TXT, PDFs
- **Ubicación**: `data/knowledge_base/`

#### Retriever
```python
retriever = KnowledgeRetriever(top_k=5)
results = retriever.retrieve(query)
# Returns: [(content, metadata, score), ...]
```

#### Embeddings
- **Modelo**: Sentence Transformers (HuggingFace)
- **Dimensión**: 384 dimensiones
- **Ventaja**: Local, sin costos API, rápido

### 4. **Qdrant Vector Store** (`qdrant_db/`)

**Características:**
- Base de datos vectorial local
- Almacenamiento persistente en disco
- Búsqueda semántica en O(log n)
- Metadata filtering integrado
- Escalable a millones de vectores

**Configuración:**
```python
from qdrant_client import QdrantClient

client = QdrantClient(":memory:")  # Local
# o
client = QdrantClient(path="./qdrant_db")  # Persistente
```

### 5. **Detección de Idiomas** (`src/utils/language_detector.py`)

**Idiomas Soportados:**
- 🇪🇸 Spanish (es)
- 🇬🇧 English (en)
- 🇵🇹 Portuguese (pt)
- 🇫🇷 French (fr)

**Método de Detección:**
```python
# Pattern-based detection con regex
PATTERNS = {
    'es': ['hola', 'tengo', 'qué', 'á', 'é', 'ñ'],
    'en': ['hello', 'the', 'what'],
    'pt': ['olá', 'tenho', 'ã', 'õ'],
    'fr': ['bonjour', 'quoi', 'ç']
}

# Scoring ponderado
score = sum(weight for pattern in detected_patterns)
language = patterns_with_highest_score
```

**Integración:**
1. Usuario envía mensaje en cualquier idioma
2. Sistema detecta idioma automáticamente
3. Inyecta instrucción en prompt del LLM
4. Agente responde en idioma detectado
5. UI muestra idioma detectado (🌐 icon)

### 6. **Langfuse Monitoring** (`src/monitoring/langfuse_config.py`)

**Métricas Capturadas:**
- 📝 LLM calls (input, output, tokens, latencia)
- 🔧 Tool executions (herramienta, parámetros, resultado)
- ⏱️ Timing (latencia por componente)
- 💰 Costos (modelo, tokens, precio)
- 🎯 User sessions (historial conversacional)

**Configuración:**
```python
from langfuse.callback import CallbackHandler

handler = CallbackHandler(
    secret_key=LANGFUSE_SECRET_KEY,
    public_key=LANGFUSE_PUBLIC_KEY,
    base_url=LANGFUSE_BASE_URL
)
```

**Dashboard Accesible en:** https://cloud.langfuse.com

---

## 📦 Stack Tecnológico

### Dependencias Principales

```
Core Framework:
├── langchain==0.3.0                    # Orchestration & agents
├── langchain-openai==0.2.0             # OpenAI integration
├── langchain-community==0.3.0          # Community integrations
└── qdrant-client>=1.7.0                # Vector database

AI/ML:
├── sentence-transformers>=2.2.0        # Local embeddings
├── openai>=1.12.0                      # OpenAI API
├── pydantic>=2.11.10                   # Data validation
└── pandas>=2.0.0                       # Data processing

Interface:
├── gradio==6.0.0                       # Web UI
└── requests>=2.31.0                    # HTTP client

Monitoring:
├── langfuse>=2.0.0                     # Production tracing

Utilities:
├── python-dotenv==1.0.0                # Environment config
├── pytest>=7.4.0                       # Testing framework
└── (More in requirements.txt)
```

### Versiones Probadas
- Python: 3.9 - 3.12
- LangChain: 0.3.0 (estable)
- Qdrant: 1.7.0+
- Gradio: 6.0.0

---

## 🔑 Configuración & Credenciales

### Variables de Entorno (.env)

```bash
# LLM API
OPENROUTER_API_KEY=xxx          # Clave de OpenRouter
OPENROUTER_MODEL=free           # Modelo a usar (auto-fallback)

# Vector Database
QDRANT_PATH=./qdrant_db         # Path local de Qdrant
QDRANT_HOST=localhost           # Host si es remoto
QDRANT_PORT=6333                # Puerto por defecto

# Monitoring & Tracing
LANGFUSE_SECRET_KEY=xxx         # Secreto de Langfuse
LANGFUSE_PUBLIC_KEY=xxx         # Clave pública
LANGFUSE_BASE_URL=https://cloud.langfuse.com

# Development
DEBUG=True                       # Modo debug
LOG_LEVEL=INFO                   # Nivel de logging
```

### Archivo `.env.example`
```bash
OPENROUTER_API_KEY=
OPENROUTER_MODEL=free
QDRANT_PATH=./qdrant_db
LANGFUSE_SECRET_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_BASE_URL=https://cloud.langfuse.com
DEBUG=False
LOG_LEVEL=INFO
```

---

## 🚀 Instalación & Setup

### Requisitos Previos
- Python 3.9+
- Git
- 500MB espacio en disco (Qdrant DB + embeddings cache)
- Conexión a internet (para OpenRouter API)

### Instalación Paso a Paso

**1. Clonar Repositorio**
```bash
git clone https://github.com/AlejandroRS21/mechanic-diagnostic-assistant.git
cd mechanic-diagnostic-assistant
```

**2. Crear Virtual Environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

**4. Configurar Variables de Entorno**
```bash
# Copiar archivo ejemplo
cp .env.example .env

# Editar .env con tus credenciales
# - OPENROUTER_API_KEY
# - LANGFUSE_SECRET_KEY / PUBLIC_KEY (opcional)
```

**5. Inicializar Base de Conocimiento**
```bash
python -c "from src.rag.knowledge_base import initialize_knowledge_base; initialize_knowledge_base(rebuild=True)"
```

**6. Ejecutar Aplicación**
```bash
python app.py
```

**7. Acceder a Interfaz**
- Abrir: http://localhost:7860
- O esperar a que se abra automáticamente en navegador

---

## 📁 Estructura de Directorios

```
mechanic-diagnostic-assistant/
│
├── app.py                          # Punto de entrada principal (Gradio)
├── requirements.txt                # Dependencias Python
├── DOCUMENTATION.md                # Índice de documentación
│
├── src/
│   ├── agent/
│   │   ├── mechanic_agent.py       # Agente ReAct principal
│   │   ├── prompts.py              # System prompts y templates
│   │   └── tools.py                # Registro de herramientas
│   │
│   ├── tools_impl/
│   │   ├── cost_calculator.py      # Cálculo de costos
│   │   ├── diagnostic_codes.py     # Búsqueda de códigos OBD
│   │   ├── estimate_generator.py   # Generación de presupuestos
│   │   ├── known_issues.py         # Base de problemas conocidos
│   │   └── parts_finder.py         # Búsqueda de piezas
│   │
│   ├── rag/
│   │   ├── knowledge_base.py       # Inicialización KB + Qdrant
│   │   ├── document_loader.py      # Cargador de documentos
│   │   └── retriever.py            # Retrieval logic
│   │
│   ├── monitoring/
│   │   └── langfuse_config.py      # Setup Langfuse
│   │
│   └── utils/
│       ├── config.py               # Config centralizada
│       ├── helpers.py              # Funciones auxiliares
│       ├── language_detector.py    # Detección de idiomas
│       ├── model_manager.py        # Gestión de modelos
│       └── __init__.py
│
├── data/
│   ├── knowledge_base/
│   │   ├── common_symptoms.json    # Síntomas comunes
│   │   ├── obd_codes.json          # Códigos OBD-II
│   │   ├── repair_guides.txt       # Guías de reparación
│   │   ├── pdfs/                   # Documentos PDF
│   │   └── mock_data/              # Datos de prueba
│   │
│   └── mock_data/
│       ├── labor_rates.json        # Tarifas de mano de obra
│       └── parts_catalog.json      # Catálogo de piezas
│
├── qdrant_db/                      # Base de datos vectorial Qdrant
│   ├── meta.json
│   ├── collections/
│   └── snapshots/
│
├── docs/                           # Documentación
│   ├── README.md                   # Guía de usuario
│   ├── INSTALLATION_GUIDE.md       # Instalación detallada
│   ├── TECHNICAL_DOCUMENTATION.md  # Documentación académica
│   ├── PROJECT_SUMMARY.md          # Resumen ejecutivo
│   ├── FEATURES_MULTILANGUAGE.md   # Feature multilingüe
│   └── QDRANT_IMPLEMENTATION.md    # Implementación Qdrant
│
├── tests/                          # Suite de tests
│   ├── test_agent.py
│   ├── test_rag.py
│   └── test_tools.py
│
├── .env                            # Variables de entorno (NO COMMITAR)
├── .env.example                    # Ejemplo de .env
├── .gitignore                      # Git ignore rules
└── README.md                       # (Root README)
```

---

## 🔄 Flujo de Conversación

```
┌─ Usuario envía mensaje
│
├─ 1. DETECCIÓN DE IDIOMA
│  └─ LanguageDetector.detect_language(message)
│     → Retorna: 'es', 'en', 'pt', o 'fr'
│
├─ 2. RECUPERACIÓN DE CONTEXTO
│  └─ KnowledgeRetriever.retrieve(message)
│     → Busca 5 documentos más relevantes en Qdrant
│     → Retorna: [(content, metadata, score), ...]
│
├─ 3. PREPARACIÓN DE PROMPT
│  ├─ System Prompt (instrucciones del agente)
│  ├─ Contexto de KB (documentos recuperados)
│  ├─ Instrucción de idioma (de LanguageInstructions)
│  └─ Mensaje del usuario
│     → Prompt combinado enviado al LLM
│
├─ 4. RAZONAMIENTO DEL AGENTE (ReAct Loop)
│  ├─ THINK: Analiza prompt + contexto
│  ├─ PLAN: Decide qué herramienta usar
│  ├─ ACT: Ejecuta herramienta (con parámetros)
│  └─ OBSERVE: Recibe resultado de herramienta
│     → Continúa hasta tener respuesta completa
│
├─ 5. GENERACIÓN DE RESPUESTA
│  └─ LLM genera respuesta en idioma detectado
│
├─ 6. MONITOREO Y TRAZABILIDAD
│  ├─ Langfuse registra:
│  │  ├─ Input/Output del LLM
│  │  ├─ Herramientas invocadas
│  │  ├─ Latencias
│  │  └─ Costos
│  └─ Dashboard en cloud.langfuse.com
│
└─ 7. PRESENTACIÓN EN UI
   ├─ Respuesta en chat
   ├─ Razonamiento desplegable
   ├─ Timeline de herramientas
   ├─ Idioma detectado (🌐)
   └─ Fuentes consultadas
```

---

## 🛠️ APIs Utilizadas

### 1. **OpenRouter API**
**Descripción:** Acceso a múltiples modelos LLM con fallback automático

```python
# Modelos disponibles
free_models = [
    "google/gemini-2.0-flash-exp",
    "meta-llama/llama-2-7b-chat",
    "mistralai/mistral-7b-instruct"
]
```

**Endpoint:** `https://openrouter.ai/api/v1/chat/completions`

**Autenticación:** `Authorization: Bearer $OPENROUTER_API_KEY`

### 2. **Qdrant API**
**Descripción:** Vector database para búsqueda semántica

```python
# Operaciones básicas
client.search(collection_name, query_vector, limit=5)
client.upsert(collection_name, points)
client.delete(collection_name, ids)
```

### 3. **Langfuse API**
**Descripción:** Monitoreo y trazabilidad en tiempo real

```python
# Capture automático de:
# - LLM calls
# - Tool executions
# - User sessions
# - Performance metrics
```

---

## 📊 Rendimiento & Optimizaciones

### Latencia Esperada

| Operación | Latencia Típica |
|---|---|
| Detección idioma | 1-5 ms |
| Búsqueda Qdrant (top-5) | 10-50 ms |
| Embedding de documento | 50-100 ms |
| LLM inference (OpenRouter) | 2-10 segundos |
| **Respuesta Total** | **3-15 segundos** |

### Optimizaciones Implementadas

1. **Embeddings Locales**: Usa Sentence Transformers (sin latency de API)
2. **Caching**: Resultados de Qdrant cacheados en memoria
3. **Fallback de Modelos**: Auto-switchear si modelo falla
4. **Batch Processing**: Procesa múltiples documentos en paralelo
5. **Lazy Loading**: Componentes cargados bajo demanda

---

## 🧪 Testing

### Ejecución de Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Tests específicos
pytest tests/test_agent.py -v
pytest tests/test_rag.py -v
pytest tests/test_tools.py -v

# Con cobertura
pytest tests/ --cov=src --cov-report=html
```

### Pruebas Manuales Recomendadas

```python
# 1. Prueba de detección de idioma
message_es = "¿Qué significa el código P0420?"
message_en = "What does the P0420 code mean?"
message_pt = "O que significa o código P0420?"
message_fr = "Que signifie le code P0420?"

# 2. Prueba de herramientas
agent.tools_available()  # Listar herramientas
agent.chat("busca el código P0420")

# 3. Prueba de RAG
retriever.retrieve("motor no enciende")

# 4. Prueba de Langfuse
# Verificar en: https://cloud.langfuse.com
```

---

## 🐛 Debugging

### Niveles de Logging

```bash
# DEBUG (máximo detalle)
LOG_LEVEL=DEBUG python app.py

# INFO (información general)
LOG_LEVEL=INFO python app.py

# WARNING (solo advertencias)
LOG_LEVEL=WARNING python app.py

# ERROR (solo errores)
LOG_LEVEL=ERROR python app.py
```

### Archivos de Log
```
logs/
├── app.log              # Log general de app
├── agent.log            # Log del agente
├── rag.log              # Log del sistema RAG
└── errors.log           # Log de errores
```

### Comandos de Debugging Útiles

```python
# Verificar Qdrant connection
from src.rag.knowledge_base import initialize_knowledge_base
kb = initialize_knowledge_base()
print(kb.db.get_collections())

# Verificar LLM configuration
from src.utils.model_manager import ModelManager
mm = ModelManager()
print(mm.available_models)

# Verificar language detection
from src.utils.language_detector import LanguageDetector
print(LanguageDetector.detect_language("¿Hola cómo estás?"))

# Ver config actual
from src.utils.config import get_config_summary
print(get_config_summary())
```

---

## 🚨 Troubleshooting

### Error: "No available models found from OpenRouter"
**Causa:** OPENROUTER_API_KEY inválido o sin créditos
**Solución:**
1. Verificar OPENROUTER_API_KEY en .env
2. Crear cuenta en https://openrouter.ai
3. Añadir créditos a la cuenta

### Error: "Qdrant connection failed"
**Causa:** Qdrant DB no accesible
**Solución:**
```bash
# Reconstruir Qdrant
python -c "from src.rag.knowledge_base import initialize_knowledge_base; initialize_knowledge_base(rebuild=True)"

# O eliminar y recrear
rm -rf qdrant_db/
python -c "from src.rag.knowledge_base import initialize_knowledge_base; initialize_knowledge_base()"
```

### Error: "No embeddings model found"
**Causa:** Sentence Transformers no descargado
**Solución:**
```bash
pip install sentence-transformers
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Error: "Gradio port already in use"
**Causa:** Puerto 7860 ya ocupado
**Solución:**
```bash
# Cambiar puerto en app.py
app.launch(server_name="0.0.0.0", server_port=7861)
```

---

## 📈 Métricas de Rendimiento

### Monitoreo en Langfuse

Dashboard muestra:
- 📊 **Latencia**: P50, P95, P99 de respuestas
- 💰 **Costos**: Token usage, costo por modelo
- 🔧 **Tool Usage**: Herramientas más usadas
- 👥 **User Sessions**: Número de usuarios, sesiones
- 🎯 **Success Rate**: Porcentaje de consultas exitosas

---

## 🔐 Seguridad

### Buenas Prácticas

1. **Nunca commitar .env**
   ```bash
   # .gitignore
   .env
   .env.local
   ```

2. **Usar variables de entorno**
   ```python
   from dotenv import load_dotenv
   import os
   key = os.getenv('OPENROUTER_API_KEY')
   ```

3. **Validar inputs del usuario**
   ```python
   from pydantic import BaseModel, validator
   
   class DiagnosticRequest(BaseModel):
       message: str
       
       @validator('message')
       def message_not_empty(cls, v):
           if not v.strip():
               raise ValueError('Message cannot be empty')
           return v
   ```

4. **Rate Limiting** (para producción)
   ```python
   from functools import wraps
   from time import time
   
   def rate_limit(calls_per_minute=60):
       def decorator(func):
           # Implementar rate limiting
           pass
       return decorator
   ```

---

## 📚 Referencias & Recursos

### Documentación Oficial
- [LangChain Docs](https://python.langchain.com/)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- [Gradio Docs](https://www.gradio.app/docs)
- [Langfuse Docs](https://langfuse.com/docs)
- [OpenRouter API](https://openrouter.ai/docs)

### Papers Relacionados
- ReAct: [Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- RAG: [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- LangChain: [LangChain: Building applications with LLMs](https://arxiv.org/abs/2310.04861)

### Comunidades
- LangChain Discord: https://discord.gg/langchain
- Qdrant Community: https://qdrant.tech/community/
- OpenRouter Community: https://discord.gg/openrouter

---

## 👥 Contribuir

### Cómo Reportar Bugs
1. Verificar que el bug no exista en Issues
2. Crear nuevo Issue con:
   - Título descriptivo
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Logs y stack trace
   - Entorno (SO, Python version, etc.)

### Cómo Contribuir Código
1. Fork el repositorio
2. Crear rama feature: `git checkout -b feature/new-feature`
3. Commit cambios: `git commit -am 'Add new feature'`
4. Push a rama: `git push origin feature/new-feature`
5. Crear Pull Request con descripción detallada

---

## 📄 Licencia

Este proyecto está bajo licencia **MIT**. Ver `LICENSE` para más detalles.

---

## 📞 Soporte

**Contacto:** alejandro.rs21@example.com
**Issues:** https://github.com/AlejandroRS21/mechanic-diagnostic-assistant/issues
**Discussions:** https://github.com/AlejandroRS21/mechanic-diagnostic-assistant/discussions

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0.0
**Estado:** Producción ✅
