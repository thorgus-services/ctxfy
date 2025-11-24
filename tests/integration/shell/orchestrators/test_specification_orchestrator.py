from unittest.mock import Mock

from src.shell.orchestrators.specification_orchestrator import SpecificationOrchestrator


def test_specification_orchestrator_initialization():
    """Test SpecificationOrchestrator initialization and component setup"""
    mock_mcp = Mock()

    orchestrator = SpecificationOrchestrator(mock_mcp)

    assert hasattr(orchestrator, 'mcp')
    assert orchestrator.mcp is mock_mcp


def test_specification_orchestrator_components_registration():
    """Test that SpecificationOrchestrator properly registers tools and prompts"""
    mock_mcp = Mock()

    SpecificationOrchestrator(mock_mcp)

    tool_calls = [call for call in mock_mcp.method_calls if call[0] == 'tool']
    prompt_calls = [call for call in mock_mcp.method_calls if call[0] == 'prompt']

    assert len(tool_calls) >= 1
    assert len(prompt_calls) >= 1


def test_specification_orchestrator_integration_with_real_components():
    """Integration test with real components (not mocks)"""
    mock_mcp = Mock()

    SpecificationOrchestrator(mock_mcp)

    tool_registered = any(call[0] == 'tool' for call in mock_mcp.method_calls)
    prompt_registered = any(call[0] == 'prompt' for call in mock_mcp.method_calls)

    assert tool_registered
    assert prompt_registered

    registered_tool_names = [call[2]['name'] for call in mock_mcp.method_calls if call[0] == 'tool' and 'name' in call[2]]
    registered_prompt_names = [call[2]['name'] for call in mock_mcp.method_calls if call[0] == 'prompt' and 'name' in call[2]]

    assert "generate_specification" in registered_tool_names
    assert "specification_save_instruction" in registered_prompt_names