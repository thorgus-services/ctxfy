from unittest.mock import AsyncMock

import pytest

from src.adapters.context.business_requirements_adapter import (
    BusinessRequirementsAdapter,
)
from src.core.models.business_requirements_models import (
    BusinessRequirementConfig,
    BusinessRequirements,
    TechnicalSpecification,
)


class TestBusinessRequirementsAdapter:
    """Test cases for BusinessRequirementsAdapter"""
    
    @pytest.fixture
    def mock_ctx(self):
        """Create a mock context object"""
        ctx = AsyncMock()
        ctx.sample = AsyncMock()
        ctx.error = AsyncMock()
        ctx.log = AsyncMock()
        return ctx
    
    @pytest.fixture
    def adapter(self, mock_ctx):
        """Create a BusinessRequirementsAdapter instance"""
        return BusinessRequirementsAdapter(ctx=mock_ctx)
    
    @pytest.mark.asyncio
    async def test_translate_business_requirements_success(self, adapter, mock_ctx):
        """Test successful business requirements translation"""
        # Arrange
        config = BusinessRequirementConfig(
            requirements_text="Create a user management system",
            output_directory="ctxfy/specifications"
        )
        
        # Mock LLM response
        mock_ctx.sample.side_effect = [
            # First call: LLM translation
            {"content": "# Technical Specification\n\nSystem for managing users..."},
            # Second call: File write operation
            {"success": True}
        ]
        
        # Act
        result = await adapter.translate_business_requirements(config)
        
        # Assert
        assert result.success is True
        assert result.specification is not None
        assert "# Technical Specification" in result.specification.content
        assert mock_ctx.sample.call_count == 2  # LLM call + file write
    
    @pytest.mark.asyncio
    async def test_translate_business_requirements_with_string_llm_response(self, adapter, mock_ctx):
        """Test translation with string response from LLM"""
        # Arrange
        config = BusinessRequirementConfig(
            requirements_text="Create an API endpoint",
            output_directory="ctxfy/specifications"
        )
        
        # Mock LLM response as string and file write success
        mock_ctx.sample.side_effect = [
            "# API Specification\n\nEndpoint for user management...",  # LLM response
            {"success": True}  # File write success
        ]
        
        # Act
        result = await adapter.translate_business_requirements(config)
        
        # Assert
        assert result.success is True
        assert result.specification is not None
        assert "# API Specification" in result.specification.content
    
    @pytest.mark.asyncio
    async def test_translate_business_requirements_security_failure(self, adapter, mock_ctx):
        """Test translation with security validation failure"""
        # Arrange
        config = BusinessRequirementConfig(
            requirements_text="Execute eval('dangerous code')",
            output_directory="ctxfy/specifications"
        )
        
        # Act
        result = await adapter.translate_business_requirements(config)
        
        # Assert
        assert result.success is False
        assert len(result.errors) > 0
        assert any("malicious content detected" in str(error).lower() for error in result.errors)
        mock_ctx.sample.assert_not_called()  # Should not reach LLM call due to security check
    
    @pytest.mark.asyncio
    async def test_translate_business_requirements_file_write_failure(self, adapter, mock_ctx):
        """Test translation when file write fails"""
        # Arrange
        config = BusinessRequirementConfig(
            requirements_text="Create a user management system",
            output_directory="ctxfy/specifications"
        )
        
        # Mock LLM response and file write failure
        mock_ctx.sample.side_effect = [
            {"content": "# Technical Specification\n\nSystem for managing users..."},  # LLM response
            {"success": False}  # File write failure
        ]
        
        # Act
        result = await adapter.translate_business_requirements(config)
        
        # Assert
        assert result.success is False
        assert "Failed to store technical specification" in result.errors
    
    @pytest.mark.asyncio
    async def test_generate_technical_specification_success(self, adapter, mock_ctx):
        """Test successful technical specification generation"""
        # Arrange
        requirements = BusinessRequirements(
            content="Create a user management system"
        )
        
        # Mock LLM response
        mock_ctx.sample.return_value = {"content": "# Generated Specification\n\nDetails..."}
        
        # Act
        result = await adapter.generate_technical_specification(requirements)
        
        # Assert
        assert result.content == "# Generated Specification\n\nDetails..."
        assert result.format == "SPEC"
        assert result.source_requirements_id == requirements.id
        mock_ctx.sample.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_technical_specification_security_failure(self, adapter, mock_ctx):
        """Test specification generation with security validation failure"""
        # Arrange
        requirements = BusinessRequirements(
            content="Execute os.system('rm -rf /')"
        )
        
        # Mock LLM response with dangerous content
        mock_ctx.sample.return_value = {"content": "exec('dangerous code')"}
        
        # Act
        result = await adapter.generate_technical_specification(requirements)
        
        # Assert
        assert "Specification rejected for security reasons" in result.content
        assert result.format == "SPEC"
        mock_ctx.sample.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_store_technical_specification_success(self, adapter, mock_ctx):
        """Test successful storage of technical specification"""
        # Arrange
        spec = TechnicalSpecification(
            content="# Test Specification",
            format="SPEC"
        )
        
        # Mock file write success
        mock_ctx.sample.return_value = {"success": True}
        
        # Act
        result = await adapter.store_technical_specification(spec, "ctxfy/specifications")
        
        # Assert
        assert result is True
        mock_ctx.sample.assert_called_once()
        # Check that the call contains the expected path with secure path building
        call_args = mock_ctx.sample.call_args[0][0]
        assert "action" in call_args
        assert call_args["action"] == "write_file"
        assert "ctxfy/specifications/spec_" in call_args["path"]
        assert call_args["content"] == "# Test Specification"
    
    @pytest.mark.asyncio
    async def test_store_technical_specification_path_traversal_failure(self, adapter, mock_ctx):
        """Test specification storage with path traversal attempt"""
        # Arrange
        spec = TechnicalSpecification(
            content="# Test Specification",
            format="SPEC"
        )
        
        # Act
        result = await adapter.store_technical_specification(spec, "../../../etc")
        
        # Assert
        assert result is False
        mock_ctx.error.assert_called_once()
        assert "Failed to build secure output path" in str(mock_ctx.error.call_args[0][0])
        mock_ctx.sample.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_store_technical_specification_write_failure(self, adapter, mock_ctx):
        """Test specification storage with write failure"""
        # Arrange
        spec = TechnicalSpecification(
            content="# Test Specification",
            format="SPEC"
        )
        
        # Mock file write failure
        mock_ctx.sample.return_value = {"success": False}
        
        # Act
        result = await adapter.store_technical_specification(spec, "ctxfy/specifications")
        
        # Assert
        assert result is False
        mock_ctx.sample.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_translation_status(self, adapter, mock_ctx):
        """Test getting translation status"""
        # Act
        result = await adapter.get_translation_status("test-id")
        
        # Assert
        assert result.translation_id == "test-id"
        assert result.status == "completed"  # Based on implementation
        assert result.progress == 1.0
    
    @pytest.mark.asyncio
    async def test_validate_requirements_valid(self, adapter, mock_ctx):
        """Test validating valid requirements"""
        # Arrange
        requirements = BusinessRequirements(
            content="Valid business requirements with sufficient content for proper validation"
        )
        
        # Act
        result = await adapter.validate_requirements(requirements)
        
        # Assert
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    @pytest.mark.asyncio
    async def test_validate_requirements_invalid_content(self, adapter, mock_ctx):
        """Test validating requirements with invalid content"""
        # Arrange
        requirements = BusinessRequirements(
            content="Hi"  # Too short
        )
        
        # Act
        result = await adapter.validate_requirements(requirements)
        
        # Assert
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("content too short" in str(error).lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_validate_requirements_sensitive_content(self, adapter, mock_ctx):
        """Test validating requirements with sensitive content"""
        # Arrange
        requirements = BusinessRequirements(
            content="Store the password in plain text"
        )
        
        # Act
        result = await adapter.validate_requirements(requirements)
        
        # Assert
        assert result.is_valid is False
        assert len(result.errors) > 0
        assert any("sensitive information detected" in str(error).lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_list_translations(self, adapter, mock_ctx):
        """Test listing translations"""
        # Act
        result = await adapter.list_translations()
        
        # Assert
        assert result == ()
        mock_ctx.log.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_list_translations_with_limit(self, adapter, mock_ctx):
        """Test listing translations with custom limit"""
        # Act
        result = await adapter.list_translations(limit=5)
        
        # Assert
        assert result == ()
        assert "limit: 5" in str(mock_ctx.log.call_args[0][0])