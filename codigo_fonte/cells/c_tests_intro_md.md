## 7. Suíte de Testes Automatizados (Sprint 03)

Diferente do roteiro manual usado nas Sprints 1 e 2 (perguntar na interface e copiar a resposta na mão), a Sprint 03 executa os testes **programaticamente**, chamando o grafo LangGraph diretamente (`app.invoke`). Isso permite:

- repetir exatamente a mesma suíte para **qualquer combinação de provedor/modelo/parâmetros** (Seção 8);
- medir **latência** e **tokens aproximados** de cada resposta;
- aplicar critérios objetivos (palavras-chave esperadas / proibidas) para marcar cada teste como `OK`/`REVISAR` ou `ADEQUADO`/`INADEQUADO`, reduzindo a subjetividade da avaliação manual.

A suíte cobre três categorias, conforme exigido no enunciado:

1. **Testes funcionais** — o agente responde corretamente com base na base de conhecimento do projeto (`MINHA_BASE`).
2. **Teste de memória conversacional** — 3 turnos na mesma sessão (`thread_id`), replicando o exemplo do condomínio Solar Park.
3. **Testes de segurança / guardrails** — Prompt Injection, tentativa de fuga de escopo, aconselhamento jurídico, aconselhamento financeiro e orientação de segurança elétrica perigosa.

> Execute as células desta seção com suas próprias chaves de API (Seção 2) para reproduzir os resultados. Os resultados de referência obtidos pela equipe estão documentados em `relatorio_modelos.md` e no relatório de evolução (PDF).
