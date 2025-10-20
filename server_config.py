"""
Configuration for FastMPC MCP Server
"""
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8080))
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # FastMPC Configuration (disabilitato - pacchetto non disponibile)
    FASTMPC_ENABLED = True
    FASTMPC_ENDPOINT = '/tools'
    
    # Nota: Il pacchetto fastmcp non è disponibile su PyPI.
    # Se necessario, installalo manualmente o specifica il percorso del pacchetto locale.
    # Esempio: pip install -e /percorso/al/pacchetto/fastmcp
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def to_dict(cls):
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'debug': cls.DEBUG,
            'fastmpc_enabled': cls.FASTMPC_ENABLED,
            'fastmpc_endpoint': cls.FASTMPC_ENDPOINT,
            'log_level': cls.LOG_LEVEL
        }

# Example usage:
if __name__ == "__main__":
    print("Current Configuration:")
    print(json.dumps(Config.to_dict(), indent=2))
