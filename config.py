"""
Configuration for FastMPC MCP Server - CORRETTO per Fly.io
"""
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # Server Configuration - IMPORTANTE: 8080 per Fly.io
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8080))  # ← CAMBIA 8000 a 8080
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # MCP Server URL
    MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'https://test-mcp-prodv2.fly.dev')
    
    # FastAPI Server URL
    FASTAPI_SERVER_URL = os.getenv('FASTAPI_SERVER_URL', 'https://test-mcp-prodv2.fly.dev')
    
    # FastMPC Configuration
    FASTMPC_ENABLED = True
    FASTMPC_ENDPOINT = '/tools'
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # CORS
    _allowed_origins = os.getenv('ALLOWED_ORIGINS', None)
    if _allowed_origins:
        ALLOWED_ORIGINS = _allowed_origins.split(',')
    else:
        ALLOWED_ORIGINS = [
            FASTAPI_SERVER_URL, 
            'https://test-mcp-prodv2.fly.dev',
            'http://localhost:3000',
            'http://127.0.0.1:3000'
        ]
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Example usage:
if __name__ == "__main__":
    print("Current Configuration:")
    print(json.dumps(Config.to_dict(), indent=2))
