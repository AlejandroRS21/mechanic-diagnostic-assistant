"""
Gradio 6 Interface - Mechanic Diagnostic Assistant
Optimized UX for 2 main use cases:
1. Diagnosis with OBD-II code
2. Diagnosis from symptoms
"""

import gradio as gr
import json
from typing import List, Dict
from datetime import datetime

from src.agent.mechanic_agent import create_agent
from src.monitoring.langfuse_config import setup_langfuse
from src.utils.helpers import get_logger

# Initialize Langfuse monitoring
langfuse_config = setup_langfuse()

logger = get_logger(__name__)

# Global agent instance
agent = None
# Global agent instance
agent = None


def initialize_agent():
    """Initialize the agent with auto-free model selection."""
    global agent
    
    if agent is None:
        logger.info("Initializing agent with Auto-Free Model Manager...")
        agent = create_agent(verbose=False)
        logger.info("✅ Agent ready!")
    
    return agent




def chat_with_agent(message: str, history: List[Dict]) -> tuple:
    """Process message and return response with metadata."""
    if not message.strip():
        return history, "", "---", "{}"
    
    current_agent = initialize_agent()
    
    # Add user message
    history.append({"role": "user", "content": message})
    
    # Get agent response
    result = current_agent.chat(message)
    response = result.get("response", "Error processing request")
    steps = result.get("steps", [])
    
    # Add assistant response
    history.append({"role": "assistant", "content": response})
    
    # Format steps for display
    # Format steps for display
    steps_md = format_steps_timeline(steps)
    
    # Add sources to steps display if available
    sources = result.get("sources", [])
    if sources:
        steps_md += format_sources(sources)
        
    steps_json = json.dumps(steps, indent=2) if steps else "{}"
    
    # Get current model name
    model_name = current_agent.current_model_name if hasattr(current_agent, 'current_model_name') else "Unknown"
    status_msg = f"ℹ️ Modelo actual: {model_name}"
    
    return history, "", steps_md, steps_json, status_msg


def format_steps_timeline(steps: List[Dict]) -> str:
    """Format agent steps as a visual timeline."""
    if not steps:
        return "### 🤖 Modo: Conversación Directa\n\nNo se ejecutaron herramientas específicas."
    
    timeline = f"### 🔧 Herramientas Ejecutadas: {len(steps)}\n\n"
    
    for i, step in enumerate(steps, 1):
        tool_name = step.get('tool', 'Unknown')
        tool_icons = {
            "search_diagnostic_code": "🔍",
            "calculate_repair_cost": "💰",
            "find_replacement_parts": "🔧",
            "query_known_issues": "📋",
            "generate_estimate": "📄"
        }
        icon = tool_icons.get(tool_name, "⚙️")
        
        timeline += f"""
**{i}. {icon} {tool_name}**

📥 **Input:**  
```
{str(step.get('tool_input', ''))[:150]}...
```

📤 **Output:**  
```
{str(step.get('observation', ''))[:200]}...
```

---
"""
    
    return timeline


def format_sources(sources: List[Dict]) -> str:
    """Format sources as a Markdown list."""
    if not sources:
        return ""
        
    md = "\n### 📚 Fuentes Consultadas\n\n"
    
    for i, source in enumerate(sources, 1):
        title = source.get('title', 'Documento Desconocido')
        src_type = source.get('type', 'general')
        page = source.get('page')
        
        page_info = f" (Pág. {page})" if page else ""
        icon = "📄" if src_type == "manual" else "🔍"
        
        md += f"{i}. {icon} **{title}**{page_info}\n"
        
    md += "\n---\n"
    return md


def reset_chat():
    """Reset conversation."""
    global agent
    if agent:
        agent.reset_conversation()
    if agent:
        agent.reset_conversation()
    return [], "", "### 💭 Listo para nueva consulta", "{}", "ℹ️ Listo"


# Enhanced CSS
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', system-ui, sans-serif !important;
}

.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 1.5rem;
}

.use-case-card {
    background: #f8f9fa;
    border-left: 4px solid #667eea;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
}

.stats-box {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
}

