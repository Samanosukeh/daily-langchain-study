```python
from langchain_core.output_parsers import StrOutputParser

# Instancia o parser mais simples para converter saída de LLM em string
output_parser = StrOutputParser()

# Exemplo de uso com uma saída de LLM
llm_output = "O céu é azul durante o dia.\n"
parsed_output = output_parser.parse(llm_output)

print(parsed_output)  # Saída: "O céu é azul durante o dia."
```