# 🚗 Asistente Diagnóstico Automotriz

Asistente inteligente para diagnóstico de problemas automotrices con búsqueda de códigos OBD-II y base de conocimiento.

## ✨ Características

- **Agente ReAct** - Razonamiento automático con herramientas
- **Códigos OBD-II** - Búsqueda en JSON + PDFs
- **Multilingüe** - ES, EN, PT, FR
- **Base de Conocimiento** - 538 fragmentos vectorizados
- **Interfaz Web** - Gradio con visualización del razonamiento

## 📋 Instalación

```bash
# Clonar repo
git clone <repo-url>
cd mechanic-diagnostic-assistant

# Crear venv
python -m venv venv
source venv/Scripts/activate  # Windows: .\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu API key
```

### Opción: Usar LM Studio para Embeddings

Para usar embeddings locales sin coste, sigue estos pasos:

1. **Descargar LM Studio**
   - Ir a https://lmstudio.ai
   - Instalar la aplicación

2. **Cargar modelo de embeddings**
   - Abrir LM Studio
   - Descargar: `nomic-embed-text` (recomendado, 768 dims)
   - O: `all-MiniLM-L6-v2` (más rápido, 384 dims)

3. **Configurar proyecto**
   ```bash
   # En .env, cambiar a:
   EMBEDDING_PROVIDER=lmstudio
   LMSTUDIO_BASE_URL=http://localhost:8000
   LMSTUDIO_EMBEDDING_MODEL=nomic-embed-text
   ```

4. **Reconstruir base de datos**
   ```bash
   python rebuild_with_lmstudio.py
   ```

5. **Verificar configuración**
   ```bash
   python test_lmstudio_setup.py
   ```

**Ventajas de LM Studio:**
- 🔒 100% privado - datos nunca salen del equipo
- 💰 Gratis - sin costos de API
- ⚡ Rápido - ejecución local
- 🔧 Configurable - soporta múltiples modelos

Ver [LMSTUDIO_EMBEDDINGS.md](LMSTUDIO_EMBEDDINGS.md) para documentación completa.

## 🚀 Uso

### Línea de Comandos
```bash
python app.py --mode cli
```

### Interfaz Web (Gradio)
```bash
python app.py --mode web
# Acceder a: http://localhost:7860
```

### Python API
```python
from src.agent.mechanic_agent import MechanicAgent

agent = MechanicAgent()
response = agent.chat("¿Qué significa P0258?")
print(response)
```

## 📁 Estructura

```
src/
├── agent/              # Agente ReAct
│   ├── mechanic_agent.py
│   ├── tools.py
│   └── prompts.py
├── rag/                # Base de conocimiento
│   ├── knowledge_base.py
│   ├── retriever.py
│   └── document_loader.py
├── tools_impl/         # Herramientas disponibles
│   ├── diagnostic_codes.py
│   ├── known_issues.py
│   ├── estimate_generator.py
│   └── cost_calculator.py
├── utils/              # Utilidades
├── monitoring/         # Langfuse config
└── __init__.py

data/
├── knowledge_base/
│   ├── obd_codes.json
│   ├── common_symptoms.json
│   └── pdfs/          # Documentos técnicos

tests/                 # Tests unitarios
```

## 🛠 Herramientas Disponibles

| Herramienta | Descripción |
|---|---|
| `search_diagnostic_code` | Busca códigos OBD-II (P0420, P0258, etc.) |
| `search_symptoms` | Identifica problemas por síntomas |
| `search_known_issues` | Consulta problemas conocidos |
| `get_repair_cost` | Calcula costos de reparación |
| `search_knowledge_base` | Búsqueda semántica en PDFs |

## 🔍 Búsqueda de Códigos P0XXX

### Cascada de Búsqueda (3 niveles)

1. **JSON Database** (~50ms)
   - 23 códigos predefinidos
   - Búsqueda rápida

2. **Vector Database** (3-5s)
   - Qdrant con embeddings
   - Búsqueda semántica en PDFs

3. **Direct PDF Search** (4-5s)
   - Fallback directo en archivos
   - Búsqueda por texto exacto

### Ejemplo: P0258
```python
result = search_diagnostic_code("P0258")
# Retorna:
# {
#   "found": True,
#   "code": "P0258",
#   "description": "Injection Pump Fuel Metering Control 'B' Low",
#   "source": "dtc_list.pdf",
#   "document": "dtc_list.pdf"
# }
```

## 📊 Monitoreo

El sistema registra todas las interacciones en **Langfuse**:
- Trazabilidad de llamadas al LLM
- Métricas de rendimiento
- Análisis de costos

Acceso: https://cloud.langfuse.com

## ⚙️ Configuración (.env)

```env
# API Keys
OPENROUTER_API_KEY=sk_...      # Para OpenRouter
OPENAI_API_KEY=sk_...          # Para OpenAI (opcional)
GROQ_API_KEY=gsk_...           # Para Groq (gratis)

# Langfuse Monitoring
LANGFUSE_PUBLIC_KEY=pk_...
LANGFUSE_SECRET_KEY=sk_...

# Qdrant Vector DB
QDRANT_PATH=./qdrant_db        # Local o remoto
QDRANT_COLLECTION_NAME=automotive_knowledge
```

## 🧪 Testing

```bash
# Test de herramientas
python test_tool_direct.py

# Test de búsqueda P0258
python test_p0258_fallback.py

# Test de RAG
python -m pytest tests/
```

## 📝 Notas Importantes

### Problemas Resueltos

- ✅ **Agent Format Loop** - Errores repetidos solucionados
- ✅ **Source Metadata** - Ahora muestra títulos correctos
- ✅ **P0258 Search** - Fallback a PDFs implementado

### Limitaciones Actuales

- Respuestas pueden tardar 3-5s (búsqueda vectorial)
- Vector DB necesita optimización de query
- Algunas deprecation warnings de LangChain (sin impacto)

### Mejoras Futuras

- [ ] Caché de búsquedas
- [ ] Búsqueda paralela de PDFs
- [ ] Actualizar a versiones estables de LangChain
- [ ] Soporte para conversación multi-turno
- [ ] Más códigos OBD-II en JSON

## 📖 Documentación Técnica

- **TECHNICAL_DOC.md** - Arquitectura detallada
- **TECHNICAL_DOC_PART2.md** - Implementación de RAG
- **QDRANT_FINAL_SUMMARY.md** - Vector database setup
- **P0258_SOLUTION_SUMMARY.md** - Implementación del fallback

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit con mensajes claros
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

MIT License - Ver LICENSE para detalles

## 👤 Autor

Alejandro RS - [@AlejandroRS21](https://github.com/AlejandroRS21)

---

**Última actualización:** Diciembre 2025
**Estado:** ✅ Producción
**Versión:** 1.0
