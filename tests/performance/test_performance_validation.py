import time

from src.adapters.template_engine.template_renderer import TemplateRenderer
from src.core.models.prompt_models import PromptTemplate
from src.core.models.variable_models import Variable
from src.core.use_cases.prompt_use_cases import substitute_variables


class TestPerformanceRequirements:
    """Tests for performance requirements (<200ms response time)."""

    def test_substitute_variables_performance(self):
        """Test that variable substitution performs under 200ms."""
        template = "Hello {name}, welcome to {place}! Your id is {id} and score is {score}."
        variables = {
            "name": "Alice",
            "place": "Wonderland", 
            "id": "12345",
            "score": 95.5
        }
        
        start_time = time.time()
        result = substitute_variables(template, variables)
        end_time = time.time()
        
        execution_time_ms = (end_time - start_time) * 1000
        assert execution_time_ms < 200, f"Variable substitution took {execution_time_ms:.2f}ms, which exceeds 200ms limit"
        
        # Verify result is correct
        assert "Alice" in result
        assert "Wonderland" in result

    def test_substitute_variables_performance_with_complex_template(self):
        """Test variable substitution performance with a more complex template."""
        template = """
        User Profile:
        Name: {name}
        Email: {email}
        Age: {age}
        Location: {location}
        Interests: {interests}
        Membership: {membership}
        Registration Date: {reg_date}
        Last Login: {last_login}
        Status: {status}
        """
        
        variables = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 32,
            "location": "New York, NY",
            "interests": "Technology, Sports, Reading",
            "membership": "Premium",
            "reg_date": "2023-01-15",
            "last_login": "2023-11-10",
            "status": "Active"
        }
        
        start_time = time.time()
        result = substitute_variables(template, variables)
        end_time = time.time()
        
        execution_time_ms = (end_time - start_time) * 1000
        assert execution_time_ms < 200, f"Complex variable substitution took {execution_time_ms:.2f}ms, which exceeds 200ms limit"
        assert "John Doe" in result

    def test_template_rendering_performance(self):
        """Test that template rendering performs under 200ms."""
        variables = (Variable("name", "string"), Variable("city", "string"))
        template = PromptTemplate(
            template_id="welcome-template",
            template_content="Hello {name}, welcome to {city}!",
            variables=variables,
            description="Welcome message template",
            model_name="gpt-4o"
        )
        
        start_time = time.time()
        result = TemplateRenderer.render_template(template, {"name": "Alice", "city": "Paris"})
        end_time = time.time()
        
        execution_time_ms = (end_time - start_time) * 1000
        assert execution_time_ms < 200, f"Template rendering took {execution_time_ms:.2f}ms, which exceeds 200ms limit"
        assert result == "Hello Alice, welcome to Paris!"

    def test_multiple_variable_substitutions_performance(self):
        """Test performance with multiple sequential substitutions."""
        template = "User: {name}, Score: {score}, Rank: {rank}"
        variables_list = [
            {"name": f"User{i}", "score": i*10, "rank": f"Rank{i%5}"} 
            for i in range(50)  # Test 50 substitutions
        ]
        
        start_time = time.time()
        for vars in variables_list:
            substitute_variables(template, vars)
        end_time = time.time()
        
        total_time_ms = (end_time - start_time) * 1000
        avg_time_per_substitution = total_time_ms / len(variables_list)
        
        assert avg_time_per_substitution < 200, f"Average substitution time was {avg_time_per_substitution:.2f}ms, which exceeds 200ms limit"
        assert total_time_ms < 5000, f"Total time for 50 substitutions was {total_time_ms:.2f}ms, which exceeds expected limits"

    def test_template_rendering_with_injection_check_performance(self):
        """Test that template rendering with injection prevention still performs under 200ms."""
        # Create template with many variables to test injection checks
        variables = tuple(Variable(f"var{i}", "string") for i in range(10))
        template_content = "Results: " + ", ".join([f"{{var{i}}}" for i in range(10)])
        
        template = PromptTemplate(
            template_id="multi-var-template",
            template_content=template_content,
            variables=variables,
            description="Template with multiple variables",
            model_name="gpt-4o"
        )
        
        test_variables = {f"var{i}": f"value{i}" for i in range(10)}
        
        start_time = time.time()
        result = TemplateRenderer.render_template(template, test_variables)
        end_time = time.time()
        
        execution_time_ms = (end_time - start_time) * 1000
        assert execution_time_ms < 200, f"Multi-var template rendering took {execution_time_ms:.2f}ms, which exceeds 200ms limit"
        
        # Verify all variables were substituted
        for i in range(10):
            assert f"value{i}" in result

    def test_substitute_variables_with_injection_validation_performance(self):
        """Test performance of injection validation."""
        # Test with safe variables (should be fast)
        template = "Hello {name}, your request {request_id} is processed."
        variables = {
            "name": "Alice",
            "request_id": "req-12345"
        }
        
        start_time = time.time()
        result = substitute_variables(template, variables)
        end_time = time.time()
        
        execution_time_ms = (end_time - start_time) * 1000
        assert execution_time_ms < 200, f"Injection-safe substitution took {execution_time_ms:.2f}ms, which exceeds 200ms limit"
        assert "Alice" in result