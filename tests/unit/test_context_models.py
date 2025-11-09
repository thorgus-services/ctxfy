"""Unit tests for context models."""

from datetime import datetime
from decimal import Decimal

import pytest

from src.core.exceptions import ValidationError
from src.core.models.context_models import (
    ContextGenerationRequest,
    ContextGenerationResponse,
    ContextLayer,
    ContextStack,
    ContextStackMetadata,
)


class TestContextLayer:
    """Test cases for ContextLayer value object."""
    
    def test_context_layer_creation_with_valid_data(self):
        """Test creating a ContextLayer with valid data."""
        layer = ContextLayer(
            name="test",
            description="A test layer",
            specifications={"key": "value"},
            dependencies=["dep1", "dep2"]
        )
        
        assert layer.name == "test"
        assert layer.description == "A test layer"
        assert layer.specifications == {"key": "value"}
        assert layer.dependencies == ["dep1", "dep2"]
    
    def test_context_layer_creation_fails_with_empty_name(self):
        """Test that creating a ContextLayer with empty name raises ValidationError."""
        with pytest.raises(ValidationError, match="name cannot be empty"):
            ContextLayer(
                name="",
                description="A test layer"
            )
    
    def test_context_layer_creation_fails_with_empty_description(self):
        """Test that creating a ContextLayer with empty description raises ValidationError."""
        with pytest.raises(ValidationError, match="description cannot be empty"):
            ContextLayer(
                name="test",
                description=""
            )
    
    def test_add_dependency_creates_new_instance(self):
        """Test that add_dependency returns a new ContextLayer instance."""
        layer1 = ContextLayer(
            name="test",
            description="A test layer"
        )
        
        layer2 = layer1.add_dependency("new_dep")
        
        assert layer1 is not layer2
        assert layer1.dependencies == []
        assert layer2.dependencies == ["new_dep"]
    
    def test_with_specification_creates_new_instance(self):
        """Test that with_specification returns a new ContextLayer instance."""
        layer1 = ContextLayer(
            name="test",
            description="A test layer"
        )
        
        layer2 = layer1.with_specification("new_key", "new_value")
        
        assert layer1 is not layer2
        assert layer1.specifications == {}
        assert layer2.specifications == {"new_key": "new_value"}


class TestContextStackMetadata:
    """Test cases for ContextStackMetadata value object."""
    
    def test_metadata_creation_with_valid_data(self):
        """Test creating ContextStackMetadata with valid data."""
        metadata = ContextStackMetadata(
            version="1.0.0",
            creation_date=datetime.now(),
            author="Test Author",
            domain="Test Domain",
            task_type="Test Task"
        )
        
        assert metadata.version == "1.0.0"
        assert metadata.author == "Test Author"
        assert metadata.domain == "Test Domain"
        assert metadata.task_type == "Test Task"
    
    def test_metadata_creation_fails_with_empty_version(self):
        """Test that creating metadata with empty version raises ValidationError."""
        with pytest.raises(ValidationError, match="version cannot be empty"):
            ContextStackMetadata(
                version="",
                creation_date=datetime.now(),
                author="Test Author",
                domain="Test Domain",
                task_type="Test Task"
            )
    
    def test_metadata_creation_fails_with_empty_author(self):
        """Test that creating metadata with empty author raises ValidationError."""
        with pytest.raises(ValidationError, match="author cannot be empty"):
            ContextStackMetadata(
                version="1.0.0",
                creation_date=datetime.now(),
                author="",
                domain="Test Domain",
                task_type="Test Task"
            )
    
    def test_metadata_creation_fails_with_empty_domain(self):
        """Test that creating metadata with empty domain raises ValidationError."""
        with pytest.raises(ValidationError, match="domain cannot be empty"):
            ContextStackMetadata(
                version="1.0.0",
                creation_date=datetime.now(),
                author="Test Author",
                domain="",
                task_type="Test Task"
            )
    
    def test_metadata_creation_fails_with_empty_task_type(self):
        """Test that creating metadata with empty task_type raises ValidationError."""
        with pytest.raises(ValidationError, match="task_type cannot be empty"):
            ContextStackMetadata(
                version="1.0.0",
                creation_date=datetime.now(),
                author="Test Author",
                domain="Test Domain",
                task_type=""
            )


