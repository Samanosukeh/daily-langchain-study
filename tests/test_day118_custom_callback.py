```python
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

import pytest
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult, AgentAction, AgentFinish
from langchain_core.agents import AgentActionMessageLog

def test_custom_callback_is_called_on_execution():
    # Mock do callback customizado
    mock_callback = MagicMock(spec=BaseCallbackHandler)

    # Configuração do agente ou cadeia que usará o callback
    # Exemplo mínimo para testar o callback
    from langchain.llms.fake import FakeListLLM

    llm = FakeListLLM(responses=["foo"])

    # Executando o LLM com o callback
    llm.generate(["input"], callbacks=[mock_callback])

    # Verificando se o callback foi chamado
    mock_callback.on_llm_start.assert_called_once()
    mock_callback.on_llm_end.assert_called_once()

def test_custom_callback_is_called_with_correct_args():
    # Mock do callback customizado
    mock_callback = MagicMock(spec=BaseCallbackHandler)

    # Configuração do agente ou cadeia
    from langchain.llms.fake import FakeListLLM

    llm = FakeListLLM(responses=["foo"])

    # Executando o LLM com o callback
    llm.generate(["input"], callbacks=[mock_callback])

    # Capturando os argumentos passados para o callback
    on_llm_start_args = mock_callback.on_llm_start.call_args[0]
    on_llm_end_args = mock_callback.on_llm_end.call_args[0]

    # Verificando se os argumentos estão corretos
    assert on_llm_start_args[0] == "input"
    assert isinstance(on_llm_start_args[1], Dict)
    assert on_llm_end_args[0] is not None  # LLMResult
    assert isinstance(on_llm_end_args[1], Dict)

def test_custom_callback_is_called_on_chain_execution():
    # Mock do callback customizado
    mock_callback = MagicMock(spec=BaseCallbackHandler)

    # Configuração de uma cadeia simples
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    prompt = PromptTemplate.from_template("Responda: {input}")
    chain = (
        {"input": RunnablePassthrough()}
        | prompt
        | StrOutputParser()
    )

    # Executando a cadeia com o callback
    chain.invoke("teste", config={"callbacks": [mock_callback]})

    # Verificando se o callback foi chamado
    assert mock_callback.on_chain_start.call_count >= 1
    assert mock_callback.on_chain_end.call_count >= 1

def test_custom_callback_is_called_on_agent_execution():
    # Mock do callback customizado
    mock_callback = MagicMock(spec=BaseCallbackHandler)

    # Configuração de um agente simples
    from langchain.agents import AgentExecutor, initialize_agent, load_tools
    from langchain.llms.fake import FakeListLLM

    llm = FakeListLLM(responses=["foo"])
    tools = load_tools(["python_repl"], llm=llm)
    agent = initialize_agent(
        tools,
        llm,
        agent="zero-shot-react-description",
        verbose=True
    )
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        callbacks=[mock_callback]
    )

    # Executando o agente
    agent_executor.run("Qual é a capital do Brasil?")

    # Verificando se o callback foi chamado
    assert mock_callback.on_agent_action.call_count >= 1
    assert mock_callback.on_agent_finish.call_count >= 1
```