from fastmcp import FastMCP
from datetime import datetime
import psutil
import uuid
from typing import Dict, Any

# Crea server MCP con gestione sessioni
class MCPServer(FastMCP):
    def __init__(self, name: str):
        super().__init__(name)
        self._sessions = {}  # Dizionario per tenere traccia delle sessioni

    async def handle_request(self, method: str, params: Dict[Any, Any] = None) -> Dict[Any, Any]:
        """Override del metodo handle_request per gestire initialize e sessioni"""
        if method == "initialize":
            session_id = str(uuid.uuid4())
            self._sessions[session_id] = {"created_at": datetime.now().isoformat()}
            
            return {
                "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                "sessionId": session_id,
                "capabilities": {
                    "experimental": {},
                    "prompts": {"listChanged": True},
                    "resources": {"subscribe": False, "listChanged": True},
                    "tools": {"listChanged": True}
                },
                "serverInfo": {
                    "name": self.name,
                    "version": "1.17.0"
                }
            }
        return await super().handle_request(method, params)

# Istanzia il server MCP personalizzato
mcp = MCPServer("FlyMCP-Server")

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
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("🚀 FlyMCP Server starting on SSE transport (port 8080)...")
    print("📍 MCP Tools available via SSE")
    print("🔧 Tools: get_server_info, calculate_operation, format_text, get_system_status")
    
    # Avvia server MCP con SSE e gestione sessioni
    mcp.run(transport="sse", port=8080, host="0.0.0.0", base_path="/sse")
