import pytest
from langchain_community.llms import HuggingFaceHub

def test_resposta_nao_vazia():
    """Teste unitário para verificar se a resposta do LLM não é vazia."""
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-small",
        model_kwargs={"temperature": 0.5, "max_length": 50}
    )
    resposta = llm.invoke("Qual a capital do Brasil?")
    assert resposta.strip(), "Resposta do LLM está vazia ou contém apenas espaços"
