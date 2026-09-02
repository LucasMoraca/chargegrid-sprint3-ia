## 9. Divisão da Equipe e Problemas Encontrados

### 9.1 Divisão da equipe

| Nome | RM | Principal responsabilidade |
|---|---|---|
| Renan Fracalossi Mano da Silva | 569610 | Engenharia de Agentes (Dev Core) — arquitetura LangGraph, `StateGraph`, checkpointer de memória |
| Gabriel Barbosa Furin | 572941 | Guardrails e testes de segurança — casos de Prompt Injection e validação de escopo |
| Gabriel de Almeida Santos | 569395 | Comparação entre modelos — harness de testes, `relatorio_modelos.md`, experimentação de parâmetros |
| Herbert Soares de Jesus | 571507 | Interface de chat (ipywidgets) e integração da base de conhecimento (`MINHA_BASE`) |
| Lucas Kiodi Moraca | 571004 | Documentação, comparativo antes × depois e relatório de evolução (PDF) |

### 9.2 Problemas encontrados e soluções adotadas

**Problema 1 — Memória perdida entre execuções de célula**
- *Alternativas consideradas*: (a) salvar o histórico em uma variável global manual; (b) usar um checkpointer
  persistente em disco/banco (ex.: SQLite); (c) usar o `MemorySaver` em memória do LangGraph.
- *Solução adotada*: `MemorySaver` do LangGraph, indexado por `thread_id`.
- *Justificativa*: atende ao requisito de memória por sessão exigido na sprint com baixa complexidade de
  implementação; a limitação de não persistir em disco foi aceita porque o escopo do projeto é uma demonstração
  local, não um serviço em produção contínua.

**Problema 2 — Avaliação de guardrails de forma subjetiva**
- *Alternativas consideradas*: (a) leitura manual de cada resposta, classificando "parece seguro"/"não parece";
  (b) usar um segundo LLM como "juiz" para classificar as respostas; (c) usar checagem por palavras-chave
  (heurística determinística) combinando termos que devem e que não devem aparecer na resposta.
- *Solução adotada*: checagem por palavras-chave (heurística), com revisão manual dos casos marcados como
  "REVISAR"/"INADEQUADO".
- *Justificativa*: é reprodutível, não depende de custo/latência extra de um segundo LLM avaliador e é suficiente
  para o volume de casos de teste desta sprint; a limitação (falsos negativos se o modelo usar sinônimos não
  previstos) é mitigada pela revisão manual dos casos sinalizados.

**Problema 3 — Comparar modelos de provedores diferentes de forma justa**
- *Alternativas consideradas*: (a) comparar apenas "na sensação", testando manualmente; (b) fixar exatamente os
  mesmos parâmetros (`temperature`, `top_p`, `max_tokens`) e a mesma suíte de perguntas para todos os provedores.
- *Solução adotada*: (b) — mesma suíte, mesmos parâmetros por padrão, com um experimento adicional variando
  `temperature` apenas para o modelo já líder, isolando o efeito do parâmetro do efeito do provedor.
- *Justificativa*: garante que as diferenças observadas sejam atribuíveis ao modelo (e não a perguntas ou
  parâmetros diferentes entre execuções), tornando a escolha final do modelo defensável com dados.
