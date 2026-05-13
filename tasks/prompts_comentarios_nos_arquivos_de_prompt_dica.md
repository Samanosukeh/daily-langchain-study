```markdown
# Dicas Rápidas: Comentários em Arquivos `.prom` (Prometheus)

## 1. Comentários de Linha
Use `#` para comentários de linha única:
```prom
# Este é um comentário explicando a métrica abaixo
node_memory_MemTotal_bytes 4.294967296e+09
```

## 2. Comentários de Bloco
Para blocos de texto, use `/* ... */`:
```prom
/*
  Configuração de alertas para alta utilização de CPU
  Ajuste o threshold conforme necessário.
*/
```

## 3. Comentários em Regras de Alerta
Comente regras de alerta para documentar lógica:
```prom
# Regra: Alerta se CPU > 80% por 5 minutos
- alert: HighCPU
  expr: (100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)) > 80
  for: 5m
  labels:
    severity: warning
```

## 4. Comentários em Funções de Agregação
Documente funções complexas:
```prom
# Calcula a média móvel de 1 hora para métricas de rede
avg_over_time( rate(node_network_receive_bytes_total[1h]) ) by (device)
```

## 5. Comentários em Labels
Use comentários para explicar labels personalizados:
```prom
# Label 'env' distingue ambientes (prod, staging, dev)
node_disk_io_time_seconds_total{device="sda", env="prod"}
```

## 6. Evite Comentários Desnecessários
Não comente código óbvio. Foque em:
- Lógica complexa.
- Decisões de design.
- Riscos conhecidos.

## 7. Ferramentas de Validação
Use `promtool` para verificar sintaxe:
```bash
promtool check rules alert.rules
```

## 8. Boas Práticas
- Mantenha comentários atualizados.
- Use linguagem clara e objetiva.
- Evite comentários redundantes.

---
**Exemplo Completo:**
```prom
# Métrica: Bytes lidos do disco (agrupado por dispositivo)
# Threshold crítico: > 1GB/s
node_disk_read_bytes_total{device=~"sda|sdb"} > 1e9
```
```