```python
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List, Optional, Union
import os
from datetime import datetime

class FileCallbackHandler(BaseCallbackHandler):
    """Callback handler que salva logs em arquivo."""

    def __init__(self, file_path: str = "langchain_logs.txt"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Cria o arquivo se não existir."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(f"=== Logs gerados em: {datetime.now().isoformat()} ===\n\n")

    def _write_log(self, message: str) -> None:
        """Escreve uma mensagem no arquivo de log."""
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - {message}\n")

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Chamado quando o LLM começa a ser executado."""
        message = f"LLM Start - Modelo: {serialized.get('id', ['Desconhecido'])[-1]}"
        self._write_log(message)

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """Chamado quando o LLM termina a execução."""
        self._write_log("LLM End - Resposta recebida")

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Chamado quando uma cadeia (chain) começa."""
        chain_name = serialized.get("id", ["Desconhecido"])[-1]
        self._write_log(f"Chain Start - Nome: {chain_name}")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Chamado quando uma cadeia termina."""
        self._write_log("Chain End - Outputs recebidos")

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Chamado quando uma ferramenta começa."""
        tool_name = serialized.get("id", ["Desconhecido"])[-1]
        self._write_log(f"Tool Start - Nome: {tool_name}, Input: {input_str}")

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Chamado quando uma ferramenta termina."""
        self._write_log(f"Tool End - Output: {output}")

    def on_agent_action(self, action: Any, **kwargs: Any) -> None:
        """Chamado quando um agente executa uma ação."""
        log_message = f"Agent Action - {action.log}"
        self._write_log(log_message)

    def on_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> None:
        """Chamado quando ocorre um erro."""
        error_type = type(error).__name__
        self._write_log(f"ERROR - Tipo: {error_type}, Mensagem: {str(error)}")
```