# 02 - Base de Conhecimento

## Objetivo da base

A base de conhecimento guarda informacoes mockadas que o agente usa para responder sem inventar dados.

## Arquivos usados

| Arquivo | Finalidade |
| --- | --- |
| `data/transacoes.csv` | Registrar entradas e saidas do mes. |
| `data/historico_atendimento.csv` | Guardar duvidas anteriores da pessoa usuaria. |
| `data/perfil_investidor.json` | Descrever renda, objetivo, reserva e perfil de risco. |
| `data/produtos_financeiros.json` | Listar produtos educativos que podem ser citados. |

## Dados principais

O perfil ficticio usado no prototipo tem renda mensal de R$ 3.200,00, reserva atual de R$ 1.200,00 e meta de reserva de R$ 9.600,00.

A meta de reserva representa aproximadamente tres meses de renda. Como a tolerancia a risco e baixa, o agente deve priorizar organizacao, liquidez e seguranca.

## Como a base ajuda o agente

- As transacoes permitem calcular saldo, total de despesas e maiores categorias de gasto.
- O perfil orienta o tom e o tipo de sugestao.
- Os produtos limitam o que pode ser recomendado.
- O historico evita repetir orientacoes e ajuda a manter contexto.

## Limitacoes

Esta base e pequena e ficticia. Ela nao contem taxas reais, regulamentos, cotacoes, produtos oficiais do Santander ou informacoes atualizadas de mercado.

Por isso, o agente deve assumir uma postura educativa e transparente.
