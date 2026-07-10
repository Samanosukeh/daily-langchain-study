```python
import pytest
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

class InputSchema(BaseModel):
    campo_obrigatorio: str = Field(..., description="Campo obrigatório")
    campo_opcional: Optional[str] = Field(None, description="Campo opcional")

def test_structured_tool_valida_campo_obrigatorio():
    """Testa se a ferramenta estruturada valida corretamente campos obrigatórios."""
    def funcao_mock(campo_obrigatorio: str, campo_opcional: Optional[str] = None) -> str:
        return f"Recebido: {campo_obrigatorio}, {campo_opcional}"

    tool = StructuredTool.from_function(
        func=funcao_mock,
        name="test_tool",
        description="Ferramenta de teste",
        args_schema=InputSchema,
    )

    # Teste com campo obrigatório preenchido
    result = tool.run({"campo_obrigatorio": "valor1"})
    assert "Recebido: valor1, None" in result

    # Teste com campo obrigatório ausente (deve lançar ValidationError)
    with pytest.raises(Exception) as exc_info:
        tool.run({"campo_opcional": "valor_ignorado"})
    assert "campo_obrigatorio" in str(exc_info.value)

def test_structured_tool_valida_campo_opcional():
    """Testa se a ferramenta estruturada aceita campos opcionais."""
    def funcao_mock(campo_obrigatorio: str, campo_opcional: Optional[str] = None) -> str:
        return f"Recebido: {campo_obrigatorio}, {campo_opcional}"

    tool = StructuredTool.from_function(
        func=funcao_mock,
        name="test_tool",
        description="Ferramenta de teste",
        args_schema=InputSchema,
    )

    # Teste com campo opcional preenchido
    result = tool.run({"campo_obrigatorio": "valor1", "campo_opcional": "valor2"})
    assert "Recebido: valor1, valor2" in result

def test_structured_tool_valida_tipos():
    """Testa se a ferramenta estruturada valida tipos de dados."""
    def funcao_mock(campo_obrigatorio: str, campo_opcional: Optional[int] = None) -> str:
        return f"Recebido: {campo_obrigatorio}, {campo_opcional}"

    class InputSchemaTipado(BaseModel):
        campo_obrigatorio: str = Field(..., description="Campo obrigatório")
        campo_opcional: Optional[int] = Field(None, description="Campo opcional numérico")

    tool = StructuredTool.from_function(
        func=funcao_mock,
        name="test_tool",
        description="Ferramenta de teste",
        args_schema=InputSchemaTipado,
    )

    # Teste com tipo correto
    result = tool.run({"campo_obrigatorio": "valor1", "campo_opcional": 42})
    assert "Recebido: valor1, 42" in result

    # Teste com tipo incorreto (deve lançar ValidationError)
    with pytest.raises(Exception) as exc_info:
        tool.run({"campo_obrigatorio": "valor1", "campo_opcional": "nao_e_numero"})
    assert "campo_opcional" in str(exc_info.value)
```