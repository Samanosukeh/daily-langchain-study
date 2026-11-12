```python
from mcp.server import Server
from mcp.server.models import InitializationOptions
import os

# Configuração do servidor MCP
server = Server("text-file-server")

@server.list_resources()
async def list_resources() -> list[dict]:
    """Lista recursos disponíveis (arquivos de texto)."""
    resources = []
    directory = "./text_files"  # Diretório onde os arquivos estão armazenados

    if not os.path.exists(directory):
        os.makedirs(directory)

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            resources.append({
                "uri": f"file://{filepath}",
                "name": filename,
                "description": f"Arquivo de texto: {filename}",
                "mimeType": "text/plain"
            })

    return resources

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Lê o conteúdo de um arquivo de texto."""
    try:
        with open(uri.replace("file://", ""), "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Erro ao ler arquivo: {str(e)}"

# Inicialização do servidor
if __name__ == "__main__":
    server.run(
        InitializationOptions(
            server_name="text-file-server",
            server_version="0.1.0",
        )
    )
```