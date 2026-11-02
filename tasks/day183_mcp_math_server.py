```python
from fastmcp import FastMCP
from pydantic import BaseModel

# Inicializa o servidor MCP
mcp = FastMCP("Calculadora MCP")

# Define os modelos de entrada para as tools
class AddInput(BaseModel):
    a: float
    b: float

class MultiplyInput(BaseModel):
    a: float
    b: float

@mcp.tool()
def add(input: AddInput) -> float:
    """Soma dois números"""
    return input.a + input.b

@mcp.tool()
def multiply(input: MultiplyInput) -> float:
    """Multiplica dois números"""
    return input.a * input.b

# Executa o servidor
if __name__ == "__main__":
    mcp.run()
```