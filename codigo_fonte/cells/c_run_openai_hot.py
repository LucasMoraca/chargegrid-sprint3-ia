# Experimento adicional: mesmo modelo, temperatura mais alta (exploração de parâmetros)
print("Executando suíte de testes — OpenAI (gpt-4o-mini, temperature=0.9)...")
res_openai_hot = run_test_suite("openai", "gpt-4o-mini", temperature=0.9)
df_openai_hot = pd.DataFrame(res_openai_hot)
df_openai_hot.insert(0, "modelo", "gpt-4o-mini (T=0.9)")
df_openai_hot[["categoria", "id", "resultado", "latencia_s", "tokens_resposta"]]
