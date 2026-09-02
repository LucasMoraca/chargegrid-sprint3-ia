## 6. Framework de Agentes — Justificativa Técnica

### 6.1 Framework escolhido: **LangGraph**

O núcleo conversacional do ChargeGrid foi reconstruído com **LangGraph** (biblioteca da equipe LangChain para orquestração de agentes como grafos de estados).

### 6.2 Motivo da escolha

Nas Sprints 1 e 2, o "agente" era, na prática, uma função Python que montava manualmente uma lista de mensagens (`system + histórico + pergunta`) e chamava a API do provedor a cada turno. Não havia:
- controle formal do fluxo de execução (tudo era um único `if/else` linear);
- memória persistente — o histórico era mantido em uma lista Python comum, perdida ao reiniciar o kernel/sessão;
- um ponto único para inserir novos nós (ex.: validação, roteamento, ferramentas) sem reescrever a função inteira.

O LangGraph foi escolhido porque:
1. **Modela o agente como grafo de estados (`StateGraph`)**, deixando explícito o fluxo `entrada → agente → fim`, e permitindo evoluir facilmente para grafos mais complexos (ex.: nó de checagem de guardrail antes do nó do LLM, nó de ferramentas, roteamento condicional) sem reescrever a base.
2. **Possui checkpointer nativo (`MemorySaver`)**, que gerencia a memória por sessão automaticamente através de um `thread_id`, eliminando a necessidade de controlar listas de histórico manualmente.
3. **É agnóstico ao provedor de LLM**, pois se integra ao `langchain-core`: basta trocar o objeto `llm` (`ChatOpenAI`, `ChatGoogleGenerativeAI`, `ChatAnthropic`, etc.) sem alterar a lógica do grafo — o que viabiliza diretamente o requisito de comparação entre modelos (Seção 8).
4. Tem **curva de adoção baixa** para quem já usa LangChain, e documentação madura, o que era relevante dado o prazo curto da sprint.

### 6.3 Principais componentes utilizados

| Componente | Papel no projeto |
|---|---|
| `StateGraph` / `AgentState` (TypedDict) | Define o estado do agente (lista de mensagens) que trafega entre os nós do grafo |
| `add_messages` (reducer) | Garante que novas mensagens sejam **anexadas** ao histórico existente, em vez de sobrescrevê-lo |
| Nó `agent` (`make_agent_node`) | Nó único do grafo: injeta o `SYSTEM_PROMPT` (persona + base de conhecimento + guardrails) e invoca o LLM ativo |
| `MemorySaver` (checkpointer) | Persiste o estado da conversa por `thread_id`, implementando a memória por sessão exigida na Seção 3.2 |
| `thread_id` (`sessao_atual`) | Identificador único de sessão; trocá-lo (botão "Limpar") inicia uma nova conversa sem memória do histórico anterior |
| `get_chat_model(provider, ...)` | *Factory* que abstrai o provedor de LLM (OpenAI/Gemini), permitindo executar a mesma suíte de testes em modelos diferentes apenas trocando um parâmetro |

### 6.4 Vantagens encontradas

- **Memória sem código extra**: o mesmo `thread_id` recupera automaticamente todo o histórico da sessão — o comportamento exigido no exemplo do enunciado (Solar Park / 12 vagas) funciona sem nenhuma lógica adicional de "lembrar" escrita manualmente.
- **Separação de responsabilidades**: o system prompt, a lógica de chamada ao modelo e a interface (ipywidgets) ficaram desacoplados, facilitando testes automatizados (Seção 7) que chamam o grafo diretamente, sem depender da UI.
- **Extensibilidade**: novos nós (ex.: um nó de moderação/guardrail antes do nó do agente, ou um nó de *tools* para consultar tarifas em tempo real) podem ser adicionados ao grafo sem alterar o restante do pipeline.
- **Portabilidade entre modelos**: comparar OpenAI × Gemini exigiu apenas trocar `provider` e `model_name` na *factory* `get_chat_model`, sem duplicar código de orquestração.

### 6.5 Limitações e trade-offs identificados

- **Overhead de aprendizado**: a curva de entrada do LangGraph (estado tipado, reducers, checkpointer) é maior do que simplesmente concatenar strings, o que custou tempo extra no início da sprint.
- **Memória em processo (`MemorySaver`)**: por padrão, o checkpointer usado é em memória (RAM) — a conversa é perdida se o notebook reiniciar. Para produção, seria necessário um checkpointer persistente (ex.: SQLite/Postgres), disponível no LangGraph mas fora do escopo desta sprint.
- **Dependência de biblioteca externa**: qualquer *breaking change* nas APIs do `langchain-core`/`langgraph` (comuns em bibliotecas jovens) pode exigir ajustes no código — risco que não existia na versão "manual" das Sprints 1 e 2.
- **Custo cognitivo de depuração**: erros dentro do grafo (ex.: no reducer `add_messages`) geram *stack traces* mais difíceis de interpretar do que uma função Python simples.
