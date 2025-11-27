from unittest.mock import Mock

from src.core.ports.specification_ports import SpecificationGenerationCommandPort
from src.shell.registry.tool_registry import ToolRegistry


def test_tool_registry_initialization():
    registry = ToolRegistry()

    assert hasattr(registry, '_tools')
    assert isinstance(registry._tools, dict)
    assert len(registry._tools) == 0


def test_tool_registry_register_tool():
    registry = ToolRegistry()

    # Create a mock tool
    mock_tool = Mock(spec=SpecificationGenerationCommandPort)

    # Register the tool
    registry.register_tool("test_tool", mock_tool)
    
    # Verify it was added to the registry
    assert "test_tool" in registry._tools
    assert registry._tools["test_tool"] is mock_tool


def test_tool_registry_register_tool_duplicate():
    """Test register_tool method with duplicate name (should overwrite)"""
    registry = ToolRegistry()
    
    # Create mock tools
    mock_tool1 = Mock(spec=SpecificationGenerationCommandPort)
    mock_tool2 = Mock(spec=SpecificationGenerationCommandPort)
    
    # Register the first tool
    registry.register_tool("test_tool", mock_tool1)
    
    # Register a different tool with the same name
    registry.register_tool("test_tool", mock_tool2)
    
    # Verify the second tool overwrote the first
    assert registry._tools["test_tool"] is mock_tool2


def test_tool_registry_register_all_to_mcp():
    """Test register_all_to_mcp method"""
    mock_mcp = Mock()

    registry = ToolRegistry()

    mock_tool1 = Mock(spec=SpecificationGenerationCommandPort)
    mock_tool2 = Mock(spec=SpecificationGenerationCommandPort)

    registry.register_tool("tool1", mock_tool1)
    registry.register_tool("tool2", mock_tool2)

    registry.register_all_to_mcp(mock_mcp)

    assert mock_mcp.tool.call_count == 2

    calls = mock_mcp.tool.call_args_list

    assert any('name' in call[1] and call[1]['name'] == 'tool1' for call in calls)
    assert any('name' in call[1] and call[1]['name'] == 'tool2' for call in calls)