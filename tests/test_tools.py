"""
Tests for individual tools.
Run with: pytest tests/test_tools.py -v
"""

import pytest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_diagnostic_code_tool():
    """Test diagnostic code search."""
    from src.tools_impl.diagnostic_codes import search_diagnostic_code
    
    result = search_diagnostic_code("P0420")
    
    assert result['found'] == True
    assert result['code'] == "P0420"
    assert 'description' in result
    assert 'common_causes' in result
    assert len(result['common_causes']) > 0


def test_diagnostic_code_tool_not_found():
    """Test diagnostic code search with non-existent code."""
    from src.tools_impl.diagnostic_codes import search_diagnostic_code
    
    result = search_diagnostic_code("P9999")
    
    assert result['found'] == False
    assert 'message' in result


def test_cost_calculator():
    """Test repair cost calculation."""
    from src.tools_impl.cost_calculator import calculate_repair_cost
    
    result = calculate_repair_cost(parts=["CAT-001"], labor_hours=2.5)
    
    assert 'grand_total' in result
    assert result['grand_total'] > 0
    assert 'parts_cost' in result
    assert 'labor_cost' in result
    assert result['labor_hours'] == 2.5


def test_parts_finder():
    """Test parts finder tool."""
    from src.tools_impl.parts_finder import find_replacement_parts
    
    vehicle = {"brand": "Toyota", "model": "Corolla", "year": "2018"}
    result = find_replacement_parts(vehicle, "catalytic converter")
    
    assert 'parts_found' in result
    assert result['parts_found'] > 0
    assert 'parts' in result
    assert isinstance(result['parts'], list)


def test_known_issues():
    """Test known issues query."""
    from src.tools_impl.known_issues import query_known_issues
    
    result = query_known_issues("Toyota", "Corolla", 2018)
    
    assert 'issues_found' in result
    assert 'common_issues' in result
    assert isinstance(result['common_issues'], list)


def test_estimate_generator():
    """Test estimate generation."""
    from src.tools_impl.estimate_generator import generate_estimate
    
    solution = {
        "parts": [{"name": "Test Part", "price": 100}],
        "labor_hours": 2.0,
        "parts_cost": 100,
        "labor_cost": 170,
        "grand_total": 270
    }
    
    result = generate_estimate(
        diagnosis="Test diagnosis",
        solution=solution
    )
    
    assert 'estimate_number' in result
    assert 'formatted_estimate' in result
    assert 'estimated_cost' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
