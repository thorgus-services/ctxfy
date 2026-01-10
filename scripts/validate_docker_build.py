#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path

def validate_docker_requirements():
    print("Validating Docker image requirements...")
    
    # Check that required modules can be imported
    try:
        import fastapi
        import uvicorn
        import fastmcp
        import pydantic_settings
        print("✅ All required Python packages are available")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        return False
    
    # Check that Dockerfile exists
    dockerfile_path = Path("Dockerfile")
    if dockerfile_path.exists():
        print("✅ Dockerfile exists")
    else:
        print("❌ Dockerfile does not exist")
        return False
    
    # Check that .dockerignore exists
    dockerignore_path = Path(".dockerignore")
    if dockerignore_path.exists():
        print("✅ .dockerignore exists")
    else:
        print("❌ .dockerignore does not exist")
        return False
    
    # Check that docker-compose.yml exists
    compose_path = Path("docker-compose.yml")
    if compose_path.exists():
        print("✅ docker-compose.yml exists")
    else:
        print("❌ docker-compose.yml does not exist")
        return False
    
    # Check that health check module exists
    health_module_path = Path("src/shell/utils/health_check.py")
    if health_module_path.exists():
        print("✅ Health check module exists")
    else:
        print("❌ Health check module does not exist")
        return False
    
    # Check that app.py has been updated with health check functionality
    with open("src/app.py", "r") as f:
        app_content = f.read()
        if "run_both_servers" in app_content and "health_thread" in app_content:
            print("✅ App module updated with health check functionality")
        else:
            print("❌ App module not updated with health check functionality")
            return False
    
    print("\n🎉 All Docker image requirements validated successfully!")
    return True

if __name__ == "__main__":
    success = validate_docker_requirements()
    sys.exit(0 if success else 1)