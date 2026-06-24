```python
from typing import List
from langchain.output_parsers import OutputFixingParser
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Definição do schema esperado
class Person(BaseModel):
    name: str = Field(description="Nome da pessoa")
    age: int = Field(description="Idade da pessoa")

# Parser original que pode falhar
parser = PydanticOutputParser(pydantic_object=Person)

# Template de prompt com instruções para o modelo
template = """Extraia as informações da seguinte frase:
{query}
{format_instructions}
"""

prompt = PromptTemplate.from_template(
    template,
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Frase com output potencialmente malformado
malformed_query = "João tem 30 anos."

# Criando o OutputFixingParser
fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=None)  # llm=None usa o modelo padrão

# Processando a entrada
try:
    # Tentando parsear diretamente
    direct_output = parser.parse(malformed_query)
except Exception as e:
    print(f"Erro no parse direto: {e}")

    # Corrigindo com OutputFixingParser
    fixed_output = fixing_parser.parse(malformed_query)
    print("\nOutput corrigido:")
    print(fixed_output)
```