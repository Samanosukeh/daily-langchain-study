```python
import pytest
from langchain_core.runnables import Runnable
from chains_advanced.router import route_question

def test_route_question_deve_retornar_chain_financeira_para_pergunta_financeira():
    pergunta = "Qual é o meu saldo atual?"
    resultado = route_question.invoke({"question": pergunta})
    assert resultado == "financeiro_chain"

def test_route_question_deve_retornar_chain_suporte_para_pergunta_suporte():
    pergunta = "Como faço para resetar minha senha?"
    resultado = route_question.invoke({"question": pergunta})
    assert resultado == "suporte_chain"

def test_route_question_deve_retornar_chain_geral_para_pergunta_nao_mapeada():
    pergunta = "Qual a previsão do tempo hoje?"
    resultado = route_question.invoke({"question": pergunta})
    assert resultado == "geral_chain"

def test_route_question_deve_lancar_erro_para_input_invalido():
    with pytest.raises(ValueError):
        route_question.invoke({"question": None})

def test_route_question_deve_lancar_erro_para_chave_faltando():
    with pytest.raises(KeyError):
        route_question.invoke({"pergunta": "Qual é o meu saldo?"})
```