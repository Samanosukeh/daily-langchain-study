```markdown
# MCP Resources: Tratamento de Erros em Streams de Dados

## Introdução
Ao trabalhar com streams de dados em MCP Resources, é comum encontrar cenários onde a conexão é interrompida ou ocorrem erros de parsing. Este documento aborda técnicas para lidar com esses casos de forma robusta.

## Tratamento de Exceções em Streams

```python
from mcp import ClientSession
import logging

logger = logging.getLogger(__name__)

async def stream_with_recovery(session: ClientSession, resource_uri: str):
    max_retries = 3
    retry_delay = 1  # segundos

    for attempt in range(max_retries):
        try:
            async with session.stream_resource(resource_uri) as stream:
                async for chunk in stream:
                    try:
                        # Processa o chunk
                        process_chunk(chunk)
                    except ValueError as e:
                        logger.warning(f"Chunk inválido (tentativa {attempt+1}): {e}")
                        continue
                    except Exception as e:
                        logger.error(f"Erro ao processar chunk: {e}")
                        raise

        except ConnectionError as e:
            if attempt == max_retries - 1:
                logger.error("Máximo de tentativas atingido")
                raise
            logger.warning(f"Conexão perdida (tentativa {attempt+1}). Reconnectando...")
            await asyncio.sleep(retry_delay)
            continue

        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            raise
```

## Validação de Dados em Tempo Real

```python
from pydantic import BaseModel, ValidationError

class DataChunk(BaseModel):
    timestamp: float
    value: float
    metadata: dict

async def validate_stream_chunk(chunk: dict):
    try:
        validated = DataChunk(**chunk)
        return validated
    except ValidationError as e:
        logger.warning(f"Dados inválidos: {e}")
        return None
```

## Bufferização para Recuperação

```python
from collections import deque

class RecoverableStream:
    def __init__(self, window_size: int = 100):
        self.buffer = deque(maxlen=window_size)
        self.last_valid_index = -1

    async def add_chunk(self, chunk: DataChunk):
        self.buffer.append(chunk)
        if chunk.is_valid():  # Método customizado
            self.last_valid_index = len(self.buffer) - 1

    def recover_from_last_valid(self) -> list[DataChunk]:
        if self.last_valid_index >= 0:
            return list(self.buffer)[self.last_valid_index+1:]
        return []
```

## Considerações Finais
1. Sempre implemente timeouts para operações de stream
2. Use validação de dados com Pydantic para garantir consistência
3. Considere implementar um mecanismo de checkpoint para retomar streams longos
4. Monitore métricas de tentativas de reconexão e erros de parsing
```