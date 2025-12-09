
import os
import sys
from dotenv import load_dotenv

# Load env
load_dotenv('.env')

# Add src to path
sys.path.append(os.getcwd())

from src.agent.mechanic_agent import create_agent

def test_examples():
    print("🚀 Starting Quick Examples Test")
    print("-" * 50)
    
    agent = create_agent(verbose=True)
    
    examples = [
        "Tengo un Toyota Corolla 2018 con código P0420",
        "El auto hace un ruido chirriante al frenar",
        "Check engine encendido, ralentí irregular, Toyota Camry 2019",
        "¿Cuáles son los problemas comunes del Honda Civic 2020?",
        "Necesito presupuesto para cambio de pastillas de freno en Nissan Sentra 2017"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n🧪 Test {i}: {example}")
        print("-" * 30)
        
        try:
            result = agent.chat(example)
            
            if result.get("success"):
                print("✅ Success!")
                response = result.get("response", "")
                print(f"Response preview: {response[:100]}...")
            else:
                print("❌ Failed!")
                print(f"Error: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            
    print("\n🏁 All tests completed")

if __name__ == "__main__":
    test_examples()
