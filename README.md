# BIA Financeira - Assistente Virtual com IA

Projeto criado para o Lab "Construa Seu Assistente Virtual Com Inteligência Artificial", do bootcamp DIO em parceria com o Santander.

## Tema

A BIA Financeira é um protótipo de assistente virtual educativo para ajudar uma pessoa a entender seus gastos, organizar uma reserva de emergência e decidir o próximo passo de planejamento financeiro.

O objetivo não é substituir um consultor financeiro. A proposta é mostrar como um agente pode usar uma base de conhecimento pequena, responder com clareza e reconhecer quando não tem informação suficiente.

## Diferencial do projeto

O diferencial da BIA Financeira e o **Diagnostico Financeiro Inteligente**.

Com o comando `diagnostico`, o assistente calcula entradas, saidas, saldo, percentual da renda comprometida, progresso da reserva de emergencia e uma classificacao simples da situacao financeira: `saudavel`, `atencao` ou `critico`.

Esse recurso transforma os dados mockados em uma leitura pratica para a pessoa decidir o proximo passo.

## Para quem serve

Este assistente foi pensado para pessoas iniciantes em organização financeira que querem:

- Entender para onde o dinheiro está indo.
- Identificar categorias de maior gasto.
- Organizar uma meta de reserva de emergência.
- Receber orientações simples com base em dados mockados.
- Evitar respostas inventadas sobre produtos, taxas ou recomendações.

A BIA tambem ajuda a fazer um diagnostico simples da propria situacao financeira.

## Como funciona

O protótipo lê arquivos da pasta `data/`:

- `transacoes.csv`: histórico simples de receitas e despesas.
- `historico_atendimento.csv`: dúvidas e atendimentos anteriores.
- `perfil_investidor.json`: perfil financeiro fictício.
- `produtos_financeiros.json`: produtos educativos disponíveis na base.

A aplicação em `src/app.py` interpreta perguntas por palavras-chave, consulta a base local e responde de forma simples. Quando a pergunta foge da base de conhecimento, o assistente informa a limitação.

## Estrutura

```text
assistente-virtual-ia/
  README.md
  data/
  docs/
  src/
```

## Como executar

Requisitos:

- Python 3.10 ou superior.
- Não precisa instalar bibliotecas externas.

Executar em modo conversa continua:

```bash
python src/app.py
```

Depois disso, faca quantas perguntas quiser. Para encerrar, digite:

```text
sair
```

Executar uma pergunta direta:

```bash
python src/app.py --pergunta "Quais foram meus maiores gastos?"
```

## Exemplos de perguntas

- "Faca meu diagnostico financeiro"
- "Quais foram meus maiores gastos?"
- "Como está minha reserva de emergência?"
- "Qual produto combina com meu perfil?"
- "O que eu já perguntei em atendimentos anteriores?"
- "Qual é a cotação do dólar hoje?"

Na última pergunta, o assistente deve dizer que não tem informação suficiente, porque esse dado não está na base.

## Os 6 passos do desafio

1. Documentação do agente: arquivo `docs/01-documentacao-agente.md`.
2. Base de conhecimento: arquivo `docs/02-base-conhecimento.md` e dados em `data/`.
3. Prompts do agente: arquivo `docs/03-prompts.md`.
4. Aplicação funcional: arquivo `src/app.py`.
5. Avaliação e métricas: arquivo `docs/04-metricas.md`.
6. Pitch final: arquivo `docs/05-pitch.md`.

## Próximas melhorias

- Conectar a aplicação a uma API de LLM.
- Criar interface em Streamlit ou Gradio.
- Aumentar a base de conhecimento com mais cenários.
- Criar testes automatizados para medir qualidade das respostas.
