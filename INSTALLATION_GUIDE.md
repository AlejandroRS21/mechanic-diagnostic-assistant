# 🚀 Installation & Testing Guide

## Quick Start (Step-by-Step)

### Step 1: Navigate to Project

```powershell
cd "d:\PROYECTOS\Big Data IA\Modelos de IA\Proyecto  MCP\Ayudauto Asistant\mechanic-diagnostic-assistant"
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
```

### Step 3: Activate Virtual Environment

```powershell
.\venv\Scripts\activate
```

You should see `(venv)` in your prompt.

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- LangChain 0.3.0
- Gradio 6.0.0
- ChromaDB 0.5.0
- OpenAI SDK
- LangSmith
- And all other dependencies

**Expected time**: 2-5 minutes

### Step 5: Configure API Keys

1. Copy the environment template:
```powershell
copy .env.example .env
```

2. Edit `.env` with your text editor and add your API keys:

```env
# OpenRouter API (for LLM)
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=openai/gpt-4

# OpenAI API (for embeddings)
OPENAI_API_KEY=sk-your-openai-key-here

# LangSmith Monitoring
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your-langsmith-key-here
LANGCHAIN_PROJECT=mechanic-diagnostic-assistant
```

**Where to get API keys**:
- OpenRouter: https://openrouter.ai/keys
- OpenAI: https://platform.openai.com/api-keys
- LangSmith: https://smith.langchain.com/settings

### Step 6: Test Individual Components

Before running the full application, test components:

#### Test Tools (should work without API keys)
```powershell
python src\tools_impl\diagnostic_codes.py
python src\tools_impl\cost_calculator.py
python src\tools_impl\parts_finder.py
```

Expected output: Success messages with sample data

#### Test Configuration
```powershell
python src\utils\config.py
```

Expected: Configuration summary (will warn about missing API keys if not set)

#### Test RAG Data Loading (no API keys needed for this)
```powershell
python -c "from src.rag.document_loader import load_all_knowledge_base; from src.utils.config import OBD_CODES_PATH, SYMPTOMS_PATH, REPAIR_GUIDES_PATH; docs = load_all_knowledge_base(OBD_CODES_PATH, SYMPTOMS_PATH, REPAIR_GUIDES_PATH); print(f'Loaded {len(docs)} documents')"
```

Expected: "Loaded 42 documents"

### Step 7: Initialize Knowledge Base (Requires API Keys)

⚠️ **Important**: This requires OpenAI API key for embeddings.

```powershell
python -c "from src.rag.knowledge_base import initialize_knowledge_base; kb = initialize_knowledge_base(rebuild=True); print('Knowledge base initialized')"
```

**Expected time**: 2-3 minutes on first run  
**What happens**: Creates ChromaDB vector database in `./chroma_db/`

Expected output:
```
Loading documents from knowledge base...
Loaded 23 OBD code documents
Loaded 18 symptom documents
Loaded 4 repair guide documents
Total documents loaded: 45
Splitting documents into chunks...
Created 65 chunks from 45 documents
Creating embeddings and building vector database...
(This may take a few minutes on first run...)
✅ Knowledge base built and persisted to ./chroma_db
```

### Step 8: Run the Application

```powershell
python app.py
```

Expected output:
```
✅ LangSmith tracing enabled for project: mechanic-diagnostic-assistant
   View traces at: https://smith.langchain.com/
Loading existing knowledge base...
✅ Knowledge base loaded successfully
Initializing Mechanic Diagnostic Agent...
Loaded 5 tools for agent
✅ Mechanic Agent initialized successfully
✅ Agent initialized
Launching Gradio interface...
Running on local URL:  http://127.0.0.1:7860
```

### Step 9: Test the Interface

1. Open your browser to http://localhost:7860
2. Try these test queries:

**Test 1**: "I have a Toyota Corolla 2018 with code P0420"

Expected: Agent will:
- Search for code P0420
- Consult knowledge base
- Find parts
- Calculate cost
- Offer to generate estimate

**Test 2**: "Customer says car makes squealing noise when braking"

Expected: Agent will:
- Search symptoms
- Ask follow-up questions
- Suggest diagnosis

**Test 3**: "What are common issues with Honda Civic 2020?"

Expected: Agent will query known issues database

### Step 10: Check Monitoring

1. Go to https://smith.langchain.com/
2. Login with your account
3. Find project "mechanic-diagnostic-assistant"
4. See all traces from your interactions

---

## 🧪 Running Tests

### Run All Tests
```powershell
pytest tests/ -v
```

### Run Specific Test Files
```powershell
pytest tests/test_tools.py -v
pytest tests/test_rag.py -v
pytest tests/test_agent.py -v
```

**Note**: Some tests require API keys and may be skipped. That's normal.

---

## 🔧 Troubleshooting

### ImportError: No module named 'X'
**Solution**: Make sure venv is activated and dependencies installed:
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

### "Missing required environment variables"
**Solution**: Check your `.env` file has all API keys set correctly

### ChromaDB/Embeddings errors
**Solution**: 
1. Make sure OpenAI API key is valid
2. Try rebuilding knowledge base:
```powershell
python -c "from src.rag.knowledge_base import initialize_knowledge_base; initialize_knowledge_base(rebuild=True)"
```

### Gradio not loading
**Solution**:
1. Check if port 7860 is already in use
2. Try changing port in app.py (server_port parameter)

### LangSmith not showing traces
**Solution**:
1. Verify LANGCHAIN_TRACING_V2=true in .env
2. Check LangSmith API key is valid
3. Check project name matches in dashboard

---

## ✅ Success Checklist

Before recording your demo video, verify:

- [ ] Dependencies installed (`pip list` shows langchain, gradio, chromadb)
- [ ] API keys configured in `.env`
- [ ] Knowledge base initialized (chroma_db/ directory exists)
- [ ] Application runs without errors (`python app.py`)
- [ ] Can open http://localhost:7860 in browser
- [ ] Test query works and agent responds
- [ ] Tools are executed (visible in right panel)
- [ ] LangSmith traces appear in dashboard
- [ ] All 5 tools listed in interface documentation

---

## 📹 Recording Demo Video

### Suggested Script (3-5 minutes)

**00:00 - 00:30**: Introduction
- Show PROJECT_SUMMARY.md
- Explain what the project does
- List key features (RAG, 5 tools, Gradio UI)

**00:30 - 02:00**: Demo Scenario 1 - OBD Code
- Open Gradio interface
- Enter: "I have a Toyota Corolla 2018 with code P0420"
- Show agent reasoning (right panel)
- Show tools being executed
- Show final estimate generated

**02:00 - 03:30**: Demo Scenario 2 - Symptom
- Clear conversation
- Enter: "Customer says squealing noise when braking"
- Show follow-up questions
- Answer questions
- Show diagnosis and cost calculation

**03:30 - 04:30**: Show Monitoring
- Open LangSmith dashboard
- Show recent traces
- Click into a trace to show details
- Show tool executions logged

**04:30 - 05:00**: Conclusion
- Recap features demonstrated
- Mention academic requirements met
- Thank you

---

## 🎉 You're Ready!

If all steps above work, your project is complete and ready for submission.

**Next**: 
1. ✅ Test everything works
2. 📹 Record demo video
3. 🚀 Push to GitHub
4. 📤 Submit project

Good luck! 🍀
