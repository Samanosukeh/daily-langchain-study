```python
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class InputSchema(BaseModel):
    """Schema de entrada validado com Pydantic."""
    task_id: str = Field(..., description="ID único da tarefa")
    priority: Optional[int] = Field(
        default=1,
        ge=1,
        le=5,
        description="Prioridade da tarefa (1-5, padrão=1)"
    )
    description: str = Field(..., min_length=10, description="Descrição detalhada da tarefa")

class TaskValidatorTool(BaseTool):
    """Ferramenta para validar inputs de tarefas com Pydantic."""
    name = "validate_task_input"
    description = "Valida dados de entrada para criação/atualização de tarefas"
    args_schema: Type[BaseModel] = InputSchema

    def _run(self, task_id: str, priority: Optional[int] = 1, description: str = "") -> dict:
        """Valida e retorna os dados sanitizados."""
        return {
            "task_id": task_id.strip(),
            "priority": priority,
            "description": description.strip(),
            "is_valid": True
        }

# Exemplo de uso
if __name__ == "__main__":
    tool = TaskValidatorTool()

    # Input válido
    result = tool.run(task_id="t123", description="Implementar nova feature")
    print("Input válido:", result)

    # Input inválido (será rejeitado pelo Pydantic)
    try:
        tool.run(task_id="", description="curto")  # description muito curta
    except Exception as e:
        print("Input inválido:", str(e))
```