#!/usr/bin/env python3
"""
MCP Server Minimalista - Versione senza emoji
"""
import asyncio
import json
import sys
import subprocess
from fastapi import FastAPI, Request
import uvicorn

async def handle_mcp_protocol():
    """Minimal MCP server implementation"""
    # SENZA EMOJI - usa testo semplice
    print("MCP Server Started - Waiting for Claude connection...", file=sys.stderr)
    
    while True:
        try:
            # Legge da stdin (da Claude)
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            data = json.loads(line.strip())
            method = data.get("method")
            msg_id = data.get("id")
            
            print(f"Received: {method}", file=sys.stderr)
            
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {},
                            "resources": {}
                        },
                        "serverInfo": {
                            "name": "fly-mcp-server",
                            "version": "1.0.0"
                        }
                    }
                }
                print(json.dumps(response), flush=True)
                print("Initialized successfully", file=sys.stderr)
                
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "get_server_info",
                                "description": "Get server information and status",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            },
                            {
                                "name": "calculate_operation", 
                                "description": "Perform mathematical calculations",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "operation": {
                                            "type": "string",
                                            "description": "Math operation like '2+2'"
                                        }
                                    },
                                    "required": ["operation"]
                                }
                            },
                            {
                                "name": "format_text",
                                "description": "Format text in different styles",
                                "inputSchema": {
                                    "type": "object", 
                                    "properties": {
                                        "text": {"type": "string"},
                                        "style": {
                                            "type": "string",
                                            "enum": ["uppercase", "lowercase", "title"]
                                        }
                                    },
                                    "required": ["text", "style"]
                                }
                            },
                            {
                                "name": "check_remote_health",
                                "description": "Check remote server health",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "url": {
                                            "type": "string", 
                                            "default": "https://test-mcp-prodv1.fly.dev"
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
                print(json.dumps(response), flush=True)
                print("Tools list sent", file=sys.stderr)
                
            elif method == "tools/call":
                tool_name = data["params"]["name"]
                arguments = data["params"].get("arguments", {})
                
                print(f"Executing tool: {tool_name}", file=sys.stderr)
                
                if tool_name == "get_server_info":
                    result_text = json.dumps({
                        "server_name": "Fly MCP Server",
                        "version": "1.0.0", 
                        "status": "running",
                        "message": "Hello from MCP Server!"
                    }, indent=2)
                    
                elif tool_name == "calculate_operation":
                    operation = arguments.get("operation", "")
                    try:
                        result = eval(operation)
                        result_text = f"Calculation: {operation} = {result}"
                    except Exception as e:
                        result_text = f"Error: {e}"
                        
                elif tool_name == "format_text":
                    text = arguments.get("text", "")
                    style = arguments.get("style", "")
                    
                    if style == "uppercase":
                        result_text = text.upper()
                    elif style == "lowercase":
                        result_text = text.lower() 
                    elif style == "title":
                        result_text = text.title()
                    else:
                        result_text = text
                        
                elif tool_name == "check_remote_health":
                    url = arguments.get("url", "https://test-mcp-prodv1.fly.dev")
                    try:
                        import requests
                        response = requests.get(url, timeout=5)
                        result_text = f"URL: {url}\nStatus: {response.status_code}\nHealthy: {response.status_code == 200}"
                    except ImportError:
                        result_text = "requests library not available"
                    except Exception as e:
                        result_text = f"Error: {e}"
                        
                else:
                    result_text = f"Unknown tool: {tool_name}"
                
                response = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result_text
                            }
                        ]
                    }
                }
                print(json.dumps(response), flush=True)
                print(f"Tool {tool_name} executed", file=sys.stderr)
                
            elif method == "notifications/initialized":
                print("Client initialized", file=sys.stderr)
                continue
                
        except json.JSONDecodeError:
            print("Invalid JSON received", file=sys.stderr)
            continue
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            error_response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            }
            print(json.dumps(error_response), flush=True)

# Create FastAPI app
app = FastAPI()

@app.post("/mcp")
async def handle_mcp(request: Request):
    """Handle MCP protocol over HTTP"""
    try:
        data = await request.json()
        method = data.get("method")
        msg_id = data.get("id")
        
        print(f"Received: {method}", file=sys.stderr)
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {},
                        "resources": {}
                    },
                    "serverInfo": {
                        "name": "fly-mcp-server",
                        "version": "1.0.0"
                    }
                }
            }
        
        # Add other method handlers here
        
        return {"error": "Method not implemented"}
    except Exception as e:
        return {"error": str(e)}

def run_server():
    """Run the FastAPI server"""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )

if __name__ == "__main__":
    run_server()
