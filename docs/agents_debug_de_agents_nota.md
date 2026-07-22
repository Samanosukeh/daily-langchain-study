```markdown
# Debug de Prompts em LangChain: Validação de Estrutura

## Introdução
Ao trabalhar com LangChain, um aspecto secundário mas crítico é o **debug de prompts**, especialmente quando se lida com templates complexos ou múltiplas variáveis. A validação da estrutura do prompt evita erros silenciosos que podem comprometer toda a cadeia de execução.

## Problema Comum: Inconsistências no Template
Um erro frequente ocorre quando o template do prompt (`PromptTemplate`) não corresponde às variáveis esperadas durante a instanciação. Exemplo:

```python
from langchain.prompts import PromptTemplate

template = "Analise o seguinte texto sobre {tema} e resuma em 3 pontos."
prompt = PromptTemplate.from_template(template)

# Erro: Variável 'assunto' não existe no template
input_data = {"assunto": "IA", "texto": "..."}
prompt.format(**input_data)  # ValueError: Missing variables: tema
```

## Solução: Validação Prévia
Para evitar esse problema, adicione validação explícita antes de formatar o prompt:

```python
def validate_prompt(prompt_template: PromptTemplate, input_data: dict) -> bool:
    missing_vars = set(prompt_template.input_variables) - set(input_data.keys())
    if missing_vars:
        raise ValueError(f"Variáveis ausentes no input: {missing_vars}")
    return True

# Uso:
try:
    validate_prompt(prompt, input_data)
    formatted_prompt = prompt.format(**input_data)
except ValueError as e:
    print(f"Erro no prompt: {e}")
```

## Boas Práticas Adicionais
1. **Logs Detalhados**: Registre o template e as variáveis usadas para debugging:
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   logging.info(f"Template: {prompt.template}")
   logging.info(f"Input: {input_data}")
   ```

2. **Testes Automatizados**: Crie testes unitários para validar prompts críticos:
   ```python
   import pytest

   def test_prompt_template():
       template = "Resuma {texto} em {pontos} tópicos."
       prompt = PromptTemplate.from_template(template)
       assert prompt.input_variables == ["texto", "pontos"]
   ```

3. **Ferramentas Externas**: Use `langchain-core`'s `check_valid_template()` para validação rápida:
   ```python
   from langchain_core.prompts import check_valid_template
   check_valid_template(template, ["tema", "texto"])
   ```

## Conclusão
Validar a estrutura do prompt antes da execução evita erros de runtime e facilita o debugging. Integre essas verificações em pipelines de produção para garantir robustez.
```