
import logging
import sys
from src.agent.mechanic_agent import create_agent

# Force logging configuration
root_logger = logging.getLogger()
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("debug_u0100.log", encoding='utf-8', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

def test_u0100_loop():
    print("Initializing agent...")
    agent = create_agent(verbose=True)
    
    query = "Código U0100 en Honda Civic 2018, no arranca"
    print(f"\nTesting query: {query}")
    print("-" * 50)
    
    response = agent.chat(query)
    
    print("\nResult:")
    print(response)

if __name__ == "__main__":
    test_u0100_loop()
