```markdown
# CriteriaEvalChain: avaliar por critérios objetivos

O `CriteriaEvalChain` é uma ferramenta poderosa no ecossistema LangChain para validar respostas de LLM com base em critérios explícitos, eliminando a subjetividade. Seu maior valor está em padronizar avaliações, especialmente em pipelines de RAG ou geração de texto onde consistência é crítica.

A configuração básica exige dois componentes:
1. **Critérios**: Definidos como uma lista de dicionários com chaves como `name`, `criteria` e `weight` (opcional).
2. **Avaliador**: Um LLM ou função que pontua cada critério em uma escala (ex: 1-5).

Exemplo prático:
```python
criteria = [
    {"name": "precisao", "criteria": "A resposta contém apenas informações factuais?", "weight": 0.4},
    {"name": "completeza", "criteria": "Todos os aspectos da pergunta foram abordados?", "weight": 0.6}
]
```

**Pontos de atenção**:
- **Peso dos critérios**: Ajuste conforme a importância relativa (ex: precisão > estilo).
- **Flexibilidade**: Critérios podem ser dinâmicos (ex: extraídos de metadados).
- **Limitações**: Avaliação ainda depende da qualidade do LLM avaliador. Para casos críticos, considere validação humana ou regras de negócio.

**Quando usar**:
- Validação de respostas em sistemas de suporte.
- Benchmarking de modelos em domínios específicos.
- Automação de feedback em pipelines de geração.
```