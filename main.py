#!/usr/bin/env python3
"""
Main application entry point for MCP Server
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Config

app = FastAPI(
    title="Fly MCP Server",
    description="Flyio MCP Test Server",
    version="0.2"
)

# Configurazione CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["System"])
async def health_check():
    """Endpoint per il controllo dello stato del server"""
    return {
        "status": "ok",
        "service": "MCP Server",
        "version": "1.0.0"
    }

@app.get("/tools", tags=["MCP"])
async def list_available_tools():
    """Elenco dei tool MCP disponibili"""
    return {
        "tools": [
            "get_server_info",
            "calculate_operation",
            "format_text",
            "get_system_status"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Starting MCP Server on http://{Config.HOST}:{Config.PORT}")
    print(f"🔧 Debug mode: {'ON' if Config.DEBUG else 'OFF'}")
    print(f"⚡ FastMPC Enabled: {Config.FASTMPC_ENABLED}")
    
    if Config.FASTMPC_ENABLED:
        print(f"🔌 FastMPC Endpoint: {Config.FASTMPC_ENDPOINT}")
    
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level=Config.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    run_server()
