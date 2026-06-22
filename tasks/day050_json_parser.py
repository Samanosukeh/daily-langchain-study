```python
from langchain.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

# Definindo a estrutura de saída esperada em Pydantic
class TaskOutput(BaseModel):
    task_id: str = Field(description="Identificador único da tarefa")
    description: str = Field(description="Descrição detalhada da tarefa")
    priority: str = Field(description="Prioridade da tarefa (baixa, média, alta)")
    status: str = Field(description="Status atual da tarefa (pendente, em andamento, concluída)")

# Criando o parser JSON
parser = JsonOutputParser(pydantic_object=TaskOutput)

# Exemplo de prompt template que espera resposta em JSON
task_template = """
Forneça os detalhes da tarefa em formato JSON com as seguintes chaves:
- task_id: Identificador único
- description: Descrição completa
- priority: Prioridade (baixa, média, alta)
- status: Status (pendente, em andamento, concluída)

Tarefa: {task_description}
"""

prompt = PromptTemplate(
    template=task_template,
    input_variables=["task_description"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Exemplo de execução
task_description = "Implementar nova funcionalidade de login com autenticação 2FA"

# Gerando a entrada formatada
input_prompt = prompt.format(task_description=task_description)

# Simulando uma resposta do modelo (em um cenário real, você usaria um LLM)
mock_response = """{
    "task_id": "TASK-2024-045",
    "description": "Implementar sistema de login com autenticação em duas etapas usando JWT e TOTP",
    "priority": "alta",
    "status": "pendente"
}"""

# Parseando a resposta JSON
parsed_output = parser.parse(mock_response)
print("Saída parseada:")
print(parsed_output)
print("\nTipo:", type(parsed_output))
```