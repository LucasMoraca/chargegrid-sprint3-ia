# --- 7.3 Agregação e resumo dos resultados -----------------------------------

todos = pd.concat([df_openai, df_gemini, df_openai_hot], ignore_index=True)

resumo = todos.groupby("modelo").agg(
    latencia_media_s=("latencia_s", "mean"),
    tokens_medio=("tokens_resposta", "mean"),
    testes_ok=("resultado", lambda s: s.str.contains(r"OK|ADEQUADO", case=False, regex=True).sum()),
    testes_total=("resultado", "count"),
).round(2)
resumo["taxa_sucesso"] = (resumo["testes_ok"] / resumo["testes_total"] * 100).round(1).astype(str) + "%"

print("Resumo por configuração de modelo:")
resumo
