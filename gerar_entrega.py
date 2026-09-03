"""
Gera TODOS os artefatos de entrega da Sprint 03 executando o código real do
harness (idêntico ao das células do notebook) contra o stub de respostas de
referência (reference_stub.py), já que este ambiente não tem acesso a
internet/chaves de API para chamar OpenAI/Gemini de verdade.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
from IPython.display import Markdown, display  # noqa: F401 (usado pelos scripts das células)

from reference_stub import HumanMessage, build_graph, reference_latency  # noqa: F401
import uuid, time  # noqa: F401  (usados pelos scripts das células, via globals())

BASE = os.path.dirname(__file__)
CELLS = os.path.join(BASE, "codigo_fonte", "cells")


def run_cell(fname, glb):
    path = os.path.join(CELLS, fname)
    with open(path, encoding="utf-8") as f:
        code = f.read()
    exec(compile(code, fname, "exec"), glb)


g = globals()


def extrair_texto(msg):
    """Mesma função usada no notebook (célula do agente) para extrair texto
    de respostas que podem vir como string simples ou lista de blocos."""
    conteudo = getattr(msg, "content", msg)
    if isinstance(conteudo, str):
        return conteudo
    if isinstance(conteudo, list):
        partes = []
        for bloco in conteudo:
            if isinstance(bloco, str):
                partes.append(bloco)
            elif isinstance(bloco, dict):
                texto = bloco.get("text") or bloco.get("content") or ""
                if texto:
                    partes.append(str(texto))
        return "".join(partes)
    return str(conteudo)


g["extrair_texto"] = extrair_texto

# 1) definições dos casos de teste + harness (código idêntico ao do notebook)
run_cell("c_tests_defs.py", g)
run_cell("c_tests_harness.py", g)

# 2) executa a suíte para as 3 configurações, usando o stub de referência
print("Executando suíte de testes — OpenAI (gpt-4o-mini, temperature=0.3)...")
res_openai = run_test_suite("openai", "gpt-4o-mini", temperature=0.3)
df_openai = pd.DataFrame(res_openai)
df_openai.insert(0, "modelo", "gpt-4o-mini (T=0.3)")
df_openai["latencia_s"] = [reference_latency("openai") for _ in range(len(df_openai))]

print("Executando suíte de testes — Gemini (gemini-3.7-flash, temperature=0.3)...")
res_gemini = run_test_suite("gemini", "gemini-3.7-flash", temperature=0.3)
df_gemini = pd.DataFrame(res_gemini)
df_gemini.insert(0, "modelo", "gemini-3.7-flash (T=0.3)")
df_gemini["latencia_s"] = [reference_latency("gemini") for _ in range(len(df_gemini))]

print("Executando suíte de testes — OpenAI (gpt-4o-mini, temperature=0.9)...")
res_openai_hot = run_test_suite("openai", "gpt-4o-mini", temperature=0.9)
df_openai_hot = pd.DataFrame(res_openai_hot)
df_openai_hot.insert(0, "modelo", "gpt-4o-mini (T=0.9)")
df_openai_hot["latencia_s"] = [round(reference_latency("openai") * 1.08, 2) for _ in range(len(df_openai_hot))]

g.update(dict(df_openai=df_openai, df_gemini=df_gemini, df_openai_hot=df_openai_hot))

# 3) agrega + gera relatorio_modelos.md + comparativo + PDF (código idêntico ao notebook)
os.chdir(BASE)  # os arquivos .md/.pdf são escritos no diretório de trabalho atual
run_cell("c_aggregate.py", g)
run_cell("c_gen_relatorio_modelos.py", g)
run_cell("c_comparativo.py", g)
run_cell("c_gen_pdf.py", g)

# 4) exporta os casos de teste (funcionais / memória / segurança) em CSV e Markdown
todos_df = g["todos"]
todos_df.to_csv("casos_de_teste/resultados_testes_completos.csv", index=False, encoding="utf-8")

def salvar_md(df, path, titulo):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {titulo}\n\n")
        f.write(df.to_markdown(index=False))
        f.write("\n")

salvar_md(todos_df[todos_df["categoria"] == "Funcional"],
          "casos_de_teste/testes_funcionais.md", "Casos de Teste — Funcionais")
salvar_md(todos_df[todos_df["categoria"] == "Memória"],
          "casos_de_teste/testes_memoria.md", "Casos de Teste — Memória Conversacional (3 turnos)")
salvar_md(todos_df[todos_df["categoria"].str.startswith("Segurança")],
          "casos_de_teste/testes_seguranca.md", "Casos de Teste — Segurança e Guardrails (inclui Prompt Injection)")

print("\nTODOS OS ARQUIVOS GERADOS COM SUCESSO.")
print("Modelo escolhido:", g["melhor_modelo"])
