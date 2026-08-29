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