
import pytest

from src.shell.utils.retry_utils import execute_async_with_retry, execute_with_retry


def test_execute_with_retry_success_on_first_attempt():
    """Test that execute_with_retry returns result immediately on success"""
    call_count = 0
    
    def successful_function():
        nonlocal call_count
        call_count += 1
        return "success"
    
    result = execute_with_retry(successful_function, max_retries=3)
    
    assert result == "success"
    assert call_count == 1


def test_execute_with_retry_eventual_success():
    """Test that execute_with_retry retries on failure and succeeds eventually"""
    call_count = 0
    
    def eventually_successful_function():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Failing on purpose")
        return "finally successful"
    
    result = execute_with_retry(eventually_successful_function, max_retries=5)
    
    assert result == "finally successful"
    assert call_count == 3


def test_execute_with_retry_fails_after_max_retries():
    """Test that execute_with_retry raises exception after max retries"""
    call_count = 0
    
    def always_failing_function():
        nonlocal call_count
        call_count += 1
        raise ValueError(f"Always fails - attempt {call_count}")
    
    with pytest.raises(ValueError):
        execute_with_retry(always_failing_function, max_retries=3)
    
    assert call_count == 3


@pytest.mark.asyncio
async def test_execute_async_with_retry_success_on_first_attempt():
    """Test that execute_async_with_retry returns result immediately on success"""
    call_count = 0
    
    async def successful_async_function():
        nonlocal call_count
        call_count += 1
        return "async success"
    
    result = await execute_async_with_retry(successful_async_function, max_retries=3)
    
    assert result == "async success"
    assert call_count == 1


@pytest.mark.asyncio
async def test_execute_async_with_retry_fails_after_max_retries():
    """Test that execute_async_with_retry raises exception after max retries"""
    call_count = 0
    
    async def always_failing_async_function():
        nonlocal call_count
        call_count += 1
        raise RuntimeError(f"Always fails async - attempt {call_count}")
    
    with pytest.raises(RuntimeError):
        await execute_async_with_retry(always_failing_async_function, max_retries=2)
    
    assert call_count == 2