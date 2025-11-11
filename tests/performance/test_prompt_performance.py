import asyncio
import time

from src.adapters.template_engine.template_renderer import TemplateRenderer
from src.core.models.prompt_models import PromptTemplate
from src.core.models.variable_models import Variable


def test_prompt_execution_performance():
    """Performance test to ensure prompt execution meets <200ms requirement"""
    # Create a template
    variables = (Variable("name", "string"), Variable("value", "number"))
    template = PromptTemplate(
        template_id="perf.test",
        template_content="Hello {name}, your value is {value}",
        variables=variables,
        description="Performance test template",
        model_name="gpt-4o"
    )
    
    # Execute prompt multiple times and measure performance
    times = []
    iterations = 100
    
    for _ in range(iterations):
        start = time.time()
        
        # Execute the prompt operation
        result = TemplateRenderer.render_template(
            template, 
            {"name": "TestUser", "value": 42}
        )
        
        end = time.time()
        times.append((end - start) * 1000)  # Convert to milliseconds
        
        # Verify the result is correct
        assert result == "Hello TestUser, your value is 42"
    
    # Calculate p95 (95th percentile) time
    times.sort()
    p95_index = int(0.95 * len(times))
    p95_time = times[p95_index]
    
    # Verify performance requirements
    assert p95_time < 200.0, f"p95 response time {p95_time:.2f}ms exceeds 200ms requirement"
    assert max(times) < 500.0, f"Max response time {max(times):.2f}ms exceeds 500ms threshold"


def test_variable_substitution_performance():
    """Performance test for variable substitution with complex templates"""
    # Create a more complex template
    variables = tuple(Variable(f"var{i}", "string") for i in range(10))
    template_content = "Test: {var0}, {var1}, {var2}, {var3}, {var4}, {var5}, {var6}, {var7}, {var8}, {var9}"
    
    template = PromptTemplate(
        template_id="perf.complex",
        template_content=template_content,
        variables=variables,
        description="Complex template for performance testing",
        model_name="gpt-4o"
    )
    
    # Prepare variables for substitution
    test_vars = {f"var{i}": f"value_{i}" for i in range(10)}
    
    # Execute substitution multiple times
    times = []
    iterations = 50
    
    for _ in range(iterations):
        start = time.time()
        
        result = TemplateRenderer.render_template(template, test_vars)
        
        end = time.time()
        times.append((end - start) * 1000)
        
        # Verify result
        expected = "Test: value_0, value_1, value_2, value_3, value_4, value_5, value_6, value_7, value_8, value_9"
        assert result == expected
    
    # Calculate p95 time
    times.sort()
    p95_index = int(0.95 * len(times))
    p95_time = times[p95_index]
    
    assert p95_time < 200.0, f"Complex substitution p95 time {p95_time:.2f}ms exceeds 200ms requirement"


def test_concurrent_prompt_execution():
    """Test performance under concurrent execution"""
    # Create templates
    templates = []
    for i in range(5):
        variables = (Variable("id", "string"),)
        template = PromptTemplate(
            template_id=f"concurrent.test.{i}",
            template_content=f"Template {i}: {{id}}",
            variables=variables,
            description=f"Concurrent test template {i}",
            model_name="gpt-4o"
        )
        templates.append(template)
    
    # Execute concurrently using asyncio
    async def execute_single_prompt(template, idx):
        start = time.time()
        result = TemplateRenderer.render_template(template, {"id": f"item_{idx}"})
        end = time.time()
        return (end - start) * 1000, result  # time in ms
    
    async def run_concurrent_test():
        tasks = [execute_single_prompt(templates[i], i) for i in range(5)]
        results = await asyncio.gather(*tasks)
        return results
    
    # Run the concurrent test
    results = asyncio.run(run_concurrent_test())
    
    times = [result[0] for result in results]
    outputs = [result[1] for result in results]
    
    # Verify outputs
    expected_outputs = [f"Template {i}: item_{i}" for i in range(5)]
    assert outputs == expected_outputs
    
    # Check performance
    p95_index = int(0.95 * len(times))
    p95_time = sorted(times)[p95_index] if times else 0
    
    # For concurrent execution, allow slightly higher threshold due to system overhead
    assert p95_time < 500.0, f"Concurrent p95 time {p95_time:.2f}ms exceeds 500ms requirement"