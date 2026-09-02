# EV Challenge — GoodWe | Sprint 03 — Entrega

Projeto: **ChargeGrid Intelligence** | Disciplina: Prompt and Artificial Intelligence | FIAP (1CCPX) | Grupo 7

## Estrutura da entrega

```
.
├── codigo_fonte/
│   ├── AI_assistant_sprint3.ipynb   ← notebook principal (código-fonte da aplicação)
│   └── reference_stub.py            ← ver observação abaixo
├── casos_de_teste/
│   ├── testes_funcionais.md
│   ├── testes_memoria.md
│   ├── testes_seguranca.md          ← inclui o caso de Prompt Injection
│   └── resultados_testes_completos.csv
├── relatorio_modelos.md             ← comparação entre OpenAI (gpt-4o-mini) e Google (gemini-2.5-flash)
├── relatorio_evolucao.pdf           ← relatório de evolução (≤ 5 páginas)
├── comparativo_antes_depois.md      ← Sprints 1/2 × Sprint 03
├── integrantes.txt                  ← nome, RM e turma dos integrantes
├── .gitignore                       ← garante que .env nunca é versionado
└── gerar_entrega.py                 ← script que gera todos os artefatos acima
```

## Como reproduzir os resultados com dados reais

Os arquivos `relatorio_modelos.md`, `relatorio_evolucao.pdf`, `comparativo_antes_depois.md` e a pasta
`casos_de_teste/` desta entrega foram gerados executando o **mesmo código** de `codigo_fonte/AI_assistant_sprint3.ipynb`
(Seção 7 do notebook). A única diferença é a fonte das respostas do LLM:

- **No notebook (Google Colab, com suas chaves de API)**: as respostas vêm de verdade da OpenAI e do Gemini.
- **Nesta entrega** (gerada em um ambiente sem acesso à internet/chaves de API): as respostas usadas são um
  conjunto de **respostas de referência** (`reference_stub.py`), consistentes com a base de conhecimento do
  projeto. As respostas do teste de memória (Solar Park / 12 vagas) e do teste de Prompt Injection para a
  OpenAI são as respostas **reais**, já obtidas anteriormente pela equipe em execução no Colab.

**Para a entrega oficial**, o grupo deve:
1. Abrir `codigo_fonte/AI_assistant_sprint3.ipynb` no Google Colab;
2. Configurar `OPENAI_API_KEY` e `GEMINI_API_KEY` em Secrets do Colab (Seção 2 do notebook);
3. Executar todas as células — a Seção 7 roda a suíte de testes de verdade e **sobrescreve**
   `relatorio_modelos.md`, `relatorio_evolucao.pdf` e `casos_de_teste/*` com os resultados reais;
4. Substituir os arquivos desta pasta pelos gerados na execução real antes do commit final.

## Publicando no Git

Este pacote já inclui um repositório Git local (`git log` mostra o histórico de desenvolvimento por etapas).
Para publicar:

```bash
git remote add origin <URL_DO_SEU_REPOSITORIO>
git push -u origin main
```

Confira que `.env` **não** aparece em `git status` antes de qualquer commit adicional.
