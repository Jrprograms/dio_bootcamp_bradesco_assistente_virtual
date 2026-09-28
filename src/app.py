import argparse
import csv
import json
import unicodedata
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def format_brl(value):
    formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted}"


def normalize(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def load_transactions():
    path = DATA_DIR / "transacoes.csv"
    with path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    for row in rows:
        row["valor"] = float(row["valor"])

    return rows


def load_csv(name):
    path = DATA_DIR / name
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_json(name):
    path = DATA_DIR / name
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def build_context():
    return {
        "transacoes": load_transactions(),
        "historico": load_csv("historico_atendimento.csv"),
        "perfil": load_json("perfil_investidor.json"),
        "produtos": load_json("produtos_financeiros.json"),
    }


def summarize_spending(transactions):
    totals = defaultdict(float)
    total_out = 0.0
    total_in = 0.0

    for transaction in transactions:
        value = transaction["valor"]
        if transaction["tipo"] == "entrada":
            total_in += value
            continue

        total_out += value
        totals[transaction["categoria"]] += value

    top_categories = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    balance = total_in - total_out
    return total_in, total_out, balance, top_categories


def answer_spending(context):
    total_in, total_out, balance, top_categories = summarize_spending(context["transacoes"])
    category_lines = [
        f"{index}. {category}: {format_brl(value)}"
        for index, (category, value) in enumerate(top_categories[:3], start=1)
    ]

    return (
        "Com base nas transacoes cadastradas, estes foram os maiores grupos de saida:\n"
        + "\n".join(category_lines)
        + f"\n\nEntradas: {format_brl(total_in)} | Saidas: {format_brl(total_out)} | Saldo estimado: {format_brl(balance)}."
        + "\nProximo passo: revise primeiro os gastos variaveis, como alimentacao, lazer e transporte."
    )


def answer_financial_diagnostic(context):
    profile = context["perfil"]
    total_in, total_out, balance, top_categories = summarize_spending(context["transacoes"])
    monthly_income = profile["renda_mensal"]
    expense_ratio = (total_out / monthly_income) * 100 if monthly_income else 0
    reserve_progress = (
        (profile["reserva_atual"] / profile["meta_reserva"]) * 100
        if profile["meta_reserva"]
        else 0
    )

    if balance < 0 or expense_ratio > 100:
        classification = "critico"
        next_step = "reduzir primeiro a maior categoria variavel e evitar novos compromissos neste mes."
    elif expense_ratio > 80 or reserve_progress < 30:
        classification = "atencao"
        next_step = "revisar gastos variaveis e manter um valor fixo mensal para a reserva."
    else:
        classification = "saudavel"
        next_step = "manter o acompanhamento semanal e continuar reforcando a reserva."

    category_lines = [
        f"{index}. {category}: {format_brl(value)}"
        for index, (category, value) in enumerate(top_categories[:3], start=1)
    ]

    return (
        "Diagnostico Financeiro Inteligente\n"
        f"- Entradas cadastradas: {format_brl(total_in)}\n"
        f"- Saidas cadastradas: {format_brl(total_out)}\n"
        f"- Saldo estimado: {format_brl(balance)}\n"
        f"- Renda comprometida com despesas: {expense_ratio:.1f}%\n"
        f"- Progresso da reserva: {reserve_progress:.1f}%\n"
        f"- Classificacao: {classification}\n\n"
        "Top 3 categorias de gasto:\n"
        + "\n".join(category_lines)
        + f"\n\nAcao pratica: {next_step}"
    )


def answer_emergency_fund(context):
    profile = context["perfil"]
    current = profile["reserva_atual"]
    goal = profile["meta_reserva"]
    missing = max(goal - current, 0)
    progress = (current / goal) * 100 if goal else 0
    monthly_needed = missing / profile["horizonte_meses"] if profile["horizonte_meses"] else 0

    return (
        f"Sua reserva atual e {format_brl(current)} e a meta cadastrada e {format_brl(goal)}.\n"
        f"Isso representa {progress:.1f}% da meta. Ainda faltam {format_brl(missing)}.\n"
        f"Para chegar la em {profile['horizonte_meses']} meses, o valor medio seria {format_brl(monthly_needed)} por mes.\n"
        "Proximo passo: separar a reserva logo apos receber a renda ajuda a manter consistencia."
    )


def answer_profile(context):
    profile = context["perfil"]
    preferences = ", ".join(profile["preferencias"])
    return (
        f"O perfil cadastrado e {profile['conhecimento_financeiro']}, com tolerancia a risco {profile['tolerancia_risco']}.\n"
        f"O objetivo principal e: {profile['objetivo_principal']}.\n"
        f"Preferencias registradas: {preferences}.\n"
        "Proximo passo: manter foco em organizacao, liquidez e aprendizado antes de buscar produtos mais complexos."
    )


def answer_products(context):
    profile = context["perfil"]
    products = context["produtos"]
    matching_products = [
        product
        for product in products
        if product["perfil_indicado"] in {profile["conhecimento_financeiro"], "conservador"}
        or product["tipo"] in {"reserva", "educacao", "organizacao"}
    ]

    lines = [
        f"- {product['nome']}: {product['descricao']}"
        for product in matching_products
    ]

    return (
        "Pelo perfil cadastrado, posso citar apenas produtos que estao na base de conhecimento:\n"
        + "\n".join(lines)
        + "\n\nNao tenho taxas, rentabilidades ou condicoes comerciais nesta base."
        + "\nProximo passo: escolher primeiro se a prioridade e organizar gastos, formar reserva ou estudar conceitos basicos."
    )


def answer_history(context):
    history = context["historico"]
    lines = [
        f"- {row['data']} | {row['assunto']}: {row['encaminhamento']}"
        for row in history
    ]

    return (
        "Encontrei estes atendimentos anteriores:\n"
        + "\n".join(lines)
        + "\n\nProximo passo: usar esse historico para nao repetir orientacoes e acompanhar evolucao."
    )


def answer_help():
    return (
        "Menu da BIA Financeira:\n"
        "- diagnostico: gera um resumo da sua saude financeira.\n"
        "- maiores gastos: mostra as categorias com mais saidas.\n"
        "- reserva: compara sua reserva atual com a meta.\n"
        "- produtos: lista opcoes cadastradas na base.\n"
        "- historico: mostra atendimentos anteriores.\n"
        "- sair: encerra a conversa."
    )


def answer_unknown():
    return (
        "Nao tenho informacao suficiente na base de conhecimento para responder isso com seguranca.\n"
        "Posso ajudar melhor se a pergunta for sobre gastos, reserva de emergencia, perfil financeiro ou produtos cadastrados."
    )


def detect_intent(question):
    normalized_question = normalize(question)

    if any(word in normalized_question for word in ["ajuda", "menu", "opcoes", "como usar"]):
        return "menu"

    if any(
        phrase in normalized_question
        for phrase in [
            "diagnostico",
            "saude financeira",
            "como estou financeiramente",
            "resumo",
            "situacao financeira",
        ]
    ):
        return "diagnostico"

    if any(word in normalized_question for word in ["gasto", "despesa", "saida", "categoria", "saldo"]):
        return "gastos"

    if any(word in normalized_question for word in ["reserva", "emergencia", "guardar", "meta"]):
        return "reserva"

    if any(word in normalized_question for word in ["produto", "investimento", "aplicacao", "combina"]):
        if any(word in normalized_question for word in ["taxa", "rende", "rentabilidade", "hoje", "cotacao"]):
            return "desconhecido"
        return "produtos"

    if any(word in normalized_question for word in ["perfil", "risco", "objetivo"]):
        return "perfil"

    if any(word in normalized_question for word in ["atendimento", "historico", "perguntei"]):
        return "historico"

    return "desconhecido"


def generate_response(question, context):
    intent = detect_intent(question)

    if intent == "menu":
        return answer_help()

    if intent == "diagnostico":
        return answer_financial_diagnostic(context)

    if intent == "gastos":
        return answer_spending(context)

    if intent == "reserva":
        return answer_emergency_fund(context)

    if intent == "produtos":
        return answer_products(context)

    if intent == "perfil":
        return answer_profile(context)

    if intent == "historico":
        return answer_history(context)

    return answer_unknown()


def run_chat():
    context = build_context()
    last_intent = None
    answered_questions = 0

    print("BIA Financeira")
    print("Modo conversa iniciado. Faca quantas perguntas quiser e digite 'sair' para encerrar.")
    print(answer_help())

    while True:
        question = input("\nVoce: ").strip()
        if normalize(question) in {"sair", "exit", "quit"}:
            if answered_questions == 0:
                print("BIA: Ate mais. Quando quiser, volte para fazer seu diagnostico financeiro.")
            else:
                print(
                    "BIA: Ate mais. Nesta conversa respondi "
                    f"{answered_questions} pergunta(s). Ultimo tema: {last_intent}. "
                    "Continue acompanhando seus gastos com calma e consistencia."
                )
            break

        intent = detect_intent(question)
        response = generate_response(question, context)
        answered_questions += 1
        last_intent = intent
        print(f"\nBIA: {response}")


def main():
    parser = argparse.ArgumentParser(description="Protótipo da BIA Financeira.")
    parser.add_argument("--pergunta", help="Executa uma pergunta direta e encerra.")
    args = parser.parse_args()

    if args.pergunta:
        context = build_context()
        print(generate_response(args.pergunta, context))
        return

    run_chat()


if __name__ == "__main__":
    main()
