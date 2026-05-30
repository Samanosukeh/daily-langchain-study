```markdown
# Teste: Batch Retorna Lista com Múltiplos Itens

## Dicas Rápidas

1. **Verifique o tipo de retorno**
   ```python
   assert isinstance(resultado, list), "Batch deve retornar uma lista"
   ```

2. **Teste com múltiplos inputs**
   ```python
   inputs = ["item1", "item2", "item3"]
   resultado = batch_process(inputs)
   assert len(resultado) == len(inputs), "Tamanho da lista deve ser igual ao de inputs"
   ```

3. **Valide conteúdo individual**
   ```python
   for item in resultado:
       assert item in ["esperado1", "esperado2"], f"Item {item} não esperado"
   ```

4. **Teste comportamento com entrada vazia**
   ```python
   assert batch_process([]) == [], "Batch deve retornar lista vazia para entrada vazia"
   ```

5. **Verifique ordem dos itens**
   ```python
   assert resultado[0] == "item1", "Ordem dos itens deve ser preservada"
   ```

6. **Teste com exceções**
   ```python
   with pytest.raises(ValueError):
       batch_process(["invalido"])
   ```

7. **Use pytest.mark.parametrize**
   ```python
   @pytest.mark.parametrize("entrada,esperado", [
       (["a"], ["A"]),
       (["b"], ["B"]),
   ])
   def test_batch(entrada, esperado):
       assert batch_process(entrada) == esperado
   ```

8. **Mock para testes assíncronos**
   ```python
   @patch("modulo.batch_process", return_value=["mock"])
   def test_batch_mock(mock_batch):
       assert batch_process(["teste"]) == ["mock"]
   ```

9. **Teste performance com grandes volumes**
   ```python
   grandes_inputs = ["x"] * 1000
   resultado = batch_process(grandes_inputs)
   assert len(resultado) == 1000
   ```

10. **Valide metadados (se aplicável)**
    ```python
    for item in resultado:
        assert "id" in item, "Cada item deve conter um ID"
    ```
```