```markdown
# Comentários nos Arquivos de Agents

## Introdução
Nesta semana, focamos em **melhorar a legibilidade e manutenção** dos arquivos de `agents` no projeto. O uso de comentários claros e concisos é essencial para documentar lógicas complexas, decisões de design e fluxos de execução.

---

## Boas Práticas para Comentários

### 1. **Comentários Descritivos**
   - **O que fazer**:
     ```python
     # Agent responsável por validar dados de entrada antes do processamento.
     # Rejeita requisições com campos vazios ou tipos incompatíveis.
     class InputValidatorAgent:
         ...
     ```
   - **Evitar**:
     ```python
     # Classe de validação (comentário genérico e inútil)
     ```

### 2. **Comentários em Funções e Métodos**
   - **Docstring** (padrão PEP 257):
     ```python
     def process_data(data: dict) -> dict:
         """Processa dados de entrada e retorna um dicionário estruturado.

         Args:
             data: Dicionário com chaves 'id', 'value' e 'metadata'.

         Returns:
             dict: Dados processados ou None se inválidos.

         Raises:
             ValueError: Se 'id' não for numérico ou 'value' estiver ausente.
         """
         ...
     ```

### 3. **Comentários para Trechos Complexos**
   - **Exemplo**:
     ```python
     # Converte timestamp para datetime e ajusta fuso horário para UTC-3
     # Usado para sincronizar logs com a base de dados local
     timestamp = datetime.fromtimestamp(raw_data["timestamp"]).astimezone(pytz.timezone("America/Sao_Paulo"))
     ```

### 4. **Notas de Depuração (Debug)**
   - **Marcadores claros**:
     ```python
     # TODO: Otimizar query SQL para reduzir tempo de resposta (atualmente ~5s)
     # FIXME: Corrigir bug em que o agent ignora requisições com 'status=pending'
     ```

### 5. **Comentários em Configurações**
   - **Exemplo**:
     ```python
     # Configuração do LLM: modelo 'gpt-4' com temperatura 0.7 para respostas criativas
     llm_config = {
         "model": "gpt-4",
         "temperature": 0.7,
         "max_tokens": 500
     }
     ```

---

## Exemplo Completo

```python
# Agent responsável por orquestrar o fluxo de processamento de documentos.
# Responsabilidades:
#   - Receber arquivos via API
#   - Validar extensão e tamanho
#   - Encaminhar para o agent de extração de texto
class DocumentProcessingAgent:
    """Orquestra o processamento de documentos em etapas."""

    def __init__(self, max_size_mb: int = 10):
        """Inicializa o agent com limite de tamanho de arquivo.

        Args:
            max_size_mb: Tamanho máximo aceito em MB (padrão: 10MB).
        """
        self.max_size = max_size_mb * 1024 * 1024  # Converte para bytes

    def validate_file(self, file_path: str) -> bool:
        """Valida se o arquivo atende aos requisitos.

        Args:
            file_path: Caminho do arquivo a ser validado.

        Returns:
            bool: True se válido, False caso contrário.
        """
        try:
            file_size = os.path.getsize(file_path)
            if file_size > self.max_size:
                raise ValueError(f"Arquivo excede {self.max_size_mb}MB")

            # Extensões permitidas: .pdf, .docx, .txt
            valid_extensions = {".pdf", ".docx", ".txt"}
            if not any(file_path.endswith(ext) for ext in valid_extensions):
                raise ValueError("Extensão não suportada")

            return True
        except Exception as e:
            logging.error(f"Validação falhou: {str(e)}")
            return False
```

---

## Regras de Ouro
1. **Seja específico**: Evite comentários óbvios como `# Incrementa contador`.
2. **Mantenha atualizado**: Comentários desatualizados são piores que nenhum.
3. **Priorize código auto-documentado**: Nomeie variáveis/métodos de forma clara antes de comentar.
4. **Use padrões**: