from fastmcp import FastMCP
from datetime import datetime
import psutil
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json

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

# Health Check HTTP Server
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "FlyMCP-Server",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Disabilita logging HTTP
        pass

def start_http_server():
    """Avvia un semplice server HTTP per health checks"""
    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    print("🌐 HTTP Health Check server running on port 8080")
    server.serve_forever()

if __name__ == "__main__":
    print("🚀 Starting FlyMCP Server with HTTP health check...")
    
    # Avvia HTTP server in thread separato
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    # Avvia server MCP
    print("🔧 MCP Server ready for stdio connections")
    mcp.run(transport="stdio")
