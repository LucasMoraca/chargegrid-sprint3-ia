# --- 10. Geração do Relatório de Evolução (PDF, máx. 5 páginas) --------------
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], fontSize=15, spaceAfter=8, textColor=colors.HexColor("#3b1e73")))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], fontSize=12, spaceAfter=6, textColor=colors.HexColor("#5b21b6")))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontSize=9.5, leading=13, spaceAfter=6))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8, leading=11, textColor=colors.grey))

story = []

# Capa / título
story.append(Paragraph("Relatório de Evolução — Sprint 03", styles["Title"]))
story.append(Paragraph("Projeto ChargeGrid Intelligence — EV Challenge GoodWe (FIAP, Grupo 7)", styles["Body"]))
story.append(Spacer(1, 10))

# 7.1 Resumo da evolução
story.append(Paragraph("1. Resumo da evolução (Sprints 1/2 → Sprint 03)", styles["H1"]))
story.append(Paragraph(
    "Nas Sprints 1 e 2, o chatbot GoodWe/ChargeGrid era implementado como uma sequência manual de chamadas "
    "à API do LLM: uma função Python concatenava o system prompt, o histórico (mantido em uma lista comum) e "
    "a pergunta do usuário a cada turno, sem orquestração formal, sem guardrails testados sistematicamente e "
    "sem comparação objetiva entre modelos. Na Sprint 03, o núcleo conversacional foi refatorado para usar o "
    "framework de agentes <b>LangGraph</b>: o fluxo passou a ser modelado como um grafo de estados "
    "(<i>StateGraph</i>), a memória por sessão passou a ser gerenciada por um checkpointer nativo "
    "(<i>MemorySaver</i>), e uma suíte automatizada de testes funcionais, de memória e de segurança passou a "
    "ser executada contra múltiplos provedores de LLM (OpenAI e Google Gemini), com resultados exportados para "
    "<font face='Courier'>relatorio_modelos.md</font>.", styles["Body"]))

# 7.2 Refatoração
story.append(Paragraph("2. Refatoração — decisões técnicas e trade-offs", styles["H1"]))
story.append(Paragraph(
    "<b>Framework escolhido:</b> LangGraph, por permitir modelar o agente como grafo de estados, oferecer "
    "checkpointer nativo para memória por sessão e ser agnóstico ao provedor de LLM (bastando trocar o objeto "
    "<i>ChatModel</i> injetado no nó do agente). Essa escolha viabilizou diretamente o requisito de comparação "
    "entre modelos, já que a mesma orquestração roda tanto sobre <font face='Courier'>ChatOpenAI</font> quanto "
    "sobre <font face='Courier'>ChatGoogleGenerativeAI</font>.", styles["Body"]))
story.append(Paragraph(
    "<b>Principais trade-offs:</b> (1) curva de aprendizado maior do que a versão manual das Sprints 1/2; "
    "(2) o checkpointer padrão (<i>MemorySaver</i>) mantém a memória apenas em RAM — suficiente para a "
    "demonstração da sprint, mas não persistente entre reinícios do kernel; (3) depender de uma biblioteca "
    "de terceiros introduz risco de <i>breaking changes</i> entre versões, mitigado fixando as versões no "
    "<font face='Courier'>pip install</font>.", styles["Body"]))

# 7.3 Comparativo antes x depois
story.append(Paragraph("3. Comparativo antes × depois", styles["H1"]))

tabela_dados = [["Aspecto", "Sprints 1/2 (manual)", "Sprint 03 (LangGraph)"]]
for k in metricas_antes:
    tabela_dados.append([k, metricas_antes[k], metricas_depois[k]])

tabela = Table(tabela_dados, colWidths=[3.0 * cm, 6.3 * cm, 6.3 * cm])
tabela.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5b21b6")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 7.5),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f0fa")]),
]))
story.append(tabela)
story.append(Spacer(1, 8))

# Tabela de métricas quantitativas da suíte
story.append(Paragraph("Resultados quantitativos da suíte automatizada (execução real, Seção 7 do notebook):", styles["Body"]))
metricas_tab = [["Modelo/config.", "Latência média (s)", "Tokens médios (aprox.)", "Taxa de sucesso"]]
for idx, row in resumo.reset_index().iterrows():
    metricas_tab.append([row["modelo"], row["latencia_media_s"], row["tokens_medio"], row["taxa_sucesso"]])
