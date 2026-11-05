```python
# server.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.streamable_http import StreamableHTTPServerTransport
import uvicorn

app = FastAPI()
mcp_server = Server("MeuServidorMCP")

# Configuração inicial do servidor MCP
@mcp_server.initialize()
async def initialize_server():
    return InitializationOptions(
        server_name="MeuServidorMCP",
        server_version="0.1.0",
        capabilities={}
    )

# Exemplo de ferramenta MCP
@mcp_server.list_tools()
async def list_tools():
    return [
        {
            "name": "get_sistema_info",
            "description": "Retorna informações sobre o sistema operacional",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
    ]

# Implementação da ferramenta
@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_sistema_info":
        import platform
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Sistema: {platform.system()}\n"
                           f"Versão: {platform.version()}\n"
                           f"Arquitetura: {platform.machine()}"
                }
            ]
        }
    raise ValueError(f"Ferramenta desconhecida: {name}")

# Transport HTTP Streamable
transport = StreamableHTTPServerTransport(app, "/mcp")

# Endpoint principal
@app.get("/mcp")
async def handle_mcp():
    return await transport.handle_streamable_http_request()

# Endpoint para streaming
@app.post("/mcp")
async def handle_mcp_post():
    return await transport.handle_streamable_http_request()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```