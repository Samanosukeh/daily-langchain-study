```python
import pytest
from langchain_core.runnables import RunnableParallel

def test_runnable_parallel_retorna_dict_com_ambas_as_chaves():
    # Arrange
    runnable1 = {"chave1": lambda x: x * 2}
    runnable2 = {"chave2": lambda x: x + 10}
    parallel = RunnableParallel(**runnable1, **runnable2)

    input_data = 5

    # Act
    result = parallel.invoke(input_data)

    # Assert
    assert isinstance(result, dict)
    assert "chave1" in result
    assert "chave2" in result
    assert result["chave1"] == 10  # 5 * 2
    assert result["chave2"] == 15  # 5 + 10

def test_runnable_parallel_com_multiple_chaves():
    # Arrange
    runnable = RunnableParallel(
        dobro={"chave1": lambda x: x * 2},
        soma_dez={"chave2": lambda x: x + 10},
        quadrado={"chave3": lambda x: x ** 2}
    )

    input_data = 3

    # Act
    result = runnable.invoke(input_data)

    # Assert
    assert isinstance(result, dict)
    assert "dobro" in result
    assert "soma_dez" in result
    assert "quadrado" in result
    assert result["dobro"] == 6  # 3 * 2
    assert result["soma_dez"] == 13  # 3 + 10
    assert result["quadrado"] == 9  # 3 ** 2

def test_runnable_parallel_com_input_dict():
    # Arrange
    runnable = RunnableParallel(
        dobro={"__input__": "x", "funcao": lambda x: x * 2},
        soma_dez={"__input__": "y", "funcao": lambda y: y + 10}
    )

    input_data = {"x": 4, "y": 7}

    # Act
    result = runnable.invoke(input_data)

    # Assert
    assert isinstance(result, dict)
    assert "dobro" in result
    assert "soma_dez" in result
    assert result["dobro"] == 8  # 4 * 2
    assert result["soma_dez"] == 17  # 7 + 10

def test_runnable_parallel_encadeado():
    # Arrange
    runnable1 = RunnableParallel(
        dobro={"chave1": lambda x: x * 2}
    )

    runnable2 = RunnableParallel(
        soma_dez={"chave2": lambda x: x + 10}
    )

    input_data = 5

    # Act
    result = (runnable1 | runnable2).invoke(input_data)

    # Assert
    assert isinstance(result, dict)
    assert "dobro" in result
    assert "soma_dez" in result
    assert result["dobro"] == 10  # 5 * 2
    assert result["soma_dez"] == 15  # 5 + 10
```