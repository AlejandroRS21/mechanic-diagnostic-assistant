# 📖 Documentación - Índice

**Asistente Diagnóstico Automotriz** - Proyecto de IA con LangChain, Qdrant y Langfuse

---

## 📚 Documentación Disponible

### 🚀 **Comenzar Aquí**

1. **[README_MAIN.md](README_MAIN.md)** - README estándar (COMIENZA AQUÍ) ⭐
   - Características principales
   - Inicio rápido en 2 minutos
   - Ejemplos de uso prácticos
   - Solución de problemas rápida
   - Información general para usuarios

2. **[README.md](docs/README.md)** - Guía de usuario principal
   - Instalación rápida
   - Uso de la interfaz
   - Estructura del proyecto
   - Requisitos y dependencias

3. **[INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md)** - Guía de instalación detallada
   - Paso a paso de configuración
   - Pruebas de componentes
   - Solución de problemas
   - Inicialización de base de datos

### 📝 **Documentación Técnica**

4. **[README_TECHNICAL.md](docs/README_TECHNICAL.md)** - README técnico completo ⭐ **PARA DESARROLLADORES**
   - Arquitectura en capas del sistema
   - Stack tecnológico detallado
   - Componentes principales
   - Flujo de conversación paso a paso
   - Setup e instalación
   - Debugging y troubleshooting
   - Métricas de rendimiento
   - Seguridad y buenas prácticas

5. **[TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md)** - Documentación académica completa
   - Arquitectura del sistema
   - Descripción de componentes
   - Flujo conversacional
   - Patrones de diseño (ReAct)
   - Integración de LangChain
   - Monitoreo y trazabilidad
   - Metricas de rendimiento

5. **[PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)** - Resumen ejecutivo del proyecto
   - Checklist de requisitos
   - Características implementadas
   - Herramientas autónomas
   - Base de conocimiento RAG
   - Estadísticas del proyecto
   - Cumplimiento académico

### ✨ **Características Especiales**

6. **[FEATURES_MULTILANGUAGE.md](docs/FEATURES_MULTILANGUAGE.md)** - Soporte multilingüe
   - Detección automática de idioma
   - Idiomas soportados (ES, EN, PT, FR)
   - Implementación técnica
   - Ejemplos de uso

7. **[QDRANT_IMPLEMENTATION.md](docs/QDRANT_IMPLEMENTATION.md)** - Base de datos vectorial
   - Migración de ChromaDB a Qdrant
   - Configuración local y remota
   - Ventajas de Qdrant
   - Almacenamiento eficiente

---

## 🎯 Guía Rápida por Rol

### 👤 **Usuario Final**
1. Lee: [README.md](docs/README.md) - sección "Installation & Quick Start"
2. Configura: `.env` con tus API keys
3. Ejecuta: `python app.py`
4. Accede: `http://localhost:7860`

### 👨‍💻 **Desarrollador**
1. Lee: [README.md](docs/README.md) - sección "Project Structure"
2. Referencia: [TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md) - arquitectura
3. Prueba: [INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) - componentes individuales
4. Explora: `src/` para ver la implementación

### 📚 **Revisor Académico**
1. Lee: [PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) - checklist completo
2. Revisa: [TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md) - toda la documentación académica
3. Valida: [FEATURES_MULTILANGUAGE.md](docs/FEATURES_MULTILANGUAGE.md) - características adicionales
4. Verifica: [QDRANT_IMPLEMENTATION.md](docs/QDRANT_IMPLEMENTATION.md) - stack tecnológico

---

## 🏗️ Estructura del Proyecto

