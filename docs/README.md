# 🔧 Mechanic Diagnostic Assistant

An intelligent chatbot system that assists professional automotive mechanics with vehicle diagnostics, repair recommendations, and automated estimate generation. Built with LangChain, RAG (Retrieval Augmented Generation), and autonomous agent architecture.

## 🎯 Features

- ✅ **RAG System**: ChromaDB vector database with automotive knowledge base
- ✅ **5 Autonomous Tools**: Diagnostic code search, cost calculation, parts finder, known issues query, estimate generation
- ✅ **Conversational AI**: Natural language understanding powered by GPT-4
- ✅ **Real-time Reasoning**: Visible agent decision-making process
- ✅ **Professional Estimates**: Automated generation of customer-ready repair quotes
- ✅ **Langfuse Monitoring**: Full tracing and observability
- ✅ **Modern UI**: Gradio 6 interface with responsive design

## 📋 Requirements

- Python 3.10 or higher
- OpenRouter API key (for GPT-4 access)
- OpenAI API key (for embeddings)
- Langfuse API key (for monitoring - optional)

## 🚀 Installation

### 1. Clone/Navigate to Repository

```bash
cd mechanic-diagnostic-assistant
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and add your API keys:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edit `.env` and add your API keys:

```env
OPENROUTER_API_KEY=your_openrouter_key_here
OPENAI_API_KEY=your_openai_key_here
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
```

### 5. Initialize Knowledge Base (Optional)

On first run, the system will automatically build the vector database. To rebuild manually:

```bash
python -c "from src.rag.knowledge_base import initialize_knowledge_base; initialize_knowledge_base(rebuild=True)"
```

## 🎮 Usage

### Start the Application

```bash
python app.py
```

The Gradio interface will launch at `http://localhost:7860`

### Example Interactions

**Scenario 1: OBD Code Diagnosis**
```
Mechanic: "I have a Toyota Corolla 2018 with code P0420"
Assistant: [Searches diagnostic code, consults RAG, finds parts, calculates cost, generates estimate]
```

**Scenario 2: Symptom-Based Diagnosis**
```
Mechanic: "Customer says the car makes squealing noise when braking"
Assistant: [Analyzes symptoms, asks follow-up questions, recommends solution]
```

**Scenario 3: Known Issues Query**
```
Mechanic: "What are common problems with Honda Civic 2020?"
Assistant: [Queries known issues database, provides list with frequencies and symptoms]
```

## 🏗️ Project Structure

```
mechanic-diagnostic-assistant/
├── app.py                      # Main Gradio interface
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
│
├── src/
│   ├── agent/                 # Agent implementation
│   │   ├── mechanic_agent.py # Main ReAct agent
│   │   ├── tools.py          # LangChain tools wrapper
│   │   └── prompts.py        # System prompts
│   │
│   ├── rag/                   # RAG system
│   │   ├── knowledge_base.py # ChromaDB setup
│   │   ├── document_loader.py
│   │   └── retriever.py
│   │
│   ├── tools_impl/            # Tool implementations
│   │   ├── diagnostic_codes.py
│   │   ├── cost_calculator.py
│   │   ├── parts_finder.py
│   │   ├── known_issues.py
│   │   └── estimate_generator.py
│   │
│   ├── monitoring/
│   │   └── langfuse_config.py
│   │
│   └── utils/
│       ├── config.py
│       └── helpers.py
│
└── data/
    ├── knowledge_base/        # RAG documents
    │   ├── obd_codes.json
    │   ├── common_symptoms.json
    │   └── repair_guides.txt
    │
    └── mock_data/             # Parts & labor data
        ├── parts_catalog.json
        └── labor_rates.json
```

## 🛠️ Technology Stack

- **LLM**: GPT-4 (via OpenRouter API)
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector DB**: ChromaDB 0.5.0
- **Framework**: LangChain 0.3.0
- **Interface**: Gradio 6.0.0
- **Monitoring**: Langfuse

## 📊 Monitoring

All agent interactions are traced with Langfuse. View traces at:
- https://smith.langchain.com/

Set `LANGCHAIN_TRACING_V2=true` in `.env` to enable tracing.

## 📚 Documentation

- **Technical Documentation**: See [TECHNICAL_DOC.md](TECHNICAL_DOC.md) for detailed architecture and implementation
- **Conversation Diagram**: See `assets/conversation_diagram.mmd` for Mermaid flow diagram

## 🧪 Testing

Run individual component tests:

```bash
# Test RAG system
python src/rag/knowledge_base.py

# Test tools
python src/tools_impl/diagnostic_codes.py
python src/tools_impl/cost_calculator.py

# Test agent
python src/agent/mechanic_agent.py
```

## 🔒 Security & Privacy

- All API keys are stored in `.env` (not committed to git)
- No customer data is persisted
- All traces are private to your Langfuse account

## 📝 License

This is an academic project for educational purposes.

## 🤝 Contributing

This is an academic project. For questions or suggestions, please open an issue.

## 📧 Contact

Academic Project - NLP & Autonomous Agents Course

---

**Built with ❤️ using LangChain, ChromaDB, and Gradio**
