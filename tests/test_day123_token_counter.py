```python
import pytest
from unittest.mock import MagicMock, patch
from typing import Any, Dict, List, Optional, Union
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.tokens import TokenCounter

class MockCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        super().__init__()
        self.tokens = []

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.tokens.append(prompts[0])

    def on_llm_end(
        self,
        response: Any,
        *,
        run_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.tokens.append(str(response))

def test_token_counter_acumula_corretamente():
    # Setup
    handler = MockCallbackHandler()
    token_counter = TokenCounter(handlers=[handler])

    # Test on_llm_start
    prompts = ["Primeira mensagem", "Segunda mensagem"]
    token_counter.on_llm_start(
        serialized={},
        prompts=prompts,
        run_id="test_run_1"
    )

    assert len(handler.tokens) == 2
    assert handler.tokens[0] == "Primeira mensagem"
    assert handler.tokens[1] == "Segunda mensagem"

    # Test on_llm_end
    response = "Resposta do modelo"
    token_counter.on_llm_end(
        response=response,
        run_id="test_run_1"
    )

    assert len(handler.tokens) == 3
    assert handler.tokens[2] == response

    # Test multiple runs
    token_counter.on_llm_start(
        serialized={},
        prompts=["Terceira mensagem"],
        run_id="test_run_2"
    )

    assert len(handler.tokens) == 4
    assert handler.tokens[3] == "Terceira mensagem"

    token_counter.on_llm_end(
        response="Outra resposta",
        run_id="test_run_2"
    )

    assert len(handler.tokens) == 5
    assert handler.tokens[4] == "Outra resposta"

def test_token_counter_com_limpeza():
    # Setup
    handler = MockCallbackHandler()
    token_counter = TokenCounter(handlers=[handler])

    # Primeiro run
    token_counter.on_llm_start(
        serialized={},
        prompts=["Mensagem 1"],
        run_id="run_1"
    )
    token_counter.on_llm_end(
        response="Resposta 1",
        run_id="run_1"
    )

    # Segundo run
    token_counter.on_llm_start(
        serialized={},
        prompts=["Mensagem 2"],
        run_id="run_2"
    )
    token_counter.on_llm_end(
        response="Resposta 2",
        run_id="run_2"
    )

    # Verifica que os tokens estão sendo acumulados corretamente
    assert len(handler.tokens) == 4
    assert handler.tokens == ["Mensagem 1", "Resposta 1", "Mensagem 2", "Resposta 2"]

def test_token_counter_com_multiplos_handlers():
    # Setup
    handler1 = MockCallbackHandler()
    handler2 = MockCallbackHandler()
    token_counter = TokenCounter(handlers=[handler1, handler2])

    # Executa ação
    token_counter.on_llm_start(
        serialized={},
        prompts=["Mensagem"],
        run_id="run_1"
    )

    # Verifica que ambos handlers receberam a mensagem
    assert len(handler1.tokens) == 1
    assert len(handler2.tokens) == 1
    assert handler1.tokens[0] == "Mensagem"
    assert handler2.tokens[0] == "Mensagem"
```