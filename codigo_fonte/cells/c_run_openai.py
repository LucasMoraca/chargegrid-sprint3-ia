import pandas as pd

print("Executando suíte de testes — OpenAI (gpt-4o-mini, temperature=0.3)...")
res_openai = run_test_suite("openai", "gpt-4o-mini", temperature=0.3)
df_openai = pd.DataFrame(res_openai)
df_openai.insert(0, "modelo", "gpt-4o-mini (T=0.3)")
df_openai[["categoria", "id", "resultado", "latencia_s", "tokens_resposta"]]
