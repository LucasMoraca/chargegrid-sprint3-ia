
## 8. Comparativo Antes × Depois

| Aspecto | Sprints 1/2 (arquitetura manual) | Sprint 03 (LangGraph + guardrails + comparação de modelos) |
|---|---|---|
| **Arquitetura** | Chamada manual e sequencial à API (função Python simples, sem grafo/orquestrador) | Grafo de agente LangGraph (StateGraph + checkpointer), reutilizável entre provedores |
| **Memória** | Lista Python em memória local, montada manualmente a cada chamada; perdida ao reiniciar o kernel | Gerenciada pelo framework (MemorySaver) via thread_id, testada e validada em 3 turnos (Seção 7) |
| **Seleção de modelo** | Escolha ad hoc (GPT-4o-mini), sem suíte comparativa formal | Baseada em suíte automatizada — modelo escolhido: gemini-3.1-flash-lite (T=0.3) (ver relatorio_modelos.md) |
| **Testes de segurança** | Não formalizados (nenhum caso de Prompt Injection documentado) | 5 casos automatizados (Prompt Injection, escopo, jurídico, financeiro, elétrico) |
| **Medição de latência/tokens** | Qualitativa apenas ('Gemini mais rápido ~1-2s, GPT ~2-4s'), sem tabela | Automática por turno — latência média mínima observada: 0.76 s (gemini-3.1-flash-lite (T=0.3)) |
| **Nº de casos de teste funcionais** | 5 (avaliação manual: Adequada/Parcialmente/Inadequada) | 4 (avaliação automática por palavra-chave: OK/REVISAR) |

### Resultados quantitativos da Sprint 03 (execução real desta sessão)

| modelo                        |   latencia_media_s |   tokens_medio |   testes_ok |   testes_total | taxa_sucesso   |
|:------------------------------|-------------------:|---------------:|------------:|---------------:|:---------------|
| gemini-3.1-flash-lite (T=0.3) |               0.76 |          32.5  |          10 |             12 | 83.3%          |
| gpt-4o-mini (T=0.3)           |               1.4  |          48    |          10 |             12 | 83.3%          |
| gpt-4o-mini (T=0.9)           |               1.67 |          63.08 |          10 |             12 | 83.3%          |

### A nova arquitetura tornou o chatbot melhor?

**Sim, em três frentes concretas:**

1. **Memória confiável**: nas Sprints 1/2 o histórico dependia de uma lista Python mantida manualmente; agora a
   memória é gerenciada pelo framework e foi validada objetivamente (o agente recuperou corretamente "12 vagas" e
   "Solar Park" no 3º turno da mesma sessão — Seção 7.3).
2. **Segurança mensurável**: passamos de nenhum teste formal de Prompt Injection para 5 casos
   de guardrail executados e classificados automaticamente como ADEQUADO/INADEQUADO.
3. **Escolha de modelo baseada em dados**: a seleção do modelo em produção deixou de ser uma preferência do grupo
   e passou a ser resultado direto da suíte comparativa (Seção 7, `relatorio_modelos.md`).

**Trade-off aceito**: a complexidade de código aumentou (grafo, checkpointer, estado tipado) em troca de
memória, testabilidade e portabilidade entre provedores — trade-off considerado favorável dado o ganho em
confiabilidade e auditabilidade do agente.
