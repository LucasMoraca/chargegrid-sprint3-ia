# --- 8. Comparativo Antes (Sprints 1/2) × Depois (Sprint 03) -----------------
from IPython.display import Markdown, display

# Métricas "antes" — registradas manualmente nas Sprints 1/2 (ver Seção "Testes Sprint 1"
# e o relato qualitativo de latência no notebook original). Não havia medição sistemática
# de tokens/latência por turno: a avaliação era feita lendo a resposta na tela.
metricas_antes = {
    "Arquitetura": "Chamada manual e sequencial à API (função Python simples, sem grafo/orquestrador)",
    "Memória": "Lista Python em memória local, montada manualmente a cada chamada; perdida ao reiniciar o kernel",
    "Seleção de modelo": "Escolha ad hoc (GPT-4o-mini), sem suíte comparativa formal",
    "Testes de segurança": "Não formalizados (nenhum caso de Prompt Injection documentado)",
    "Medição de latência/tokens": "Qualitativa apenas ('Gemini mais rápido ~1-2s, GPT ~2-4s'), sem tabela",
    "Nº de casos de teste funcionais": "5 (avaliação manual: Adequada/Parcialmente/Inadequada)",
}

# Métricas "depois" — calculadas automaticamente pela suíte da Seção 7 desta execução
metricas_depois = {
    "Arquitetura": "Grafo de agente LangGraph (StateGraph + checkpointer), reutilizável entre provedores",
    "Memória": "Gerenciada pelo framework (MemorySaver) via thread_id, testada e validada em 3 turnos (Seção 7)",
    "Seleção de modelo": f"Baseada em suíte automatizada — modelo escolhido: {melhor_modelo} (ver relatorio_modelos.md)",
    "Testes de segurança": f"{len(SECURITY_TESTS)} casos automatizados (Prompt Injection, escopo, jurídico, financeiro, elétrico)",
    "Medição de latência/tokens": f"Automática por turno — latência média mínima observada: {resumo['latencia_media_s'].min()} s ({mais_rapido})",
    "Nº de casos de teste funcionais": f"{len(FUNCTIONAL_TESTS)} (avaliação automática por palavra-chave: OK/REVISAR)",
}

linhas = "\n".join(
    f"| **{k}** | {metricas_antes[k]} | {metricas_depois[k]} |" for k in metricas_antes
)

tabela_resumo_modelos = resumo.reset_index().to_markdown(index=False)

texto = f"""
## 8. Comparativo Antes × Depois

| Aspecto | Sprints 1/2 (arquitetura manual) | Sprint 03 (LangGraph + guardrails + comparação de modelos) |
|---|---|---|
{linhas}

### Resultados quantitativos da Sprint 03 (execução real desta sessão)

{tabela_resumo_modelos}

### A nova arquitetura tornou o chatbot melhor?

**Sim, em três frentes concretas:**

1. **Memória confiável**: nas Sprints 1/2 o histórico dependia de uma lista Python mantida manualmente; agora a
   memória é gerenciada pelo framework e foi validada objetivamente (o agente recuperou corretamente "12 vagas" e
   "Solar Park" no 3º turno da mesma sessão — Seção 7.3).
2. **Segurança mensurável**: passamos de nenhum teste formal de Prompt Injection para {len(SECURITY_TESTS)} casos
   de guardrail executados e classificados automaticamente como ADEQUADO/INADEQUADO.
3. **Escolha de modelo baseada em dados**: a seleção do modelo em produção deixou de ser uma preferência do grupo
   e passou a ser resultado direto da suíte comparativa (Seção 7, `relatorio_modelos.md`).

**Trade-off aceito**: a complexidade de código aumentou (grafo, checkpointer, estado tipado) em troca de
memória, testabilidade e portabilidade entre provedores — trade-off considerado favorável dado o ganho em
confiabilidade e auditabilidade do agente.
"""

display(Markdown(texto))

with open("comparativo_antes_depois.md", "w", encoding="utf-8") as f:
    f.write(texto)
print("comparativo_antes_depois.md salvo.")
