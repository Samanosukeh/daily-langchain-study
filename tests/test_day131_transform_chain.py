```python
import pytest
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import PromptTemplate
from chains_advance import transform_chain

def test_transform_chain_aplica_funcao_corretamente():
    # Dado
    input_text = "  texto com espaços desnecessários  "
    expected_output = "texto com espaços desnecessários"

    # Quando
    result = transform_chain.invoke(input_text)

    # Então
    assert result == expected_output

def test_transform_chain_com_funcao_customizada():
    # Dado
    custom_transform = lambda x: x.upper()
    chain = transform_chain | RunnableLambda(custom_transform)
    input_text = "texto minúsculo"
    expected_output = "TEXTO MINÚSCULO"

    # Quando
    result = chain.invoke(input_text)

    # Então
    assert result == expected_output

def test_transform_chain_com_prompt_template():
    # Dado
    prompt = PromptTemplate.from_template("Processar: {text}")
    chain = transform_chain | prompt | RunnableLambda(lambda x: x.format(text=x))
    input_text = "  texto  "
    expected_output = "Processar: texto"

    # Quando
    result = chain.invoke(input_text)

    # Então
    assert result == expected_output

def test_transform_chain_com_input_vazio():
    # Dado
    input_text = ""
    expected_output = ""

    # Quando
    result = transform_chain.invoke(input_text)

    # Então
    assert result == expected_output

def test_transform_chain_com_input_unicode():
    # Dado
    input_text = "  texto com acentuação: áéíóú  "
    expected_output = "texto com acentuação: áéíóú"

    # Quando
    result = transform_chain.invoke(input_text)

    # Então
    assert result == expected_output
```