class TestContextStack:
    """Test cases for ContextStack value object."""
    
    @pytest.fixture
    def valid_layers(self):
        """Fixture providing valid context layers."""
        system_layer = ContextLayer(
            name="system",
            description="System layer"
        )
        domain_layer = ContextLayer(
            name="domain",
            description="Domain layer"
        )
        task_layer = ContextLayer(
            name="task",
            description="Task layer"
        )
        return system_layer, domain_layer, task_layer
    
    def test_context_stack_creation_with_valid_layers(self, valid_layers):
        """Test creating ContextStack with valid layers."""
        system_layer, domain_layer, task_layer = valid_layers
        metadata = ContextStackMetadata(
            version="1.0.0",
            creation_date=datetime.now(),
            author="Test Author",
            domain="Test Domain",
            task_type="Test Task"
        )
        
        stack = ContextStack(
            system_layer=system_layer,
            domain_layer=domain_layer,
            task_layer=task_layer,
            metadata=metadata
        )
        
        assert stack.system_layer == system_layer
        assert stack.domain_layer == domain_layer
        assert stack.task_layer == task_layer
        assert stack.metadata == metadata
        assert stack.additional_layers == []
    
    def test_context_stack_fails_with_wrong_system_layer_name(self):
        """Test that ContextStack validation fails with wrong system layer name."""
        system_layer = ContextLayer(
            name="not_system",  # Should be "system"
            description="System layer"
        )
        domain_layer = ContextLayer(
            name="domain",
            description="Domain layer"
        )
        task_layer = ContextLayer(
            name="task",
            description="Task layer"
        )
        metadata = ContextStackMetadata(
            version="1.0.0",
            creation_date=datetime.now(),
            author="Test Author",
            domain="Test Domain",
            task_type="Test Task"
        )
        
        with pytest.raises(ValidationError, match="System layer name must be 'system'"):
            ContextStack(
                system_layer=system_layer,
                domain_layer=domain_layer,
                task_layer=task_layer,
                metadata=metadata
            )
    
    def test_context_stack_fails_with_wrong_domain_layer_name(self):
        """Test that ContextStack validation fails with wrong domain layer name."""
        system_layer = ContextLayer(
            name="system",
            description="System layer"
        )
        domain_layer = ContextLayer(
            name="not_domain",  # Should be "domain"
            description="Domain layer"
        )
        task_layer = ContextLayer(
            name="task",
            description="Task layer"
        )
        metadata = ContextStackMetadata(
            version="1.0.0",
            creation_date=datetime.now(),
            author="Test Author",
            domain="Test Domain",
            task_type="Test Task"
        )
        
        with pytest.raises(ValidationError, match="Domain layer name must be 'domain'"):
            ContextStack(
                system_layer=system_layer,
                domain_layer=domain_layer,
                task_layer=task_layer,
                metadata=metadata
            )
    
    def test_context_stack_fails_with_wrong_task_layer_name(self):
        """Test that ContextStack validation fails with wrong task layer name."""
        system_layer = ContextLayer(
            name="system",
            description="System layer"
        )
        domain_layer = ContextLayer(
            name="domain",
            description="Domain layer"
        )
        task_layer = ContextLayer(
            name="not_task",  # Should be "task"
            description="Task layer"
        )
        metadata = ContextStackMetadata(
            version="1.0.0",
            creation_date=datetime.now(),
            author="Test Author",
            domain="Test Domain",
            task_type="Test Task"
        )
        
        with pytest.raises(ValidationError, match="Task layer name must be 'task'"):
            ContextStack(
                system_layer=system_layer,
                domain_layer=domain_layer,
                task_layer=task_layer,
                metadata=metadata
            )
    
    def test_add_additional_layer_creates_new_instance(self, valid_layers):
        """Test that add_additional_layer returns a new ContextStack instance."""
        system_layer, domain_layer, task_layer = valid_layers
        metadata = ContextStackMetadata(
            version="1.0.0",
            creation_date=datetime.now(),
            author="Test Author",
            domain="Test Domain",
            task_type="Test Task"
        )
        
        stack1 = ContextStack(
            system_layer=system_layer,
            domain_layer=domain_layer,
            task_layer=task_layer,
            metadata=metadata
        )
        
        new_layer = ContextLayer(
            name="extra",
            description="Extra layer"
        )
        stack2 = stack1.add_additional_layer(new_layer)
        
        assert stack1 is not stack2
        assert len(stack1.additional_layers) == 0
        assert len(stack2.additional_layers) == 1
        assert stack2.additional_layers[0] == new_layer
    
    def test_get_all_layers_includes_all_layers(self, valid_layers):
        """Test that get_all_layers returns all layers including additional ones."""
        system_layer, domain_layer, task_layer = valid_layers
        metadata = ContextStackMetadata(
            version="1.0.0",
            creation_date=datetime.now(),
            author="Test Author",
            domain="Test Domain",
            task_type="Test Task"
        )
        
        stack = ContextStack(
            system_layer=system_layer,
            domain_layer=domain_layer,
            task_layer=task_layer,
            metadata=metadata
        )
        
        new_layer = ContextLayer(
            name="extra",
            description="Extra layer"
        )
        stack_with_extra = stack.add_additional_layer(new_layer)
        
        all_layers = stack_with_extra.get_all_layers()
        
        assert len(all_layers) == 4  # system, domain, task, extra
        assert system_layer in all_layers
        assert domain_layer in all_layers
        assert task_layer in all_layers
        assert new_layer in all_layers