```
mechanic-diagnostic-assistant/
├── docs/                          # 📖 Documentación
│   ├── README.md
│   ├── TECHNICAL_DOCUMENTATION.md
│   ├── PROJECT_SUMMARY.md
│   ├── INSTALLATION_GUIDE.md
│   ├── FEATURES_MULTILANGUAGE.md
│   └── QDRANT_IMPLEMENTATION.md
│
├── src/                           # 💻 Código fuente
│   ├── agent/                     # Agente ReAct
│   ├── rag/                       # Sistema RAG + Qdrant
│   ├── tools_impl/                # 5 herramientas autónomas
│   ├── monitoring/                # Langfuse integration
│   └── utils/                     # Utilidades y configuración
│
├── data/                          # 📊 Datos
│   ├── knowledge_base/            # Base de conocimiento
│   └── mock_data/                 # Datos de prueba
│
├── tests/                         # ✅ Tests
├── app.py                         # Interfaz Gradio
├── requirements.txt               # Dependencias
└── .env.example                   # Plantilla de configuración
```

---

## 🔧 Stack Tecnológico

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| **LLM** | OpenRouter (GPT-4) | Latest |
| **Agente** | LangChain ReAct | 0.3.0 |
| **Vector Store** | Qdrant | 1.7.0+ |
| **Embeddings** | HuggingFace | 2.2.0+ |
| **Interfaz** | Gradio | 6.0.0 |
| **Monitoreo** | Langfuse | 2.0.0+ |
| **Lenguaje** | Python | 3.8+ |

---

## 🌍 Idiomas Soportados

- 🇪🇸 Español (es)
- 🇬🇧 English (en)
- 🇵🇹 Português (pt)
- 🇫🇷 Français (fr)

El agente detecta automáticamente el idioma del usuario y responde en el mismo idioma.

---

## 🚀 Inicio Rápido

### Instalación (5 minutos)

```bash
# 1. Clonar o navegar al proyecto
cd mechanic-diagnostic-assistant

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar API keys
copy .env.example .env
# Editar .env y agregar tus claves
```

### Ejecución

```bash
# Iniciar la aplicación
python app.py

# Abrir en navegador
http://localhost:7860
```

---

## 📊 Características Principales

### 🤖 Agente Inteligente
- Patrón ReAct (Reasoning + Acting)
- Memoria conversacional
- Selección automática de herramientas
- 5 herramientas autónomas

### 📚 Sistema RAG
- Base vectorial Qdrant
- 42+ documentos automotrices
- Búsqueda por similitud
- Recuperación inteligente

### 🌐 Multilingüe
- Detección automática de idioma
- Respuestas en el mismo idioma
- 4 idiomas soportados

### 📡 Monitoreo
- Trazabilidad con Langfuse
- Métricas de rendimiento
- Logs detallados
- Dashboard de análisis

---

## ✅ Checklist de Verificación

- [x] Arquitectura ReAct implementada
- [x] 5 herramientas autónomas funcionales
- [x] Base de conocimiento RAG con 42+ docs
- [x] Interfaz Gradio moderna
- [x] Monitoreo con Langfuse
- [x] Soporte multilingüe (4 idiomas)
- [x] Tests unitarios incluidos
- [x] Documentación completa
- [x] Stack limpio (Qdrant + Langfuse)
- [x] Conformidad académica

---

## 🔗 Enlaces Útiles

- **GitHub**: [AlejandroRS21/mechanic-diagnostic-assistant](https://github.com/AlejandroRS21/mechanic-diagnostic-assistant)
- **Langfuse**: [cloud.langfuse.com](https://cloud.langfuse.com)
- **OpenRouter**: [openrouter.ai](https://openrouter.ai)
- **LangChain**: [langchain.com](https://langchain.com)
- **Qdrant**: [qdrant.tech](https://qdrant.tech)

---

## 📞 Soporte

Para preguntas sobre:
- **Instalación**: Ver [INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md)
- **Arquitectura**: Ver [TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md)
- **Features**: Ver documentación específica en `docs/`
- **Requisitos académicos**: Ver [PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)

---

**Última actualización**: Diciembre 5, 2025  
**Estado**: ✅ Listo para producción  
**Documentación**: 📚 Completa y organizada
