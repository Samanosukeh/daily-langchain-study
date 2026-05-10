```python
from langchain.prompts import PromptTemplate

# Criando um PromptTemplate com uma variável simples
template = PromptTemplate.from_template(
    "Olá, {nome}! Como posso te ajudar hoje?"
)

# Exemplo de uso
nome_usuario = "João"
prompt_formatado = template.format(nome=nome_usuario)

print(prompt_formatado)
# Saída: Olá, João! Como posso te ajudar hoje?
```