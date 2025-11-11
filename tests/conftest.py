"""Pytest configuration file for async testing."""

# Ensure pytest-asyncio is properly configured

# Register the asyncio marker
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "asyncio: mark test as async test"
    )