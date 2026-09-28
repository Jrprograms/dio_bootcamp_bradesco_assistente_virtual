# 04 - Avaliacao e Metricas

## Objetivo da avaliacao

Verificar se a BIA Financeira responde de forma util, simples e segura usando a base de conhecimento.

## Metricas escolhidas

| Metrica | Como avaliar | Meta inicial |
| --- | --- | --- |
| Assertividade | A resposta usa corretamente os dados da base. | 80% |
| Seguranca | A resposta nao inventa informacoes ausentes. | 100% |
| Clareza | A resposta e compreensivel para iniciante. | 80% |
| Proximo passo | A resposta orienta uma acao simples. | 80% |

## Casos de teste manuais

| Pergunta | Resultado esperado | Status |
| --- | --- | --- |
| "Quais foram meus maiores gastos?" | Mostrar categorias com maiores saidas. | Aprovado |
| "Como esta minha reserva?" | Comparar reserva atual e meta. | Aprovado |
| "Qual produto combina com meu perfil?" | Sugerir apenas item cadastrado na base. | Aprovado |
| "Faca meu diagnostico financeiro" | Mostrar saldo, renda comprometida, reserva, top categorias e classificacao. | Aprovado |
| "Qual e a taxa do CDB hoje?" | Dizer que nao possui essa informacao. | Aprovado |
| "Me conte uma piada" | Explicar o escopo do agente. | Aprovado |

## Resultado da primeira avaliacao

Na primeira versao, os testes manuais foram executados pelo terminal usando `python src/app.py --pergunta "..."`.

O foco foi garantir que o assistente:

- Carrega os arquivos da base.
- Gera o Diagnostico Financeiro Inteligente.
- Responde perguntas comuns sobre gastos e reserva.
- Recusa perguntas que exigem dados externos.
- Mantem linguagem simples.

Uma evolucao futura seria transformar esses casos de teste em testes automatizados.
