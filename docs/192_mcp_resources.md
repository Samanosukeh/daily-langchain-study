```markdown
# MCP Resources: Expor Arquivos e Dados via Servidor

## Visão Geral

O **Model Context Protocol (MCP)** permite expor recursos (arquivos, dados, APIs) de forma estruturada para que clientes (como LLMs ou aplicações) possam consumi-los. Neste guia, abordamos como expor arquivos e dados via um servidor MCP.

---

## 1. Estrutura Básica de um Servidor MCP

Um servidor MCP é um aplicativo Python que implementa a interface `ServerInterface` do `mcp`. Para expor recursos, você deve:

1. **Definir os recursos** (arquivos, dados, etc.).
2. **Implementar métodos para listar e ler os recursos**.
3. **Configurar o servidor para expor esses recursos**.

### Exemplo Mínimo

```python
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server import ServerInterface
from mcp.types import Resource, ResourceTemplate
from typing import List, Optional
import json

# Criar instância do servidor
server = Server("meu-servidor-mcp")

# Implementar a interface do servidor
class MyServer(ServerInterface):
    async def list_resources(self) -> List[Resource]:
        # Definir recursos estáticos (exemplo: arquivo JSON)
        return [
            Resource(
                uri="file:///dados/usuarios.json",
                name="Usuários",
                mimeType="application/json",
                description="Lista de usuários no sistema."
            )
        ]

    async def read_resource(self, uri: str) -> str:
        # Lógica para ler o recurso com base no URI
        if uri == "file:///dados/usuarios.json":
            dados = {"usuarios": [{"id": 1, "nome": "Alice"}, {"id": 2, "nome": "Bob"}]}
            return json.dumps(dados)
        raise ValueError(f"Recurso não encontrado: {uri}")

# Registrar a implementação
server._server_interface = MyServer()

# Inicializar o servidor
async def main():
    await server.run(
        transport="stdio",  # Ou "http" para HTTP
        options=InitializationOptions(
            server_name="meu-servidor-mcp",
            server_version="0.1.0",
        )
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## 2. Expor Arquivos Dinamicamente

Para expor arquivos de um diretório dinamicamente, use `ResourceTemplate`:

```python
from pathlib import Path

class MyServer(ServerInterface):
    def __init__(self, diretorio: str):
        self.diretorio = Path(diretorio)

    async def list_resources(self) -> List[Resource]:
        recursos = []
        for arquivo in self.diretorio.glob("*.json"):
            uri = f"file://{arquivo.absolute()}"
            recursos.append(
                Resource(
                    uri=uri,
                    name=arquivo.name,
                    mimeType="application/json",
                    description=f"Arquivo JSON: {arquivo.name}"
                )
            )
        return recursos

    async def read_resource(self, uri: str) -> str:
        arquivo = Path(uri.replace("file://", ""))
        if arquivo.exists():
            return arquivo.read_text()
        raise ValueError(f"Arquivo não encontrado: {uri}")
```

---

## 3. Expor Dados de uma API Externa

Para expor dados de uma API (ex: REST, GraphQL), implemente a lógica de requisição:

```python
import httpx

class MyServer(ServerInterface):
    async def list_resources(self) -> List[Resource]:
        return [
            Resource(
                uri="api://posts",
                name="Posts da API",
                mimeType="application/json",
                description="Posts obtidos de uma API externa."
            )
        ]

    async def read_resource(self, uri: str) -> str:
        if uri == "api://posts":
            async with httpx.AsyncClient() as client:
                response = await client.get("https://jsonplaceholder.typicode.com/posts")
                return response.text
        raise ValueError(f"Recurso não encontrado: {uri}")
```

---

## 4. Configurar o Servidor para HTTP

Para expor o servidor via HTTP (ex: para uso com um cliente web):

```python
from mcp.server import Server
from mcp.server.fastapi import app

server = Server("meu-servidor-mcp")
server._server_interface = MyServer()

# Adicionar rotas FastAPI
app.mount("/mcp", server.app)