tabela2 = Table(metricas_tab, colWidths=[4.5 * cm, 3.7 * cm, 3.7 * cm, 3.7 * cm])
tabela2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5b21b6")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f0fa")]),
]))
story.append(tabela2)
story.append(Spacer(1, 6))
story.append(Paragraph(
    f"<b>Modelo escolhido para a versão final: {melhor_modelo}</b>, com base na maior taxa de sucesso "
    "combinada (testes funcionais + memória + segurança) da suíte automatizada — decisão orientada por dados, "
    "e não por preferência do grupo. Detalhamento completo em "
    "<font face='Courier'>relatorio_modelos.md</font>.", styles["Body"]))

story.append(PageBreak())

# 7.4 Problemas encontrados e soluções
story.append(Paragraph("4. Problemas encontrados e soluções", styles["H1"]))

problemas = [
    ("Problema 1 — Memória perdida entre execuções de célula",
     "Alternativas: (a) variável global manual; (b) checkpointer persistente em disco/banco; "
     "(c) MemorySaver do LangGraph em RAM.",
     "Adotado (c): MemorySaver indexado por thread_id.",
     "Atende ao requisito de memória por sessão com baixa complexidade; persistência em disco fica fora do "
     "escopo de uma demonstração local."),
    ("Problema 2 — Avaliar guardrails de forma objetiva",
     "Alternativas: (a) leitura manual de cada resposta; (b) um segundo LLM como juiz; "
     "(c) checagem determinística por palavras-chave.",
     "Adotado (c): heurística por palavras-chave, com revisão manual dos casos sinalizados.",
     "Reprodutível e sem custo/latência extra de um LLM avaliador; suficiente para o volume de testes da sprint."),
    ("Problema 3 — Comparar modelos de provedores diferentes de forma justa",
     "Alternativas: (a) comparação subjetiva 'na sensação'; (b) mesma suíte e mesmos parâmetros para "
     "todos os provedores, variando só o modelo.",
     "Adotado (b): suíte e parâmetros fixos, com experimento isolado de temperature.",
     "Garante que diferenças observadas sejam atribuíveis ao modelo, não a perguntas/parâmetros distintos, "
     "tornando a escolha final defensável com dados."),
]
for titulo, alt, sol, just in problemas:
    story.append(Paragraph(f"<b>{titulo}</b>", styles["H2"]))
    story.append(Paragraph(f"<b>Alternativas consideradas:</b> {alt}", styles["Body"]))
    story.append(Paragraph(f"<b>Solução adotada:</b> {sol}", styles["Body"]))
    story.append(Paragraph(f"<b>Justificativa:</b> {just}", styles["Body"]))
    story.append(Spacer(1, 4))

# 7.5 Divisão da equipe
story.append(Paragraph("5. Divisão da equipe", styles["H1"]))
equipe_tab = [
    ["Nome", "RM", "Principal responsabilidade"],
    ["Renan Fracalossi Mano da Silva", "569610", "Engenharia de Agentes (Dev Core) — arquitetura LangGraph e memória"],
    ["Gabriel Barbosa Furin", "572941", "Guardrails e testes de segurança (Prompt Injection e escopo)"],
    ["Gabriel de Almeida Santos", "569395", "Comparação entre modelos — harness de testes e relatorio_modelos.md"],
    ["Herbert Soares de Jesus", "571507", "Interface de chat e integração da base de conhecimento"],
    ["Lucas Kiodi Moraca", "571004", "Documentação, comparativo antes × depois e relatório de evolução"],
]
tabela3 = Table(equipe_tab, colWidths=[5.5 * cm, 2.0 * cm, 8.4 * cm])
tabela3.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5b21b6")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f0fa")]),
]))
story.append(tabela3)
story.append(Spacer(1, 10))
story.append(Paragraph(
    "Relatório gerado automaticamente a partir dos resultados reais da execução da Seção 7 deste notebook.",
    styles["Small"]))

doc = SimpleDocTemplate(
    "relatorio_evolucao.pdf", pagesize=A4,
    leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm,
)
doc.build(story)
print("relatorio_evolucao.pdf gerado com sucesso.")
