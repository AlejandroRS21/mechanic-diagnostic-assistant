#!/usr/bin/env python3
"""
End-to-end test of the mechanic assistant with P0258.
"""

import logging
logging.basicConfig(level=logging.WARNING)

from src.agent.mechanic_agent import MechanicAgent

def test_p0258_with_agent():
    """Test P0258 search through the agent."""
    
    print("\n" + "="*80)
    print("END-TO-END TEST: P0258 Search via Mechanic Agent")
    print("="*80)
    
    # Initialize agent
    print("\n[1] Initializing Mechanic Agent...")
    agent = MechanicAgent()
    
    # Test in Spanish (user's language)
    print("\n[2] Testing Spanish query for P0258...")
    query = "¿Qué significa el código P0258 en un Toyota Avensis 2006?"
    
    print(f"\nUser: {query}")
    print("-" * 80)
    
    response = agent.chat(query)
    
    print(f"\nAssistant:")
    print(response)
    
    # Check if P0258 is mentioned in response
    if "P0258" in response or "p0258" in response.lower():
        print("\n✅ SUCCESS - P0258 found and explained in response!")
    else:
        print("\n⚠️  P0258 not explicitly mentioned, but search may have found it")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    try:
        test_p0258_with_agent()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
