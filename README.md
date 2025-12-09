# 🚗 Asistente Diagnóstico Automotriz

Un asistente de IA inteligente que ayuda a diagnosticar problemas automotrices utilizando códigos OBD-II, síntomas del vehículo y consulta de base de conocimiento especializada.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3.0-orange.svg)
![Gradio](https://img.shields.io/badge/Gradio-6.0.0-blue.svg)

---

## 🌟 Características Principales

### 🤖 Agente Inteligente ReAct
- Razonamiento automático y ejecución de herramientas
- Diagnóstico paso a paso del problema
- Respuestas contextualizadas basadas en el vehículo

### 🔍 Diagnóstico Profesional
- Búsqueda de códigos OBD-II (P0420, P0300, etc.)
- Identificación de síntomas comunes
- Generación de presupuestos de reparación
- Cálculo de costos de mano de obra y piezas

### 🌐 Soporte Multilingüe
- Detección automática de idioma
- Respuestas en: 🇪🇸 Español, 🇬🇧 Inglés, 🇵🇹 Portugués, 🇫🇷 Francés
- Usuario pregunta en cualquier idioma, recibe respuesta en el mismo

### 📚 Base de Conocimiento Inteligente
- Base de datos de  documentos especializados
- Búsqueda semántica con Qdrant
- Recuperación de información relevante automática

### 📊 Monitoreo en Tiempo Real
- Trazabilidad de cada interacción
- Dashboard en Langfuse
- Métricas de rendimiento y costos

### 💻 Interfaz Web Moderna
- Diseño limpio y responsivo con Gradio
- Visualización del razonamiento del agente
- Timeline de herramientas utilizadas
- Fuentes y referencias consultadas

---

## 🚀 Inicio Rápido

### Requisitos
- Python 3.9 o superior
- Git
- Conexión a internet

### Instalación (2 minutos)

**1. Clonar el repositorio**
```bash
git clone https://github.com/AlejandroRS21/mechanic-diagnostic-assistant.git
cd mechanic-diagnostic-assistant
```

**2. Crear entorno virtual**
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**4. Configurar variables de entorno**
```bash
# Copiar archivo ejemplo
cp .env.example .env

# Editar .env y añadir tu clave de OpenRouter
# Puedes obtener una gratis en: https://openrouter.ai
```

**5. Ejecutar la aplicación**
```bash
python app.py
```

**6. Abrir en navegador**
```
http://localhost:7860
```

---

## 📖 Cómo Usar

### Ejemplo 1: Diagnosticar por Código OBD-II

**Pregunta:**
```
¿Qué significa el código de error P0420?
```

**Respuesta:**
```
El código P0420 se refiere a "Catalyst System Efficiency Below Threshold (Bank 1)".

Significado:
- El convertidor catalítico no está funcionando eficientemente
- Hay problemas en el sistema de control de emisiones
- La sensor de oxígeno aguas abajo detecta problemas

Síntomas comunes:
- Luz de "Check Engine" encendida
- Pérdida de potencia del motor
- Consumo excesivo de combustible

Costo de reparación:
- Piezas: $400 - $800 USD
- Mano de obra: 1.5 - 2.5 horas

Recomendación: Revisar el convertidor catalítico y sensor O2
```

### Ejemplo 2: Diagnosticar por Síntomas

**Pregunta:**
```
Mi coche no enciende por las mañanas, hace un ruido extraño en el motor
```

**Respuesta:**
```
Basado en los síntomas descritos, posibles causas:

1. Batería débil (80% de probabilidad)
   - Revisar voltaje de batería (debe ser 12.6V en reposo)
   - Limpiar contactos de batería

2. Alternador defectuoso (15% de probabilidad)
   - Revisar carga del alternador
   - Comprobar diodos

3. Motor de arranque débil (5% de probabilidad)
   - Revisar conexiones
   - Posible reemplazo necesario

Pasos recomendados:
1. Llevar a mecánico certificado
2. Realizar prueba de batería
3. Escanear códigos de error OBD-II
```

### Ejemplo 3: Generar Presupuesto

**Pregunta:**
```
Necesito presupuesto para cambio de aceite, filtro de aire y pastillas de freno
```

**Respuesta:**
```
Presupuesto de Reparación
━━━━━━━━━━━━━━━━━━━━━━━━━

Concepto                  Cantidad    Precio Unit.    Total
─────────────────────────────────────────────────────────
Cambio de aceite              1          $45.00      $45.00
Filtro de aire                1          $25.00      $25.00
Pastillas de freno (juego)    1          $120.00    $120.00
Mano de obra (2.5 horas)      2.5        $85/hora   $212.50
─────────────────────────────────────────────────────────
SUBTOTAL                                            $402.50
IVA (19%)                                           $76.48
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL                                              $478.98
```

---

## 🛠️ Herramientas Disponibles

El agente tiene acceso a 5 herramientas autónomas:

| Herramienta | Uso | Ejemplo |
|---|---|---|
| 🔍 **Buscar Código OBD** | Búsqueda de códigos de error | "¿Qué es P0420?" |
| 💰 **Calcular Costos** | Estimación de costos de reparación | "¿Cuánto cuesta cambiar frenos?" |
| 🔧 **Encontrar Piezas** | Búsqueda de piezas de reemplazo | "Necesito pastillas de freno" |
| 🎯 **Problemas Conocidos** | Base de problemas comunes | "Motor no enciende" |
| 📋 **Generar Presupuesto** | Crear presupuestos formalizados | "Dame un presupuesto de reparación" |

---

## 📚 Documentación

- **[README_TECHNICAL.md](docs/README_TECHNICAL.md)** - Documentación técnica completa (arquitectura, APIs, debugging)
- **[INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md)** - Guía de instalación detallada
- **[TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md)** - Documentación académica
- **[FEATURES_MULTILANGUAGE.md](docs/FEATURES_MULTILANGUAGE.md)** - Cómo funciona el soporte multilingüe
- **[PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)** - Resumen ejecutivo
- **[QDRANT_IMPLEMENTATION.md](docs/QDRANT_IMPLEMENTATION.md)** - Detalles de la base de datos vectorial
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Índice completo de documentación

---

## ⚙️ Configuración

### Variables de Entorno

Copia `.env.example` a `.env` y completa:

```bash
# API Key de OpenRouter (obtén una gratis en https://openrouter.ai)
OPENROUTER_API_KEY=tu_clave_aqui

# Modelo a usar (auto-selecciona modelos gratuitos si es "free")
OPENROUTER_MODEL=free

# Ruta local de base de datos Qdrant
QDRANT_PATH=./qdrant_db

# Monitoreo (opcional pero recomendado)
LANGFUSE_SECRET_KEY=tu_clave_aqui
LANGFUSE_PUBLIC_KEY=tu_clave_aqui
LANGFUSE_BASE_URL=https://cloud.langfuse.com

# Desarrollo
DEBUG=False
LOG_LEVEL=INFO
```

---

## 🎨 Interfaz de Usuario

### Pantalla Principal

```
┌─────────────────────────────────────────────┐
│  🚗 ASISTENTE DIAGNÓSTICO AUTOMOTRIZ        │
├─────────────────────────────────────────────┤
│                                             │
│  Escribe tu pregunta aquí...                │
│  ┌──────────────────────────────────────┐  │
│  │ ¿Qué significa el código P0420?      │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  [ENVIAR]                                   │
│                                             │
├─────────────────────────────────────────────┤
│  Respuesta:                                 │
│  El código P0420 indica un problema en     │
│  el convertidor catalítico...              │
│                                             │
│  🌐 Español | 🤖 GPT-4 Mini               │
│  📚 Fuentes: repair_guides.txt             │
│  ⏱️ Tiempo: 3.2 segundos                   │
└─────────────────────────────────────────────┘
```

### Características de la UI

- ✅ Historial de chat persistente
- ✅ Visualización del razonamiento del agente
- ✅ Timeline de herramientas ejecutadas
- ✅ Indicador de idioma detectado
- ✅ Fuentes consultadas
- ✅ Métricas de rendimiento

---

## 🔧 Solución de Problemas

### Problema: "OpenRouter API Key inválido"
**Solución:**
1. Obtener clave en https://openrouter.ai
2. Verificar que esté correcta en `.env`
3. Asegurar que tienes créditos disponibles

### Problema: "Puerto 7860 ya está en uso"
**Solución:**
```bash
# Cambiar puerto en app.py o usar:
python app.py --server_port=7861
```

### Problema: "Qdrant connection failed"
**Solución:**
```bash
# Reconstruir base de datos
python -c "from src.rag.knowledge_base import initialize_knowledge_base; initialize_knowledge_base(rebuild=True)"
```

### Más soluciones en [README_TECHNICAL.md](docs/README_TECHNICAL.md#-troubleshooting)

---

## 📊 Características Técnicas

- **LLM:** OpenRouter API (múltiples modelos con fallback)
- **Vector Store:** Qdrant (búsqueda semántica local)
- **Framework:** LangChain 0.3.0 (patrón ReAct)
- **Embeddings:** Sentence Transformers (local, sin costo)
- **Interface:** Gradio 6.0.0 (web responsiva)
- **Monitoreo:** Langfuse (trazabilidad completa)
- **Lenguajes:** Python 3.9+

---

## 🌍 Idiomas Soportados

| Idioma | Código | Ejemplo |
|---|---|---|
| 🇪🇸 Español | `es` | "¿Qué significa P0420?" |
| 🇬🇧 English | `en` | "What does P0420 mean?" |
| 🇵🇹 Português | `pt` | "O que significa P0420?" |
| 🇫🇷 Français | `fr` | "Que signifie P0420?" |

El sistema detecta automáticamente el idioma y responde en el mismo.

---

## 📈 Rendimiento

| Métrica | Valor |
|---|---|
| Detección de idioma | < 10 ms |
| Búsqueda en KB | 10-50 ms |
| Respuesta del LLM | 2-10 seg |
| **Respuesta Total** | **3-15 seg** |

---

## 🔐 Seguridad

- ✅ No se almacenan datos personales
- ✅ Variables sensibles en `.env` (no en git)
- ✅ API keys validadas antes de usar
- ✅ Queries sanitizadas
- ✅ Logs sin información sensible

---

## 🤝 Contribuir

¿Encontraste un bug o tienes sugerencias?

1. **Reportar bug:** Abrir [GitHub Issue](https://github.com/AlejandroRS21/mechanic-diagnostic-assistant/issues)
2. **Sugerir mejora:** Crear [Discussion](https://github.com/AlejandroRS21/mechanic-diagnostic-assistant/discussions)
3. **Contribuir código:** Fork → Rama feature → Pull Request

---

## 📄 Licencia

Este proyecto está bajo licencia **MIT**. Eres libre de usarlo, modificarlo y distribuirlo.

---

## 👨‍💻 Autor

**Alejandro RS21**

- GitHub: [@AlejandroRS21](https://github.com/AlejandroRS21)
- Email: alejandro.rs21@example.com

---

## 🙏 Agradecimientos

- LangChain por el excelente framework
- Qdrant por la base de datos vectorial
- OpenRouter por acceso a múltiples LLMs
- Gradio por la interfaz web intuitiva
- Langfuse por monitoreo profesional

---

## 📞 Soporte

¿Necesitas ayuda?

- 📖 **Documentación:** [docs/](docs/)
- 🐛 **Reportar bug:** [Issues](https://github.com/AlejandroRS21/mechanic-diagnostic-assistant/issues)
- 💬 **Preguntas:** [Discussions](https://github.com/AlejandroRS21/mechanic-diagnostic-assistant/discussions)
- 🔧 **Troubleshooting:** [Guía técnica](docs/README_TECHNICAL.md#-troubleshooting)

---

## 🚀 Próximas Mejoras

- [ ] Integración con escáneres OBD-II reales
- [ ] API REST para integración
- [ ] Base de datos de repuestos actualizada en tiempo real
- [ ] Video tutoriales de reparación
- [ ] Aplicación móvil
- [ ] Más idiomas (Alemán, Italiano, etc.)
- [ ] Exportación de presupuestos en PDF
- [ ] Integración con talleres

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Estado:** ✅ Producción

---

<div align="center">

**Made with ❤️ for mechanics and car enthusiasts**

[⭐ Dar estrella en GitHub](https://github.com/AlejandroRS21/mechanic-diagnostic-assistant) | [📧 Contactar](mailto:alejandro.rs21@example.com) | [📚 Documentación](docs/)

</div>
