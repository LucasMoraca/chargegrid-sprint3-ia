print("Executando suíte de testes — Gemini (gemini-2.5-flash, temperature=0.3)...")
res_gemini = run_test_suite("gemini", "gemini-2.5-flash", temperature=0.3)
df_gemini = pd.DataFrame(res_gemini)
df_gemini.insert(0, "modelo", "gemini-2.5-flash (T=0.3)")
df_gemini[["categoria", "id", "resultado", "latencia_s", "tokens_resposta"]]
