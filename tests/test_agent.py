"""
Basic tests for the agent system.
Run with: pytest tests/test_agent.py -v
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_agent_imports():
    """Test that agent modules can be imported."""
    try:
        from src.agent.mechanic_agent import MechanicAgent
        from src.agent.tools import get_all_tools
        from src.agent.prompts import SYSTEM_PROMPT
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import agent modules: {e}")


def test_tools_available():
    """Test that all 5 tools are available."""
    from src.agent.tools import get_all_tools
    
    tools = get_all_tools()
    assert len(tools) == 5, f"Expected 5 tools, got {len(tools)}"
    
    tool_names = [tool.name for tool in tools]
    expected = [
        "search_diagnostic_code",
        "calculate_repair_cost",
        "find_replacement_parts",
        "query_known_issues",
        "generate_estimate"
    ]
    
    for expected_tool in expected:
        assert expected_tool in tool_names, f"Tool {expected_tool} not found"


@pytest.mark.skip(reason="Requires API keys - run manually")
def test_agent_initialization():
    """Test agent can be initialized (requires API keys)."""
    from src.agent.mechanic_agent import create_agent
    
    agent = create_agent(verbose=False)
    assert agent is not None
    assert hasattr(agent, 'chat')
    assert hasattr(agent, 'reset_conversation')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
