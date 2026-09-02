```python
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List, Optional
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TokenUsageLogger(BaseCallbackHandler):
    """Callback handler para logar o uso de tokens durante execução."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.total_tokens = 0
        self.total_cost = 0.0  # Se aplicável

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        if self.verbose:
            logger.info("LLM iniciado com prompts: %s", prompts)

    def on_llm_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        if self.verbose:
            usage = outputs.get("llm_output", {}).get("token_usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)
            total_tokens = input_tokens + output_tokens

            self.total_tokens += total_tokens

            logger.info(
                "LLM finalizado | Input: %d tokens | Output: %d tokens | Total: %d tokens",
                input_tokens,
                output_tokens,
                total_tokens,
            )

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        if self.verbose:
            logger.info("Chain iniciada com inputs: %s", inputs)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        if self.verbose:
            logger.info("Chain finalizada")

# Exemplo de uso:
if __name__ == "__main__":
    from langchain.chains import LLMChain
    from langchain.llms import OpenAI
    from langchain.prompts import PromptTemplate

    # Configuração do LLM (substitua pela sua chave API)
    llm = OpenAI(
        model_name="text-davinci-003",
        temperature=0,
        callbacks=[TokenUsageLogger(verbose=True)],
    )

    # Criação de uma chain simples
    template = "Pergunta: {question}\nResposta:"
    prompt = PromptTemplate.from_template(template)
    chain = LLMChain(llm=llm, prompt=prompt)

    # Execução
    response = chain.run(question="Qual é a capital do Brasil?")
    print("\nResposta:", response)
```

---

```markdown
# Comentários Detalhados nos Callbacks

## Introdução
Este documento descreve o uso de comentários detalhados nos callbacks do LangChain, com foco em clareza e manutenibilidade do código.

---

## Estrutura Básica de um Callback

```python
from langchain.callbacks.base import BaseCallbackHandler

class CustomCallbackHandler(BaseCallbackHandler):
    """Callback personalizado com comentários explicativos."""

    def on_llm_start(self, serialized: dict, prompts: list[str], **kwargs) -> None:
        """Chamado quando o LLM começa a gerar uma resposta.

        Args:
            serialized (dict): Metadados serializados do LLM.
            prompts (list[str]): Lista de prompts enviados ao LLM.
            **kwargs: Argumentos adicionais (ex: run_id, parent_run_id).
        """
        print(f"🔹 Iniciando geração de resposta para os prompts: {prompts}")

    def on_llm_end(self, outputs: dict, **kwargs) -> None:
        """Chamado quando o LLM termina a geração de resposta.

        Args:
            outputs (dict): Saída gerada pelo LLM (ex: texto, tokens).
            **kwargs: Argumentos adicionais (ex: run_id, parent_run_id).
        """
        print(f"✅ Resposta gerada: {outputs['generations'][0][0].text}")
```

---

## Tipos de Callbacks e Comentários

### 1. **Callbacks de LLM**
Comentários devem esclarecer o estágio do fluxo de execução e os dados manipulados.

```python
def on_llm_error(self, error: Exception, **kwargs) -> None:
    """Trata erros durante a execução do LLM.

    Args:
        error (Exception): Exceção levantada pelo LLM.
        **kwargs: Metadados do erro (ex: run_id, input).
    """
    print(f"❌ Erro no LLM: {error}")
    # Log adicional pode ser feito aqui (ex: Sentry, arquivo).
```

---

### 2. **Callbacks de Tool (Ferramentas)**
Comentários devem explicar a execução da ferramenta e os parâmetros usados.

```python
def on_tool_start(self, serialized: dict, input_str: str, **kwargs) -> None:
    """Chamado antes da execução de uma ferramenta.

    Args:
        serialized (dict): Metadados da ferramenta.
        input_str (str): Entrada passada para a ferramenta.
        **kwargs: Argumentos adicionais (ex: run_id, parent_run_id).
    """
    tool_name = serialized.get("name", "Desconhecida")
    print(f"🛠️ Iniciando ferramenta '{tool_name}' com entrada: {input_str[:50]}...")
```

---

### 3. **Callbacks de Chain (Cadeias)**
Comentários devem detalhar o fluxo da cadeia e os dados intermediários.

```python
def on_chain_start(self, serialized: dict, inputs: dict, **kwargs) -> None:
    """Chamado no início da execução de uma cadeia.

    Args:
        serialized (dict): Metadados da cadeia.
        inputs (dict): Dados de entrada da cadeia.
        **kwargs: Argumentos adicionais (ex: run_id, parent_run_id).
    """
    chain_name = serialized.get("name", "Desconhecida")
    print(f"🔗 Iniciando cadeia '{chain_name}' com inputs: {inputs}")
```

---

## Boas Práticas para Comentários

1. **Docstrings Completas**
   Use docstrings no formato Google ou NumPy para documentar:
   - Propósito do método.
   - Argumentos (`Args`).
   - Retornos (`Returns`, se aplicável).
   - Exceções levantadas (`Raises`).

2. **Comentários Inline para Lógica Complexa**
   ```python
   # Valida se o input é uma lista não vazia antes de prosseguir.
   if not isinstance(inputs, list) or len(inputs) == 0:
       raise ValueError("Input deve ser uma lista não vazia.")
   ```

3. **Exemplos de Uso**
   Inclua exemplos práticos nos comentários para facilitar a adoção:
   ```python
   """Exemplo de uso:
   ```python
   handler = CustomCallbackHandler()
   chain = LLMChain(llm=llm, callbacks=[handler])
   chain.run("Qual é a capital do Brasil?")
   ```
   """

4. **Marcações Visuais para Desta