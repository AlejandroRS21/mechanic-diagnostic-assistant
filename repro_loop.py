
import os
import sys
from dotenv import load_dotenv

load_dotenv('.env')
sys.path.append(os.getcwd())

from src.agent.mechanic_agent import create_agent

def repro_issue():
    print("🚀 Reproducing Iteration Limit Issue")
    print("-" * 50)
    
    agent = create_agent(verbose=True)
    
    # query = "El auto hace un ruido chirriante al frenar"
    # User reported exact string.
    query = "El auto hace un ruido chirriante al frenar"
    
    print(f"\nQuery: {query}")
    print("-" * 30)
    
    try:
        result = agent.chat(query)
        print("\nResult:")
        print(result.get("response"))
        
        print("\nSteps taken:")
        for step in result.get("steps", []):
            print(f"- Tool: {step.get('tool')}")
            print(f"  Input: {step.get('tool_input')}")
            print(f"  Observation: {step.get('observation')}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    repro_issue()
