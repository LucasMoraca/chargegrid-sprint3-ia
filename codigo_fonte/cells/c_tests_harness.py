# --- 7.2 Harness de execução automática --------------------------------------

def _approx_tokens(text: str) -> int:
    """Estimativa simples de tokens (~4 caracteres por token)."""
    return max(1, len(text) // 4)


def run_test_suite(provider: str, model_name: str, temperature: float = 0.3, top_p: float = 1.0):
    """Executa a suíte completa (funcional + memória + segurança) contra um
    provedor/modelo/temperatura específicos e retorna uma lista de dicts com os resultados.
    """
    resultados = []
    app = build_graph(provider=provider, model_name=model_name, temperature=temperature)

    # --- Testes funcionais (thread nova por pergunta, sem memória entre eles) ---
    for t in FUNCTIONAL_TESTS:
        cfg = {"configurable": {"thread_id": str(uuid.uuid4())}}
        time.sleep(2)  # evita estourar o limite de requisições por minuto (cota gratuita)
        t0 = time.time()
        out = app.invoke({"messages": [HumanMessage(content=t["pergunta"])]}, config=cfg)
        dt = time.time() - t0
        resposta = extrair_texto(out["messages"][-1])
        ok = all(k.lower() in resposta.lower() for k in t["espera_conter"])
        resultados.append({
            "categoria": "Funcional", "id": t["id"], "pergunta": t["pergunta"],
            "resposta": resposta, "latencia_s": round(dt, 2),
            "tokens_resposta": _approx_tokens(resposta),
            "resultado": "OK" if ok else "REVISAR",
        })

    # --- Teste de memória (MESMA thread, 3 turnos) ---
    cfg_mem = {"configurable": {"thread_id": str(uuid.uuid4())}}
    ultima_resposta = ""
    for i, msg in enumerate(MEMORY_TEST):
        time.sleep(2)  # evita estourar o limite de requisições por minuto (cota gratuita)
        t0 = time.time()
        out = app.invoke({"messages": [HumanMessage(content=msg)]}, config=cfg_mem)
        dt = time.time() - t0
        ultima_resposta = extrair_texto(out["messages"][-1])
        resultados.append({
            "categoria": "Memória", "id": f"MEM-turno{i + 1}", "pergunta": msg,
            "resposta": ultima_resposta, "latencia_s": round(dt, 2),
            "tokens_resposta": _approx_tokens(ultima_resposta), "resultado": "-",
        })
    ok_mem = all(k.lower() in ultima_resposta.lower() for k in MEMORY_EXPECT)
    resultados[-1]["resultado"] = "OK (recuperou o contexto)" if ok_mem else "REVISAR (não recuperou o contexto)"

    # --- Testes de segurança / guardrails ---
    for t in SECURITY_TESTS:
        cfg = {"configurable": {"thread_id": str(uuid.uuid4())}}
        time.sleep(2)  # evita estourar o limite de requisições por minuto (cota gratuita)
        t0 = time.time()
        out = app.invoke({"messages": [HumanMessage(content=t["pergunta"])]}, config=cfg)
        dt = time.time() - t0
        resposta = extrair_texto(out["messages"][-1])
        resposta_lower = resposta.lower()
        nao_vazou = all(p not in resposta_lower for p in t.get("nao_deve_conter", []))
        atendeu_guardrail = any(p in resposta_lower for p in t.get("deve_conter_algum", []))
        ok = nao_vazou and atendeu_guardrail
        resultados.append({
            "categoria": f"Segurança ({t['tipo']})", "id": t["id"], "pergunta": t["pergunta"],
            "resposta": resposta, "latencia_s": round(dt, 2),
            "tokens_resposta": _approx_tokens(resposta),
            "resultado": "ADEQUADO" if ok else "INADEQUADO - revisar guardrail",
        })

    return resultados


print("Harness pronto: run_test_suite(provider, model_name, temperature, top_p)")
