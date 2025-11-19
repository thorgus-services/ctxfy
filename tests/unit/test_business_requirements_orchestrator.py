from unittest.mock import AsyncMock

import pytest

from src.core.models.business_requirements_models import (
    BusinessRequirementConfig,
    BusinessRequirements,
)
from src.shell.orchestrators.business_requirements_orchestrator import (
    BusinessRequirementsOrchestrator,
)


class TestBusinessRequirementsOrchestrator:
    """Test cases for BusinessRequirementsOrchestrator"""
    
    @pytest.fixture
    def mock_ctx(self):
        """Create a mock context object"""
        ctx = AsyncMock()
        ctx.sample = AsyncMock()
        ctx.error = AsyncMock()
        ctx.log = AsyncMock()
        return ctx
    
    @pytest.fixture
    def mock_filesystem_adapter(self):
        """Create a mock filesystem adapter"""
        adapter = AsyncMock()
        adapter.directory_exists = AsyncMock(return_value=True)
        adapter.create_directory = AsyncMock(return_value=True)
        adapter.write_file = AsyncMock(return_value=True)
        return adapter
    
    @pytest.fixture
    def orchestrator(self, mock_ctx, mock_filesystem_adapter):
        """Create a BusinessRequirementsOrchestrator instance"""
        return BusinessRequirementsOrchestrator(
            ctx=mock_ctx,
            filesystem_adapter=mock_filesystem_adapter
        )
    
    @pytest.mark.asyncio
    async def test_translate_business_requirements_success(self, orchestrator, mock_ctx, mock_filesystem_adapter):
        """Test successful business requirements translation"""
        # Arrange
        config = BusinessRequirementConfig(
            requirements_text="Create a user management system",
            output_directory="ctxfy/specifications"
        )
        
        # Mock LLM response
        mock_ctx.sample.return_value = {
            "content": "# Technical Specification\n\nSystem for managing users..."
        }
        
        # Act
        result = await orchestrator.translate_business_requirements(config)
        
        # Assert
        assert result.success is True
        assert result.specification is not None
        assert "# Technical Specification" in result.specification.content
        mock_ctx.sample.assert_called_once()
        mock_filesystem_adapter.write_file.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_translate_business_requirements_with_string_response(self, orchestrator, mock_ctx, mock_filesystem_adapter):
        """Test translation with string response from LLM"""
        # Arrange
        config = BusinessRequirementConfig(
            requirements_text="Create an API endpoint",
            output_directory="ctxfy/specifications"
        )
        
        # Mock LLM response as string
        mock_ctx.sample.return_value = "# API Specification\n\nEndpoint for user management..."
        
        # Act
        result = await orchestrator.translate_business_requirements(config)
        
        # Assert
        assert result.success is True
        assert result.specification is not None
        assert "# API Specification" in result.specification.content
        mock_ctx.sample.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_translate_business_requirements_invalid_config(self, orchestrator, mock_ctx):
        """Test translation with invalid configuration"""
        # Test needs to validate config before calling translate_business_requirements
        # because the validation happens in __init__
        from src.core.models.business_requirements_models import (
            BusinessRequirementConfig,
        )

        # This should raise a ValueError during config creation
        with pytest.raises(ValueError, match="Requirements text must be a valid string"):
            BusinessRequirementConfig(
                requirements_text="",  # Invalid: empty requirements
                output_directory="ctxfy/specifications"
            )
    
    @pytest.mark.asyncio
    async def test_translate_business_requirements_security_rejection(self, orchestrator, mock_ctx):
        """Test translation with security issues"""
        # Arrange
        config = BusinessRequirementConfig(
            requirements_text="Execute os.system('rm -rf /')",  # Contains dangerous content
            output_directory="ctxfy/specifications"
        )
        
        # Act
        result = await orchestrator.translate_business_requirements(config)
        
        # Assert
        assert result.success is False
        assert len(result.errors) > 0
        assert any("malicious content detected" in str(error).lower() for error in result.errors)
        mock_ctx.sample.assert_not_called()
        mock_ctx.error.assert_called()
    
    @pytest.mark.asyncio
    async def test_translate_business_requirements_llm_error(self, orchestrator, mock_ctx, mock_filesystem_adapter):
        """Test translation when LLM returns error response"""
        # Arrange
        config = BusinessRequirementConfig(
            requirements_text="Create a simple system",
            output_directory="ctxfy/specifications"
        )
        
        # Mock LLM error response
        mock_ctx.sample.return_value = "Error: LLM could not process request"
        
        # Act
        result = await orchestrator.translate_business_requirements(config)
        
        # Assert
        assert result.success is True  # Processing continues even with string response
        assert result.specification is not None
        mock_ctx.sample.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_translate_business_requirements_filesystem_error(self, orchestrator, mock_ctx, mock_filesystem_adapter):
        """Test translation when filesystem write fails"""
        # Arrange
        config = BusinessRequirementConfig(
            requirements_text="Create a user management system",
            output_directory="ctxfy/specifications"
        )
        
        # Mock LLM response
        mock_ctx.sample.return_value = {
            "content": "# Technical Specification\n\nSystem for managing users..."
        }
        
        # Mock filesystem write failure
        mock_filesystem_adapter.write_file.return_value = False
        
        # Act
        result = await orchestrator.translate_business_requirements(config)
        
        # Assert
        assert result.success is False
        assert len(result.errors) > 0
        assert any("Failed to write specification" in str(error) for error in result.errors)
        mock_filesystem_adapter.write_file.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_translation_status(self, orchestrator, mock_ctx):
        """Test getting translation status"""
        # Act
        status = await orchestrator.get_translation_status("test-id")
        
        # Assert
        assert status.translation_id == "test-id"
        assert status.status == "completed"  # Based on implementation
    
    @pytest.mark.asyncio
    async def test_validate_requirements(self, orchestrator, mock_ctx):
        """Test validating requirements"""
        # Arrange
        requirements = BusinessRequirements(
            content="Valid business requirements with sufficient content for testing"
        )
        
        # Act
        result = await orchestrator.validate_requirements(requirements)
        
        # Assert
        assert result is True  # Should be valid based on content
    
    @pytest.mark.asyncio
    async def test_validate_requirements_invalid(self, orchestrator, mock_ctx):
        """Test validating invalid requirements"""
        # Arrange
        requirements = BusinessRequirements(
            content="Hi"  # Too short
        )
        
        # Act
        result = await orchestrator.validate_requirements(requirements)
        
        # Assert
        assert result is False  # Should be invalid based on content