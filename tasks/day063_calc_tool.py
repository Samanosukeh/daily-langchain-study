```python
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

class CalculatorInput(BaseModel):
    """Input para operações de calculadora."""
    num1: float = Field(..., description="Primeiro número")
    num2: float = Field(..., description="Segundo número")
    operation: str = Field(..., description="Operação a ser realizada: 'soma', 'subtracao', 'multiplicacao' ou 'divisao'")

class CalculatorTool(BaseTool):
    """Ferramenta de calculadora para operações básicas."""
    name = "calculadora"
    description = "Realiza operações matemáticas básicas entre dois números."
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, num1: float, num2: float, operation: str) -> float:
        """Executa a operação matemática."""
        if operation == "soma":
            return num1 + num2
        elif operation == "subtracao":
            return num1 - num2
        elif operation == "multiplicacao":
            return num1 * num2
        elif operation == "divisao":
            if num2 == 0:
                raise ValueError("Divisão por zero não é permitida.")
            return num1 / num2
        else:
            raise ValueError(f"Operação '{operation}' não suportada.")

# Exemplo de uso
if __name__ == "__main__":
    calculadora = CalculatorTool()
    resultado = calculadora._run(num1=10, num2=5, operation="soma")
    print(f"Resultado: {resultado}")
```