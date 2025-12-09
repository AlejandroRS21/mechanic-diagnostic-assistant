#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify the complete agent flow with a Spanish query.
"""

import sys
import os
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agent.mechanic_agent import create_agent
from src.utils.helpers import get_logger

logger = get_logger(__name__)

print("=" * 70)
print("INTEGRATION TEST: Agent Flow with Spanish Query")
print("=" * 70)

try:
    # Create the agent
    print("\nCreating agent...")
    agent = create_agent()
    print("Agent created successfully")
    
    # Test query in Spanish
    test_query = "El auto hace un ruido chirriante al frenar"
    print(f"\nTest query: {test_query}")
    print("-" * 70)
    
    # Send message to agent
    print("\nProcessing query...")
    response = agent.chat(test_query)
    
    print("\n" + "=" * 70)
    print("RESPONSE FROM AGENT:")
    print("=" * 70)
    print(response)
    print("\n" + "=" * 70)
    print("AGENT FLOW TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)
    
except Exception as e:
    print(f"\nError during agent flow: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
