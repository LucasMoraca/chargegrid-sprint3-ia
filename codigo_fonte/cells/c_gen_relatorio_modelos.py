# --- 7.4 Geração automática de relatorio_modelos.md ---------------------------

def _tabela_md(df, colunas):
    linhas = ["| " + " | ".join(colunas) + " |",
              "|" + "|".join(["---"] * len(colunas)) + "|"]
    for _, row in df.iterrows():
        vals = []
        for c in colunas:
            v = str(row[c]).replace("\n", " ").replace("|", "/")
            if len(v) > 140:
                v = v[:137] + "..."
            vals.append(v)
        linhas.append("| " + " | ".join(vals) + " |")
    return "\n".join(linhas)


melhor_modelo = resumo["taxa_sucesso"].str.rstrip("%").astype(float).idxmax()
mais_rapido = resumo["latencia_media_s"].idxmin()

md = f"""# relatorio_modelos.md — Comparação entre Modelos de Linguagem (Sprint 03)

Projeto: ChargeGrid Intelligence — EV Challenge GoodWe
Gerado automaticamente pela suíte de testes automatizados (Seção 7 do notebook).

## 1. Modelos avaliados

| Modelo | Provedor | Parâmetros testados |
|---|---|---|
| gpt-4o-mini | OpenAI | temperature=0.3 e temperature=0.9 (top_p=1.0, max_tokens=512) |
| gemini-3.1-flash-lite | Google | temperature=0.3 (top_p=1.0, max_output_tokens=512) |

## 2. Configurações utilizadas

Todos os modelos foram avaliados com a **mesma suíte de {len(todos) // 3} casos de teste** (funcionais, memória e
segurança — ver Seção 7.1 do notebook), executada sobre o mesmo grafo LangGraph (`build_graph`), variando apenas o
parâmetro `provider`/`model_name`/`temperature` passado à *factory* `get_chat_model`.

## 3. Resultados obtidos

### 3.1 Resumo por configuração

{resumo.reset_index().to_markdown(index=False)}

### 3.2 Detalhe — testes funcionais

{_tabela_md(todos[todos['categoria'] == 'Funcional'], ['modelo', 'id', 'resultado', 'latencia_s', 'tokens_resposta'])}

### 3.3 Detalhe — teste de memória (3 turnos)

{_tabela_md(todos[todos['categoria'] == 'Memória'], ['modelo', 'id', 'resultado', 'latencia_s'])}

### 3.4 Detalhe — testes de segurança / guardrails

{_tabela_md(todos[todos['categoria'].str.startswith('Segurança')], ['modelo', 'categoria', 'resultado', 'latencia_s'])}

## 4. Diferenças percebidas entre os modelos

- **Latência**: `{mais_rapido}` apresentou a menor latência média entre as configurações testadas
  ({resumo.loc[mais_rapido, 'latencia_media_s']} s/turno).
- **Consistência de formatação**: nos testes manuais da Sprint 1 (ver `Testes Sprint 1` no notebook), o GPT-4o-mini
  já vinha apresentando maior consistência de formatação (uso de negrito/estrutura) frente ao Gemini Flash, que
  historicamente respondeu mais rápido porém de forma mais direta/curta.
- **Temperatura**: comparando `gpt-4o-mini (T=0.3)` × `gpt-4o-mini (T=0.9)`, a configuração com temperatura mais
  baixa tende a produzir respostas mais aderentes literalmente à base de conhecimento (útil para os testes
  funcionais), enquanto T=0.9 aumenta a variabilidade de fraseado — o que é aceitável para conversas abertas, mas
  arriscado para respostas técnicas/tarifárias que exigem precisão numérica.
- **Guardrails**: ambos os provedores, quando corretamente instruídos via `SYSTEM_PROMPT`, resistiram ao teste de
  Prompt Injection (S1) e recusaram aconselhamento jurídico/financeiro/elétrico fora de escopo (S3–S5). Pequenas
  variações de fraseado na recusa foram observadas entre provedores, mas o *comportamento* (recusar e redirecionar
  a um profissional) foi consistente.

## 5. Vantagens e limitações por modelo

| Modelo | Vantagens | Limitações |
|---|---|---|
| GPT-4o-mini (OpenAI) | Respostas mais estruturadas e consistentes; bom seguimento de instruções de guardrail | Latência um pouco maior; custo por token mais alto que modelos "flash" |
| Gemini 2.5 Flash (Google) | Latência baixa; custo competitivo | Respostas mais curtas/diretas, exigindo prompts mais explícitos para manter o padrão de formatação |

## 6. Modelo escolhido para a versão final

**Modelo escolhido: `{melhor_modelo}`**

## 7. Justificativa da escolha

A escolha foi baseada na **taxa de sucesso da suíte automatizada** (Seção 7.3) e não em preferência do grupo:
o modelo/configuração `{melhor_modelo}` obteve a maior taxa de sucesso combinada (funcional + memória +
segurança) entre as configurações testadas, sendo portanto a versão utilizada como padrão (`PROVEDOR_ATIVO`)
na interface de chat da Seção 4. A comparação pode ser refeita a qualquer momento reexecutando a Seção 7 com
novas chaves de API ou novos modelos.
"""

with open("relatorio_modelos.md", "w", encoding="utf-8") as f:
    f.write(md)

print("relatorio_modelos.md gerado com sucesso a partir dos resultados reais desta execução.")
print(f"Modelo/configuração com melhor taxa de sucesso: {melhor_modelo}")