class TestContextGenerationRequest:
    """Test cases for ContextGenerationRequest value object."""
    
    def test_request_creation_with_valid_data(self):
        """Test creating ContextGenerationRequest with valid data."""
        request = ContextGenerationRequest(
            feature_description="Test feature",
            target_technologies=["Python", "FastAPI"],
            custom_rules=["Rule 1", "Rule 2"]
        )
        
        assert request.feature_description == "Test feature"
        assert request.target_technologies == ["Python", "FastAPI"]
        assert request.custom_rules == ["Rule 1", "Rule 2"]
    
    def test_request_creation_fails_with_empty_feature_description(self):
        """Test that creating request with empty feature description raises ValidationError."""
        with pytest.raises(ValidationError, match="Feature description cannot be empty"):
            ContextGenerationRequest(
                feature_description="",
                target_technologies=["Python", "FastAPI"]
            )


class TestContextGenerationResponse:
    """Test cases for ContextGenerationResponse value object."""
    
    def test_response_creation_with_success(self):
        """Test creating ContextGenerationResponse for success case."""
        # Need to create a minimal context stack for this test
        system_layer = ContextLayer(name="system", description="System layer")
        domain_layer = ContextLayer(name="domain", description="Domain layer")
        task_layer = ContextLayer(name="task", description="Task layer")
        metadata = ContextStackMetadata(
            version="1.0.0",
            creation_date=datetime.now(),
            author="Test",
            domain="Test",
            task_type="Test"
        )
        context_stack = ContextStack(
            system_layer=system_layer,
            domain_layer=domain_layer,
            task_layer=task_layer,
            metadata=metadata
        )
        
        response = ContextGenerationResponse(
            success=True,
            context_stack=context_stack,
            error_message=None,
            processing_time=Decimal("0.1")
        )
        
        assert response.success is True
        assert response.context_stack is not None
        assert response.error_message is None
        assert response.processing_time == Decimal("0.1")
    
    def test_response_creation_with_error(self):
        """Test creating ContextGenerationResponse for error case."""
        response = ContextGenerationResponse(
            success=False,
            context_stack=None,
            error_message="An error occurred",
            processing_time=Decimal("0.2")
        )
        
        assert response.success is False
        assert response.context_stack is None
        assert response.error_message == "An error occurred"
        assert response.processing_time == Decimal("0.2")
    
    def test_response_fails_when_success_with_no_context_stack(self):
        """Test that creating a successful response without context stack raises ValidationError."""
        with pytest.raises(ValidationError, match="Success response must include context stack"):
            ContextGenerationResponse(
                success=True,
                context_stack=None,
                error_message=None,
                processing_time=Decimal("0.1")
            )
    
    def test_response_fails_when_error_with_context_stack(self):
        """Test that creating an error response with context stack raises ValidationError."""
        # Create a minimal context stack for this test
        system_layer = ContextLayer(name="system", description="System layer")
        domain_layer = ContextLayer(name="domain", description="Domain layer")
        task_layer = ContextLayer(name="task", description="Task layer")
        metadata = ContextStackMetadata(
            version="1.0.0",
            creation_date=datetime.now(),
            author="Test",
            domain="Test",
            task_type="Test"
        )
        context_stack = ContextStack(
            system_layer=system_layer,
            domain_layer=domain_layer,
            task_layer=task_layer,
            metadata=metadata
        )
        
        with pytest.raises(ValidationError, match="Error response cannot include context stack"):
            ContextGenerationResponse(
                success=False,
                context_stack=context_stack,
                error_message="An error",
                processing_time=Decimal("0.1")
            )
    
    def test_response_fails_when_error_without_error_message(self):
        """Test that creating an error response without error message raises ValidationError."""
        with pytest.raises(ValidationError, match="Error response must include error message"):
            ContextGenerationResponse(
                success=False,
                context_stack=None,
                error_message=None,
                processing_time=Decimal("0.1")
            )