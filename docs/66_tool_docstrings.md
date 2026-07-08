```markdown
# Boas Práticas: Docstrings de Tools

## Estrutura Básica
```python
def minha_tool(param1: str, param2: int) -> str:
    """Resumo da funcionalidade da tool em uma linha.

    Args:
        param1 (str): Descrição detalhada do parâmetro 1.
        param2 (int): Descrição detalhada do parâmetro 2.

    Returns:
        str: Descrição do retorno.

    Raises:
        ValueError: Quando o parâmetro 2 é negativo.
        TypeError: Quando o tipo do parâmetro 1 é inválido.

    Example:
        >>> minha_tool("texto", 10)
        "Resultado esperado"
    """
    ...
```

## Regras Gerais
1. **Clareza**: Docstrings devem explicar *o que* a tool faz e *por que* existe.
2. **Parâmetros**: Descrever tipo, propósito e restrições de cada parâmetro.
3. **Retornos**: Especificar tipo e significado do retorno (se aplicável).
4. **Exceções**: Listar exceções comuns que a tool pode lançar.
5. **Exemplos**: Incluir pelo menos um exemplo prático de uso.

## Exemplos por Tipo de Tool

### Tool de Consulta
```python
def buscar_usuario(usuario_id: int) -> dict:
    """Recupera dados de usuário pelo ID.

    Consulta o banco de dados para retornar informações básicas do usuário.

    Args:
        usuario_id (int): ID único do usuário (deve ser > 0).

    Returns:
        dict: Estrutura com campos: id, nome, email, data_criacao.

    Raises:
        NotFoundError: Se o usuário não existir.
    """
    ...
```

### Tool de Ação
```python
def atualizar_status_pedido(pedido_id: str, novo_status: str) -> bool:
    """Atualiza o status de um pedido no sistema.

    Valida o novo_status antes de aplicar a mudança.

    Args:
        pedido_id (str): Código do pedido (formato: "PED-YYYYMMDD-XXXX").
        novo_status (str): Um dos valores permitidos: ["Pendente", "Em Andamento", "Concluído"].

    Returns:
        bool: True se atualização ocorreu com sucesso.

    Raises:
        ValueError: Se novo_status for inválido.
        ConflictError: Se pedido já estiver em status final.
    """
    ...
```

### Tool com Dependências
```python
def enviar_email(
    destinatario: str,
    assunto: str,
    corpo: str,
    anexos: list[str] = None
) -> dict:
    """Envia email via serviço SMTP configurado.

    Args:
        destinatario (str): Endereço email válido.
        assunto (str): Linha de assunto do email.
        corpo (str): Conteúdo em HTML do email.
        anexos (list[str], optional): Lista de paths para arquivos a anexar.

    Returns:
        dict: Estrutura com campos: sucesso (bool), mensagem (str), id_email (str).

    Raises:
        SMTPException: Se ocorrer erro na conexão SMTP.
        ValidationError: Se destinatario ou assunto forem inválidos.
    """
    ...
```

## Convenções Adicionais
- **Formato**: Usar Google Style ou NumPy Style (consistência no projeto).
- **Linguagem**: Escrever em português brasileiro claro e técnico.
- **Atualização**: Manter docstrings sincronizadas com a implementação.
- **Validação**: Ferramentas como `pydocstyle` ou `ruff` podem ser usadas para verificar conformidade.

## Ferramentas Recomendadas
- **Linting**: `pydocstyle`, `ruff`
- **Documentação**: `mkdocs` com plugin `mkdocstrings`
- **Testes**: `pytest` com `doctest` para validar exemplos
```