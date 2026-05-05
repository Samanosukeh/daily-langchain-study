# daily-langchain-study

Repositório de estudo progressivo de **LangChain**, cobrindo desde os conceitos fundamentais até sistemas completos com RAG, Agents e LangGraph.

## Estrutura

```
daily-langchain-study/
├── docs/        # notas e documentação de cada tópico
├── tasks/       # implementações e exemplos práticos
├── tests/       # testes unitários
└── scripts/     # utilitários do projeto
```

## Currículo (~6 meses)

| Fase | Tópicos |
|------|---------|
| 🟢 Fundamentos | LLM calls, PromptTemplates, LCEL, chains básicas |
| 🔵 Memória & Parsers | Memory, OutputParsers, tipos de dados estruturados |
| 🟣 Tools & Agents | Tools, Toolkits, agentes ReAct |
| 🟡 RAG | Embeddings, vector stores, retrievers, callbacks |
| 🟠 RAG Avançado | Chains avançadas, avaliação, LangGraph |
| 🔴 Projeto Final | Sistema integrado end-to-end com LangGraph |

## Setup Local

```bash
pip install -r requirements.txt
cp .env.example .env  # copie o template e preencha
# Edite .env com sua MISTRAL_API_KEY
```

### Executar Localmente

```bash
# Windows
run_sync.bat

# Linux/Mac
source .env && python scripts/sync.py
```

### Modo Teste (para desenvolvimento)

```bash
# Testar tarefa específica (ex: dia 1)
TEST_MODE=true TEST_DAY=1 python scripts/sync.py

# Windows PowerShell
$env:TEST_MODE="true"; $env:TEST_DAY="1"; python scripts/sync.py
```
