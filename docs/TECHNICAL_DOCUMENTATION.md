# Technical Documentation
# Mechanic Diagnostic Assistant

**Academic Project - NLP & Autonomous Agents**

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Use of Natural Language Processing](#2-use-of-natural-language-processing)
3. [Conversational Flow Diagram](#3-conversational-flow-diagram)
4. [Technical Architecture](#4-technical-architecture)
5. [Implementation with LangChain](#5-implementation-with-langchain)
6. [Monitoring & Metrics](#6-monitoring--metrics)
7. [Use Cases & Examples](#7-use-cases--examples)
8. [Conclusions & Future Work](#8-conclusions--future-work)

---

## 1. Introduction

### 1.1 Project Description

The Mechanic Diagnostic Assistant is an intelligent conversational AI system designed to help professional automotive mechanics diagnose vehicle problems efficiently and generate accurate repair estimates. The system combines:

- **RAG (Retrieval Augmented Generation)** for accessing technical automotive knowledge
- **Autonomous Agent Architecture** with 5 specialized tools
- **Natural Language Processing** for understanding mechanic inputs and customer symptom descriptions
- **GPT-4** for reasoning and decision-making

### 1.2 Problem Statement

Automotive mechanics face several challenges:

1. **Information Overload**: Thousands of diagnostic codes, symptoms, and repair procedures to remember
2. **Time Pressure**: Customers expect quick, accurate diagnostics
3. **Cost Estimation**: Manually calculating parts and labor costs is time-consuming and error-prone
4. **Knowledge Accessibility**: Technical service bulletins and repair guides are scattered across multiple sources

### 1.3 Solution

Our system acts as an intelligent assistant that:

- Instantly retrieves diagnostic code information from a knowledge base
- Analyzes symptoms in natural language to suggest probable causes
- Autonomously searches for compatible parts and calculates repair costs
- Generates professional customer estimates in seconds
- Learns from a curated knowledge base of automotive technical information

### 1.4 Target Users

- **Primary**: Professional automotive mechanics in independent repair shops
- **Secondary**: Automotive technicians in dealership service departments
- **Tertiary**: Automotive students and trainees

### 1.5 Business Value

- **Reduces diagnostic time** by 40-60% through instant code lookups and symptom analysis
- **Improves accuracy** by consulting comprehensive knowledge bases
- **Increases customer satisfaction** with faster turnaround and professional estimates
- **Reduces errors** in cost calculations and part selection
- **Training aid** for junior mechanics

---

## 2. Use of Natural Language Processing

### 2.1 NLP Tasks Performed

The system performs several critical NLP tasks:

#### 2.1.1 Natural Language Understanding (NLU)

**Task**: Interpret mechanic's natural language descriptions of problems

**Example Input**:
```
"Customer says the car makes a loud squealing noise when they press the brakes, 
and there's some vibration in the steering wheel sometimes"
```

**NLP Processing**:
- Tokenization and parsing
- Entity extraction (brake noise, steering vibration)
- Intent classification (symptom analysis request)
- Semantic understanding (linking "squealing" + "brakes" → brake pad issue)

**Output**: Structured understanding that triggers symptom search in RAG system

#### 2.1.2 Named Entity Recognition (NER)

**Entities Extracted**:
- **Vehicle Information**: Brand, model, year (e.g., "Toyota Corolla 2018")
- **Diagnostic Codes**: OBD-II codes (e.g., "P0420", "P0300")
- **Symptoms**: Noises, behaviors, warning lights
- **Components**: Parts mentioned (catalytic converter, brake pads, etc.)

**Example**:
```
Input: "I have a 2018 Corolla with code P0420 and check engine light"
Extracted:
  - Vehicle: {brand: "Toyota", model: "Corolla", year: 2018}
  - Code: "P0420"
  - Symptom: "check engine light"
```

#### 2.1.3 Question Generation

**Task**: Generate contextually relevant follow-up questions for diagnosis

**Example**:
```
Given symptom: "engine overheating"
Generated questions:
  - "Is the coolant level low?"
  - "Is the cooling fan running when the engine is hot?"
  - "Are there any visible coolant leaks?"
```

**Method**: GPT-4 uses domain knowledge to generate diagnostic decision trees

#### 2.1.4 Text Generation

**Task**: Generate natural, professional responses and estimates

**Capabilities**:
- Technical explanations in clear language
- Professional estimate documents
- Diagnostic reasoning explanations
- Part recommendations with justifications

**Example**:
```
Input diagnosis: P0420 on Toyota Corolla
Generated explanation:
"Code P0420 indicates that the catalytic converter's efficiency has dropped below 
the threshold. For your 2018 Corolla, the most common causes are [...]"
```

#### 2.1.5 Semantic Search (RAG)

**Task**: Find relevant information in knowledge base using semantic similarity

**Process**:
1. Mechanic query → Embedded as vector (OpenAI embeddings)
2. Vector similarity search in ChromaDB
3. Top-K most relevant documents retrieved
4. Context injected into LLM prompt

**Example**:
```
Query: "rough idle and stalling"
Retrieved documents:
  1. Symptom: "Rough idle or engine stalling" (95% relevance)
  2. Code P0505: "Idle Air Control System Malfunction" (87% relevance)
  3. Repair guide: "Idle Control Valve Cleaning" (82% relevance)
```

### 2. Why NLP is Useful Here

#### 2.2.1 Flexibility in Input

Mechanics don't need to use specific keywords or formats. They can describe problems as they would to a colleague:
- "Customer says it's making a funny noise"
- "P0420 on a Corolla"
- "Brake pads worn, need estimate"

All are understood correctly.

#### 2.2.2 Knowledge Accessibility

Instead of searching through manuals, the system provides instant answers:
- "What does P0171 mean?" → Instant detailed explanation
- "Common issues Honda Civic 2020?" → List of known problems

#### 2.2.3 Saves Time

Traditional: Look up code → Read manual → Find parts → Calculate cost (20-30 minutes)
With NLP Assistant: Describe problem → Get complete analysis + estimate (<5 minutes)

#### 2.2.4 Reduces Errors

- Automated cost calculation eliminates math errors
- Parts compatibility checking prevents ordering wrong parts
- Comprehensive diagnostic steps ensure nothing is missed

#### 2.2.5 Improves Communication

The system generates professional estimates that mechanics can confidently present to customers, improving trust and transparency.

---

## 3. Conversational Flow Diagram

### 3.1 Mermaid Diagram

See `assets/conversation_diagram.mmd` for the complete Mermaid source.

### 3.2 Flow Explanation

**Entry Points**:
1. **With OBD Code**: Mechanic has a diagnostic trouble code (DTC)
2. **With Symptoms**: Mechanic describes customer complaint without code

**Decision Tree**:

1. **Initial Assessment**
   - If code provided → Tool: `search_diagnostic_code`
   - If symptoms only → RAG: Search symptom database

2. **Knowledge Consultation**
   - RAG retrieval for related information
   - Cross-reference with known issues for vehicle

3. **Diagnosis Refinement**
   - Ask follow-up questions until confidence threshold reached
   - Example: "Does noise occur when engine is cold or hot?"

4. **Solution Identification**
   - Tool: `query_known_issues` for vehicle-specific problems
   - Match symptoms/codes to repair procedures

5. **Parts & Cost**
   - Tool: `find_replacement_parts` → Present OEM vs aftermarket options
   - Tool: `calculate_repair_cost` → Provide detailed breakdown

6. **Estimate Generation**
   - Tool: `generate_estimate` → Professional formatted document

7. **Loop Back**
   - If costs too high → Find alternative parts
   - If diagnosis uncertain → Ask more questions
   - If complete → New diagnosis or end

### 3.3 RAG Integration Points

RAG is consulted at multiple points:

- **Code Search**: Retrieve detailed code information and common causes
- **Symptom Analysis**: Find similar historical cases
- **Repair Procedures**: Access step-by-step repair guides
- **Diagnostic Questions**: Generate relevant follow-up questions

---

## 4. Technical Architecture

### 4.1 Model Selection & Justification

#### Large Language Model: GPT-4 (via OpenRouter)

**Why GPT-4?**

1. **Superior Reasoning**: Automotive diagnosis requires complex reasoning chains (P0420 → catalyst efficiency → check O2 sensors → test converter → estimate cost)

2. **Tool Use**: GPT-4's function calling capability enables reliable autonomous tool execution

3. **Domain Adaptation**: While not specifically trained on automotive data, GPT-4's broad knowledge covers automotive fundamentals well

4. **Context Window**: 8K+ tokens allow inclusion of:
   - Conversation history
   - Retrieved RAG context
   - Tool descriptions
   - System prompts

5. **Reliability**: More consistent than smaller models for multi-step tasks

**Why OpenRouter?**
- Cost-effective access to GPT-4
- No rate limiting for educational projects
- Simple API compatible with OpenAI SDK

#### Embedding Model: text-embedding-3-small (OpenAI)

**Why this model?**

1. **Performance**: 1536-dimensional embeddings with excellent semantic capture
2. **Cost-effective**: Smaller model, lower cost than text-embedding-3-large
3. **Speed**: Fast enough for real-time retrieval
4. **Quality**: Sufficient for automotive technical text (doesn't need domain-specific embeddings)

**Alternatives Considered**:
- Sentence-transformers (all-MiniLM-L6-v2): Free but lower quality
- Cohere embeddings: Good but added API complexity

### 4.2 System Architecture Diagram

```
┌─────────────┐
│   Mechanic │
│   (Gradio) │
└──────┬──────┘
       │
       ▼
┌──────────────────────── ───────────────┐
│       Gradio Interface (Port 7860)           │
│  - Chat UI                                   │
│  - Agent reasoning display                   │
│  - Tools execution viewer                    │
└──────────────┬───────────────────── ─────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│        MechanicAgent (ReAct Pattern)         │
│  ┌────────────────────────────────────────┐  │
│  │      LLM: GPT-4 (OpenRouter)           │  │
│  │  - Reasoning                           │  │
│  │  - Planning                            │  │
│  │  - Tool selection                      │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │   Conversation Memory (Buffer)         │  │
│  └────────────────────────────────────────┘  │
└──────┬───────────────────────────┬───────────┘
       │                           │
       │                           │
       ▼                           ▼
┌──────────────────┐      ┌────────────────────┐
│   RAG System     │      │    Tool Suite      │
│                  │      │  (5 Tools)         │
│ ┌──────────────┐ │      │                    │
│ │  ChromaDB    │ │      │  1. search_code    │
│ │  Vector DB   │ │      │  2. calc_cost      │
│ └──────────────┘ │      │  3. find_parts     │
│                  │      │  4. known_issues   │
│ ┌──────────────┐ │      │  5. gen_estimate   │
│ │  Embeddings  │ │      │                    │
│ │ (OpenAI)     │ │      └────────────────────┘
│ └──────────────┘ │               │
│                  │               │
│ ┌──────────────┐ │               ▼
│ │  Retriever   │ │      ┌────────────────────┐
│ │  (Top-K=3)   │ │      │   Data Sources     │
│ └──────────────┘ │      │                    │
└──────────────────┘      │  - parts_catalog   │
                          │  - labor_rates     │
                          │  - obd_codes       │
                          └────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│      Knowledge Base Files        │
│  - obd_codes.json (23 codes)     │
│  - common_symptoms.json (18)     │
│  - repair_guides.txt (4 guides)  │
└──────────────────────────────────┘

       │
       ▼
┌──────────────────────────────────┐
│       Langfuse Monitoring       │
│  - Trace all LLM calls           │
│  - Track tool executions         │
│  - Log token usage               │
│  - Performance metrics           │
└──────────────────────────────────┘
```

### 4.3 Component Descriptions

#### 4.3.1 Gradio Interface (`app.py`)

**Responsibilities**:
- User interaction (chat interface)
- Display agent reasoning in real-time
- Show tool execution results
- Conversation management (history, reset)

**Technology**: Gradio 6.0.0 with custom CSS for modern UI

#### 4.3.2 MechanicAgent (`src/agent/mechanic_agent.py`)

**Type**: ReAct (Reasoning + Acting) Agent

**Responsibilities**:
- Process user input
- Decide which tools to use and in what order
- Consult RAG when needed
- Generate natural language responses
- Maintain conversation context

**Key Methods**:
- `chat(message)`: Main interaction method
- `consult_knowledge_base(query)`: RAG retrieval
- `reset_conversation()`: Clear memory

#### 4.3.3 RAG System

**Components**:
1. **Document Loader** (`document_loader.py`): Converts JSON/TXT → LangChain Documents
2. **Knowledge Base** (`knowledge_base.py`): Manages ChromaDB, embeddings, indexing
3. **Retriever** (`retriever.py`): Similarity search wrapper

**Parameters**:
- Chunk size: 500 tokens
- Chunk overlap: 50 tokens
- Top-K: 3 documents
- Embedding model: text-embedding-3-small

#### 4.3.4 Tool Suite

Each tool has a specific function:

1. **search_diagnostic_code**: OBD-II code lookup
2. **calculate_repair_cost**: Parts + labor calculation
3. **find_replacement_parts**: Vehicle-compatible parts search
4. **query_known_issues**: Common problems database
5. **generate_estimate**: Professional estimate generation

**Implementation**: Python functions wrapped in LangChain `Tool` class

### 4.4 Data Flow

1. **User Input** → Gradio interface
2. **Gradio** → Agent's `chat()` method
3. **Agent**:
   - RAG retrieval (if needed) → Knowledge base context
   - Reasoning → Determine action
   - Tool execution (if needed) → Get results
   - LLM generation → Natural language response
4. **Response** → Back to Gradio
5. **All steps** → Logged to Langfuse

---

## 5. Implementation with LangChain

### 5.1 ReAct Agent Pattern

**What is ReAct?**

ReAct combines **Reasoning** and **Acting** in a loop:

```
Thought → Action → Observation → Thought → Action → ...
```

**Example**:
```
Thought: The mechanic mentioned code P0420, I should look it up
Action: search_diagnostic_code
Action Input: "P0420"
Observation: {"description": "Catalyst System Efficiency Below Threshold..."}
Thought: Now I know it's a catalytic converter issue. I should find parts.
Action: find_replacement_parts
Action Input: '{"vehicle": {"brand": "Toyota", "model": "Corolla", "year": "2018"}, "part_name": "catalytic converter"}'
Observation: [{"name": "Cat Converter - OEM", "price": 650}, ...]
Thought: I have prices. Let me calculate total cost.
... (continues until estimate generated)
```

### 5.2 Agent Implementation

**Code Structure** (`mechanic_agent.py`):

```python
class MechanicAgent:
    def __init__(self):
        self.llm = ChatOpenAI(...)  # GPT-4 via OpenRouter
        self.tools = get_all_tools()  # 5 tools
        self.knowledge_base = initialize_knowledge_base()
        self.memory = ConversationBufferMemory()
        self.agent_executor = create_react_agent(...)
    
    def chat(self, message):
        # 1. Optionally consult RAG
        kb_context = self.consult_knowledge_base(message)
        
        # 2. Augment input with context
        full_input = f"{message}\n\nContext: {kb_context}"
        
        # 3. Run agent (ReAct loop)
        result = self.agent_executor.invoke({"input": full_input})
        
        # 4. Return response + steps
        return {
            "response": result["output"],
            "steps": result["intermediate_steps"]
        }
```

### 5.3 RAG Configuration

**ChromaVector Store Setup**:

```python
# Document loading
docs = load_all_knowledge_base(
    obd_codes_path,
    symptoms_path,
    repair_guides_path
)

# Text splitting
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(docs)

# Create vector store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    persist_directory="./chroma_db"
)
```

**Retrieval**:

```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
relevant_docs = retriever.get_relevant_documents(query)
```

### 5.4 Tool Schemas

**Example Tool Definition**:

```python
diagnostic_code_tool = Tool(
    name="search_diagnostic_code",
    description="""Search for OBD-II code information.
    
    Input: Code string (e.g., "P0420")
    Returns: JSON with code details
    """,
    func=search_code_wrapper  # Wrapper function
)
```

**How Agent Uses Tools**:

1. LLM decides a tool is needed
2. Generates tool name and input
3. Tool executes
4. Result returned to LLM as "Observation"
5. LLM decides next step

### 5.5 Conversation Memory

**Type**: ConversationBufferMemory

**What it stores**:
- All user inputs
- All agent responses
- Tool executions (visible to agent)

**Why important**:
- Enables multi-turn diagnosis
- Agent remembers vehicle info mentioned earlier
- Can reference previous parts discussed

**Example**:
```
Turn 1:
User: "Toyota Corolla 2018 with P0420"
Agent: [Diagnoses, finds it's cat converter issue]

Turn 2:
User: "How much for aftermarket part instead?"
Agent: [Remembers it's about cat converter, searches aftermarket options]
```

---

##6. Monitoring & Metrics

### 6.1 Langfuse Integration

**Setup** (`langfuse_config.py`):

```python
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "..."
os.environ["LANGCHAIN_PROJECT"] = "mechanic-diagnostic-assistant"
```

**What is Traced**:

1. **LLM Calls**:
   - Input prompts (full ReAct reasoning)
   - Model responses
   - Token usage (input/output)
   - Latency

2. **Tool Executions**:
   - Tool name
   - Input parameters
   - Output results
   - Execution time

3. **RAG Retrievals**:
   - Query
   - Retrieved documents
   - Relevance scores

4. **Full Conversation Traces**:
   - End-to-end user interaction
   - All intermediate steps
   - Final response

### 6.2 Metrics Captured

| Metric | Description | Purpose |
|--------|-------------|---------|
| Tokens Used | Input + output tokens per LLM call | Cost tracking |
| Latency | Time per agent turn | Performance monitoring |
| Tool Usage | Which tools used how often | Understanding agent behavior |
| RAG Retrieval Quality | Relevance of retrieved docs | KB optimization |
| Success Rate | % of successful completions | Quality assurance |
| Error Types | Parsing errors, tool failures | Debugging |

### 6.3 Example Trace

**Dashboard View** (Langfuse):

```
Run: mechanic-diagnostic-assistant-run-abc123
Duration: 8.3s
Tokens: 1,245 (input: 892, output: 353)
Cost: $0.025

Steps:
  1. LLM Call (Reasoning) - 2.1s
     Input: "Mechanic: Toyota Corolla 2018 with code P0420..."
     Output: "Thought: I should search for P0420..."
  
  2. Tool: search_diagnostic_code - 0.3s
     Input: "P0420"
     Output: {"description": "Catalyst System...", ...}
  
  3. RAG Retrieval - 1.2s
     Query: "P0420 catalytic converter causes"
     Retrieved: 3 documents
  
  4. Tool: find_replacement_parts - 0.5s
     Input: '{"vehicle": {...}, "part_name": "catalytic converter"}'
     Output: [parts list]
  
  5. Tool: calculate_cost - 0.2s
  
  6. Tool: generate_estimate - 0.4s
  
  7. LLM Call (Final Response) - 3.6s
     Output: "Based on diagnostic code P0420..."
```

### 6.4 Public Dashboard

Traces can be made public for academic review:
- Link: `https://smith.langchain.com/public/{project_id}/...`
- Includes anonymized conversation examples
- Shows agent reasoning transparently

---

## 7. Use Cases & Examples

### 7.1 Case 1: OBD Code P0420 Diagnosis → Estimate

**Scenario**: Mechanic has a 2018 Toyota Corolla with check engine light and code P0420.

**Conversation**:

```
Mechanic: "I have a Toyota Corolla 2018 with code P0420"

[Agent Reasoning & Tool Usage]:
  
  Step 1: search_diagnostic_code("P0420")
  Result: {
    "code": "P0420",
    "description": "Catalyst System Efficiency Below Threshold",
    "common_causes": ["Deteriorated catalytic converter", "Oxygen sensor malfunction", ...]
  }
  
  Step 2: RAG Retrieval - "P0420 Toyota Corolla"
  Retrieved: Document about known P0420 issues in 2015-2018 Corollas
  
  Step 3: query_known_issues({"brand": "Toyota", "model": "Corolla", "year": 2018})
  Result: "Premature catalytic converter failure - Common issue, extended warranty may apply"
