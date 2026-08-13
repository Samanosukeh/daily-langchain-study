```markdown
# Nota Técnica: Teste de Expressões Regulares com `re` em Python

## Objetivo
Validar expressões regulares (regex) em Python usando o módulo `re` para casos de uso secundários, como:
- Validação de formatos específicos (ex: CEP, CPF, CNPJ).
- Extração de padrões em strings não estruturadas.
- Substituição de substrings com base em padrões complexos.

---

## Implementação Básica

### 1. Validação de CPF
```python
import re

def validar_cpf(cpf: str) -> bool:
    """Valida um CPF no formato XXX.XXX.XXX-XX ou XXXXXXXXXXX."""
    padrao = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$"
    return bool(re.fullmatch(padrao, cpf))
```

### 2. Extração de E-mails
```python
def extrair_emails(texto: str) -> list[str]:
    """Extrai todos os endereços de e-mail de um texto."""
    padrao = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.findall(padrao, texto)
```

### 3. Substituição de Hashtags
```python
def substituir_hashtags(texto: str, substituto: str = "") -> str:
    """Remove ou substitui hashtags de um texto."""
    padrao = r"#\w+"
    return re.sub(padrao, substituto, texto)
```

---

## Casos de Teste Recomendados

| Caso de Teste               | Entrada                          | Resultado Esperado          |
|-----------------------------|----------------------------------|-----------------------------|
| CPF válido (formato 1)      | `"123.456.789-09"`               | `True`                      |
| CPF válido (formato 2)      | `"12345678909"`                  | `True`                      |
| CPF inválido                | `"123.456.789-0"`                | `False`                     |
| Extração de e-mails         | `"Contato: teste@ex.com"`        | `["teste@ex.com"]`          |
| Substituição de hashtags    | `"Python é #legal"`              | `"Python é "`               |

---

## Observações
- **Performance**: Para grandes volumes de texto, pré-compilar padrões com `re.compile()` melhora a eficiência.
- **Limitações**: Regex não é ideal para validações complexas (ex: CPF real). Combine com lógica adicional se necessário.
- **Segurança**: Evite usar `re` para sanitizar inputs em contextos de segurança crítica (SQL injection, XSS).

---
```