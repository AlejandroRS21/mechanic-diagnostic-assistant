"""
Main Mechanic Diagnostic Agent using LangChain ReAct pattern.
"""

from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

try:
    from langchain.schema import AgentAction, AgentFinish
except ImportError:
    try:
        from langchain_core.agents import AgentAction, AgentFinish
    except ImportError:
        from langchain_core.schema import AgentAction, AgentFinish

from src.agent.tools import get_all_tools
from src.agent.prompts import SYSTEM_PROMPT, GREETING
from src.rag.knowledge_base import initialize_knowledge_base
from src.rag.retriever import KnowledgeRetriever
from src.utils.helpers import get_logger
from src.utils.language_detector import LanguageDetector, LanguageInstructions
from src.utils.config import OPENROUTER_API_KEY, TOP_K_RESULTS
from src.utils.model_manager import ModelManager

logger = get_logger(__name__)


class MechanicAgent:
    """
    Intelligent diagnostic agent for automotive mechanics.
    Uses ReAct pattern with tools and RAG knowledge base.
    """
    
    def __init__(
        self,
        temperature: float = 0.7,
        verbose: bool = True
    ):
        """
        Initialize the mechanic diagnostic agent.
        
        Args:
            model_name: LLM model to use
            temperature: Model temperature (0-1)
            verbose: Whether to print agent reasoning
        """
        logger.info("Initializing Mechanic Diagnostic Agent...")
        
        # Initialize Model Manager
        self.model_manager = ModelManager()
        self.current_model_name = self.model_manager.get_current_model_id()
        
        if not self.current_model_name:
            raise ValueError("No available models found from OpenRouter")
            
        logger.info(f"Using initial model: {self.current_model_name}")
        
        # Initialize LLM via OpenRouter
        self.llm = self._create_llm()
        
        # Initialize knowledge base and retriever
        logger.info("Loading knowledge base...")
        self.knowledge_base = initialize_knowledge_base(rebuild=False)
        self.retriever = KnowledgeRetriever(
            self.knowledge_base,
            k=TOP_K_RESULTS
        )
        
        # Get tools
        self.tools = get_all_tools()
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
        
        # Create agent
        self.agent_executor = self._create_agent(verbose=verbose)
        
        # Track agent steps for UI display
        self.last_steps: List[Dict] = []
        
        logger.info("✅ Mechanic Agent initialized successfully")
    
        logger.info("✅ Mechanic Agent initialized successfully")
    
    def _create_llm(self) -> ChatOpenAI:
        """Create LLM instance with current model."""
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is missing. Please add it to your .env file.")
            
        return ChatOpenAI(
            model=self.current_model_name,
            temperature=0.7,
            openai_api_key=OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
            max_tokens=1024
        )

    def _create_agent(self, verbose: bool = True) -> AgentExecutor:
        """Create the ReAct agent with tools."""
        
        # Create ReAct prompt template with clearer format
        template = f"""{SYSTEM_PROMPT}

You have access to the following tools:

{{tools}}

**CRITICAL: RESPOND USING THIS EXACT FORMAT - NO OTHER TEXT ALLOWED:**

Thought: <what I need to do next>
Action: <tool name from list: {{tool_names}}>
Action Input: <simple input string for the tool>
Observation: <will be provided by system>

**When ready to answer:**
Thought: <I now have enough information>
Final Answer: <your complete response>

**STOP IMMEDIATELY AFTER Final Answer - DO NOT ADD ANY TEXT**

**CRITICAL RULES:**
1. Use tool names EXACTLY as listed: {{tool_names}}
2. Action and Action Input MUST be on separate lines
3. Action Input must be plain text (no quotes, no formatting)
4. After writing "Final Answer:", STOP - do not add ANY text or thoughts
5. Never write "Thought:" after "Final Answer:"
6. If you write Final Answer, your turn is OVER

Previous conversation:
{{chat_history}}

{{input}}
Thought:{{agent_scratchpad}}"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "tools", "tool_names", "agent_scratchpad", "chat_history"]
        )
        
        # Custom parsing error message
        parsing_error_message = (
            "Invalid format. Please use EXACTLY this format:\n"
            "Thought: <what to do>\n"
            "Action: <tool name>\n"
            "Action Input: <input>\n\n"
            "OR if ready to answer:\n"
            "Thought: <reasoning>\n"
            "Final Answer: <response>\n\n"
            "STOP after Final Answer - do not add any text."
        )

        # Get Langfuse callback if available
        try:
            from src.monitoring.langfuse_config import get_langfuse_handler
            langfuse_handler = get_langfuse_handler()
            callbacks = [langfuse_handler] if langfuse_handler else []
        except:
            callbacks = []

        # Use initialize_agent (more robust in this environment)
        from langchain.agents import initialize_agent, AgentType
        
        agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=verbose,
            max_iterations=10,
            memory=self.memory,
            handle_parsing_errors=parsing_error_message,
            return_intermediate_steps=True,
            callbacks=callbacks,
            early_stopping_method="force",
            agent_kwargs={
                "prefix": SYSTEM_PROMPT
            }
        )
        
        # Create executor with callbacks
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=verbose,
            max_iterations=10,  # Increased to allow more tool usage
            handle_parsing_errors=parsing_error_message,  # Custom error message
            return_intermediate_steps=True,
            callbacks=callbacks,  # Add Langfuse tracing
            early_stopping_method="force"  # Force stop at max iterations
        )
        
        return agent
    
    def consult_knowledge_base(self, query: str) -> tuple[str, List[Dict]]:
        """
        Consult the RAG knowledge base for relevant information.
        
        Args:
            query: Search query
            
        Returns:
            Tuple of (Formatted context, List of sources)
        """
        logger.info(f"Consulting knowledge base: {query}")
        context, sources = self.retriever.retrieve_with_sources(query)
        return context, sources
    
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Send a message to the agent and get a response.
        Detects the language of the user input and responds in the same language.
        
        Args:
            message: Message from the mechanic
            
        Returns:
            Dictionary with response and metadata
        """
        logger.info(f"Processing message: {message[:100]}...")
        
        # HARDCODED SPANISH CONFIGURATION PER USER REQUEST
        # We ignore detection and force Spanish for everything.
        language_name = "Spanish"
        strong_instruction = (
            "IMPORTANTE: DEBES responder SIEMPRE en ESPAÑOL. "
            "TRADUCE tu respuesta final y explicaciones.\n"
            "CRITICO: NO TRADUZCAS LOS COMANDOS DEL PROTOCOLO.\n"
            "MANTÉN 'Thought:', 'Action:', 'Action Input:', y 'Final Answer:' EXACTAMENTE EN INGLÉS.\n"
            "Ejemplo correcto:\n"
            "Thought: He encontrado el problema.\n"
            "Final Answer: El problema es..."
        )
        
        logger.info(f"Forcing language: {language_name}")
        
        # Augment input with knowledge base context if relevant
        # (Check if message contains keywords that should trigger KB search)
        kb_context = ""
        sources = []
        # Keywords list kept broad to catch english terms too just in case
        keywords = ["code", "P0", "symptom", "noise", "leak", "problem", "issue", "manual", "guide", "pdf",
                   "código", "síntoma", "ruido", "fuga", "problema", "asunto", "manual",  # Spanish
                   "código", "sintoma", "barulho", "vazamento", "problema", "manual",  # Portuguese
                   "code", "symptôme", "bruit", "fuite", "problème", "manuel"]  # French

        if any(keyword in message.lower() for keyword in keywords):
            logger.info("Augmenting with knowledge base context...")
            kb_context, sources = self.consult_knowledge_base(message)
        
        if kb_context:
            full_input = f"{message}\n\nInformación relevante de la base de conocimientos:\n{kb_context}\n\n[SISTEMA: {strong_instruction}]"
        else:
            full_input = f"{message}\n\n[SISTEMA: {strong_instruction}]"
        
        # Retry loop for model failover
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Run agent
                result = self.agent_executor.invoke({"input": full_input})
                
                # Extract response and intermediate steps
                response = result.get("output", "I'm sorry, I couldn't process that request.")
                intermediate_steps = result.get("intermediate_steps", [])
                
                # Format intermediate steps for UI
                self.last_steps = []
                for step in intermediate_steps:
                    if isinstance(step, tuple) and len(step) == 2:
                        action, observation = step
                        if isinstance(action, AgentAction):
                            self.last_steps.append({
                                "tool": action.tool,
                                "tool_input": action.tool_input,
                                "observation": str(observation)[:200]  # Truncate for display
                            })
                
                return {
                    "response": response,
                    "steps": self.last_steps,
                    "sources": sources,
                    "success": True
                }
            
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Error in agent chat (Attempt {attempt+1}/{max_retries}): {error_msg}")
                
                # Check for rate limit or API errors
                # Broaden check to include generic provider errors
                error_lower = error_msg.lower()
                retry_keywords = ["429", "rate limit", "insufficient_quota", "provider", "error", "fail", "timeout", "connection"]
                
                if any(keyword in error_lower for keyword in retry_keywords):
                    logger.warning(f"API Error with model {self.current_model_name}: {error_msg}")
                    logger.warning("Switching model...")
                    self.model_manager.mark_current_failed()
                    
                    new_model = self.model_manager.get_current_model_id()
                    if new_model and new_model != self.current_model_name:
                        self.current_model_name = new_model
                        logger.info(f"Switching to new model: {self.current_model_name}")
                        
                        # Recreate LLM and Agent
                        self.llm = self._create_llm()
                        self.agent_executor = self._create_agent(verbose=True)
                        continue
                
                # If it's the last attempt or not a recoverable error
                if attempt == max_retries - 1:
                    return {
                        "response": f"I encountered an error and ran out of retries: {str(e)}. Please try again later.",
                        "steps": [],
                        "success": False,
                        "error": str(e)
                    }
        
        # Fallback if loop finishes without return
        return {
            "response": "I encountered an error and could not process your request after multiple attempts.",
            "steps": [],
            "success": False,
            "error": "Max retries exceeded"
        }
    
    def reset_conversation(self):
        """Reset the conversation memory."""
        self.memory.clear()
        self.last_steps = []
        logger.info("Conversation reset")
    
    def get_greeting(self) -> str:
        """Get the initial greeting message."""
        return GREETING
    
    def get_last_steps(self) -> List[Dict]:
        """Get the last agent reasoning steps."""
        return self.last_steps


def create_agent(model_name: str = None, verbose: bool = True) -> MechanicAgent:
    """
    Factory function to create a mechanic diagnostic agent.
    
    Args:
        model_name: Optional model name to override default
        verbose: Whether to enable verbose logging
        
    Returns:
        Initialized MechanicAgent
    """
    try:
        agent = MechanicAgent(verbose=verbose)
        return agent
    except Exception as e:
        logger.error(f"Failed to create agent: {e}")
        raise


if __name__ == "__main__":
    # Test the agent
    print("Initializing agent...")
    print("-" * 60)
    
    agent = create_agent(verbose=True)
    
    print("\n" + agent.get_greeting())
    print("\n" + "-" * 60)
    
    # Test interaction
    test_message = "I have a Toyota Corolla 2018 with code P0420"
    print(f"\nTest message: {test_message}")
    print("-" * 60)
    
    response = agent.chat(test_message)
    
    print(f"\nAgent response:\n{response['response']}")
    
    if response['steps']:
        print(f"\nTools used: {len(response['steps'])}")
        for step in response['steps']:
            print(f"  - {step['tool']}")
    
    print("\n✅ Agent test completed")
