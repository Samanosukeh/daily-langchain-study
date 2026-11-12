```markdown
# Notas Técnicas: LangChain + Servidores - Tratamento de Erros em Cadeias de Ferramentas

## Contexto
Ao integrar LangChain com servidores externos (APIs, bases de dados, etc.), é comum encontrar erros de:
- Timeout (ex: `requests.exceptions.Timeout`)
- Rate Limiting (ex: `429 Too Many Requests`)
- Autenticação inválida (ex: `401 Unauthorized`)

## Solução: Middleware de Resiliência

Crie um wrapper para ferramentas externas com:
1. **Tentativas múltiplas** (exponential backoff)
2. **Cache de erros** (evita repetir chamadas falhas)
3. **Timeouts configuráveis**

```python
from langchain_core.tools import tool
from tenacity import retry, stop_after_attempt, wait_exponential
import requests
from functools import wraps

def with_retry(max_attempts=3, initial_delay=1):
    def decorator(func):
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=1, min=initial_delay, max=10)
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                raise ValueError(f"Servidor indisponível: {str(e)}")
        return wrapper
    return decorator

# Exemplo de uso
@with_retry(max_attempts=3)
def buscar_dados_api(url: str) -> dict:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

@tool
def ferramenta_externa(query: str) -> str:
    """Busca dados externos com resiliência"""
    return buscar_dados_api(f"https://api.example.com/data?q={query}")
```

## Boas Práticas
- **Logs**: Registre tentativas/erros (ex: `logging.warning(f"Tentativa {i} falhou: {e}")`)
- **Metrics**: Monitore falhas (ex: Prometheus/Grafana)
- **Circuit Breaker**: Use `pybreaker` para desativar temporariamente serviços instáveis

## Limitações
- Não substitui monitoramento proativo
- Ajuste `max_attempts` conforme SLAs do serviço externo
```