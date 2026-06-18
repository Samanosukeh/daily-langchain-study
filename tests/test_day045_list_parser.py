```python
import pytest
from typing import List
from langchain.schema import BaseOutputParser

class ListParser(BaseOutputParser[List[str]]):
    """Parser que converte saída de modelo em lista de strings."""

    def parse(self, text: str) -> List[str]:
        """Converte texto em lista, removendo espaços e linhas vazias."""
        return [item.strip() for item in text.split(",") if item.strip()]

def test_list_parser_retorna_lista_python():
    """Testa se o parser converte texto em lista Python corretamente."""
    parser = ListParser()

    # Teste com entrada válida
    texto_entrada = "item1, item2, item3"
    resultado = parser.parse(texto_entrada)
    assert isinstance(resultado, list)
    assert resultado == ["item1", "item2", "item3"]

    # Teste com espaços extras
    texto_entrada = "  item1  ,  item2   ,item3"
    resultado = parser.parse(texto_entrada)
    assert resultado == ["item1", "item2", "item3"]

    # Teste com linhas vazias
    texto_entrada = "item1,,item2, ,item3"
    resultado = parser.parse(texto_entrada)
    assert resultado == ["item1", "item2", "item3"]

    # Teste com entrada vazia
    texto_entrada = ""
    resultado = parser.parse(texto_entrada)
    assert resultado == []

def test_list_parser_lanca_excecao_quando_entrada_invalida():
    """Testa se o parser lida com entrada inválida lançando exceção."""
    parser = ListParser()

    with pytest.raises(Exception):
        parser.parse(None)  # type: ignore

def test_list_parser_com_separador_customizado():
    """Testa parser com separador personalizado."""
    class CustomListParser(BaseOutputParser[List[str]]):
        def parse(self, text: str) -> List[str]:
            return [item.strip() for item in text.split(";") if item.strip()]

    parser = CustomListParser()
    texto_entrada = "item1; item2; item3"
    resultado = parser.parse(texto_entrada)
    assert resultado == ["item1", "item2", "item3"]
```