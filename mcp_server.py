from fastmcp import FastMCP
import asyncio
from datetime import datetime
import uvicorn
from fastapi import FastAPI

# Crea server MCP
mcp = FastMCP("FlyMCP-Server")

@mcp.tool()
async def get_server_info():
    """Restituisce informazioni sul server MCP"""
    return {
        "server_name": "FlyMCP-Server",
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "location": "Fly.io Frankfurt"
    }

@mcp.tool()
async def calculate_operation(operation: str, numbers: list):
    """Esegue operazioni matematiche"""
    if operation == "sum":
        result = sum(numbers)
    elif operation == "average":
        result = sum(numbers) / len(numbers)
    elif operation == "max":
        result = max(numbers)
    elif operation == "min":
        result = min(numbers)
    else:
        return {"error": "Operazione non supportata"}
    
    return {
        "operation": operation,
        "numbers": numbers,
        "result": result,
        "timestamp": datetime.now().isoformat()
    }

@mcp.tool()
async def format_text(text: str, style: str = "normal"):
    """Formatta il testo in diversi stili"""
    styles = {
        "uppercase": text.upper(),
        "lowercase": text.lower(),
        "title": text.title(),
        "reverse": text[::-1]
    }
    
    formatted = styles.get(style, text)
    
    return {
        "original": text,
        "formatted": formatted,
        "style": style,
        "length": len(text),
        "timestamp": datetime.now().isoformat()
    }

@mcp.tool()
async def get_system_status():
    """Restituisce lo stato del sistema"""
    import psutil
    import os
    
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("🚀 FlyMCP Server starting on stdio transport...")
    print("📍 Server ready for MCP clients")
    mcp.run(transport="stdio")