.timeline-step {
    border-left: 3px solid #667eea;
    padding-left: 1rem;
    margin: 1rem 0;
}
"""

# Build interface
with gr.Blocks(title="🔧 Asistente de Diagnóstico Automotriz") as demo:
    
    # Add CSS
    gr.HTML(f"<style>{custom_css}</style>")
    
    # Hero Header
    gr.HTML("""
    <div class="hero-section">
        <h1 style="margin: 0; font-size: 2.5rem;">🔧 Asistente Diagnóstico Automotriz</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            IA con RAG + 5 Herramientas Autónomas
        </p>
    </div>
    """)
    
    # Main Layout
    with gr.Row():
        # LEFT PANEL - Chat (60%)
        with gr.Column(scale=3):
            gr.Markdown("## 💬 Conversación")
            
            chatbot = gr.Chatbot(
                label="Chat",
                height=450
            )
            
            with gr.Row():
                msg_input = gr.Textbox(
                    label="Tu Mensaje",
                    placeholder="Ej: 'Tengo un Toyota Corolla 2018 con código P0420' o 'El auto hace ruido al frenar'",
                    lines=2,
                    scale=4
                )
                send_btn = gr.Button("Enviar 🚀", variant="primary", scale=1, size="lg")
            
            with gr.Row():
                clear_btn = gr.Button("🗑️ Nueva Consulta", variant="secondary")
                
        # RIGHT PANEL - Tools & Info (40%)
        with gr.Column(scale=2):
            # Model Selector
            gr.Markdown("## 🤖 Configuración")
            
            gr.Markdown("""
            **Modo: Selección Automática de Modelos Gratuitos**
            
            El sistema buscará automáticamente modelos gratuitos en OpenRouter.
            Si un modelo falla (error o límite de cuota), cambiará automáticamente al siguiente disponible.
            """)
            
            model_status = gr.Markdown("ℹ️ Estado: Buscando mejor modelo gratuito...")
            
            gr.Markdown("---")
            gr.Markdown("## 🔍 Proceso del Agente")
            
            steps_display = gr.Markdown(
                value="### 💭 Esperando consulta...",
                elem_classes=["timeline-step"]
            )
            
            with gr.Accordion("📊 Detalles Técnicos (JSON)", open=False):
                steps_json = gr.Code(
                    label="Ejecución de Herramientas",
                    language="json",
                    value="{}"
                )
            
            gr.Markdown("---")
            
            # Info boxes
            gr.HTML("""
            <div class="use-case-card">
                <h3>📋 Caso 1: Con Código OBD-II</h3>
                <ol style="margin: 0.5rem 0; padding-left: 1.5rem;">
                    <li>Introduce código (ej: P0420)</li>
                    <li>🔍 Busca en base de datos</li>
                    <li>🧠 Consulta RAG</li>
                    <li>💰 Calcula presupuesto</li>
                </ol>
            </div>
            
            <div class="use-case-card">
                <h3>🩺 Caso 2: Por Síntomas</h3>
                <ol style="margin: 0.5rem 0; padding-left: 1.5rem;">
                    <li>Describe el problema</li>
                    <li>🧠 RAG encuentra causas</li>
                    <li>❓ Preguntas de seguimiento</li>
                    <li>✅ Diagnóstico final</li>
                </ol>
            </div>
            """)
            
            with gr.Accordion("ℹ️ Sobre este Asistente", open=False):
                gr.Markdown("""
                **Tecnologías:**
                - 🧠 **LLM**: GPT-4 (OpenRouter)
                - 📚 **RAG**: ChromaDB + HuggingFace Embeddings
                - 🔧 **Herramientas**: 5 funciones autónomas
                - 📊 **Monitoreo**: Langfuse
                
                **Base de Conocimiento:**
                - 23 códigos OBD-II
                - 18 patrones de síntomas
                - 4 guías de reparación
                - 33 repuestos con precios
                """)
    
    # Quick Examples
    with gr.Accordion("💡 Ejemplos Rápidos", open=False):
        gr.Examples(
            examples=[
                ["Tengo un Toyota Corolla 2018 con código P0420"],
                ["El auto hace un ruido chirriante al frenar"],
                ["Check engine encendido, ralentí irregular, Toyota Camry 2019"],
                ["¿Cuáles son los problemas comunes del Honda Civic 2020?"],
                ["Necesito presupuesto para cambio de pastillas de freno en Nissan Sentra 2017"],
            ],
            inputs=msg_input,
            label="Haz clic en un ejemplo para probarlo"
        )
    
    # Footer
    gr.HTML("""
    <div style="text-align: center; color: #6c757d; margin-top: 2rem; padding: 1rem; border-top: 1px solid #dee2e6;">
        <p><strong>🎓 Proyecto Académico</strong> - NLP & Agentes Autónomos</p>
        <p style="font-size: 0.9rem;">LangChain • ChromaDB • Gradio 6 • Langfuse</p>
    </div>
    """)
    
    # Event Handlers
    send_btn.click(
        fn=chat_with_agent,
        inputs=[msg_input, chatbot],
        outputs=[chatbot, msg_input, steps_display, steps_json, model_status]
    )
    
    msg_input.submit(
        fn=chat_with_agent,
        inputs=[msg_input, chatbot],
        outputs=[chatbot, msg_input, steps_display, steps_json, model_status]
    )
    
    clear_btn.click(
        fn=reset_chat,
        outputs=[chatbot, msg_input, steps_display, steps_json, model_status]
    )
    


if __name__ == "__main__":
    logger.info("🚀 Iniciando Asistente de Diagnóstico Automotriz...")
    logger.info("📥 Inicializando agente (primera vez puede tardar ~5 min)...")
    
    # Pre-initialize
    initialize_agent()
    
    logger.info("✅ Agente inicializado")
    logger.info("🌐 Lanzando interfaz Gradio...")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        favicon_path=None
    )
