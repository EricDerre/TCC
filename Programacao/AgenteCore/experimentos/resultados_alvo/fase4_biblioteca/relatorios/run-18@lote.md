<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-18`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-18@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `limite_de_requisicoes` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,77)

**IMPACTO (declarado):** `O usuário recebe um erro 429 indicando que excedeu o limite de requisições, impedindo a criação da reserva.`

Justificativa (gerada por molde): O agente respondeu limite_de_requisicoes porque os verbetes limite_de_requisicoes, fluxo-reserva-e-cancelamento, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,77); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos (6a tentativa de reserva no mesmo minuto)

STATUS HTTP: 429

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
{"detail": "too many requests"}

SINTOMA OBSERVADO: Ao tentar confirmar a reserva varias vezes seguidas em pouco tempo, a API passa a recusar com 429; a reserva nao chega a ser criada.
```

## 3. Contraste com a segunda causa

limite_de_requisicoes e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,77 contra 0,00; verbete(s) na evidência: limite_de_requisicoes, fluxo-reserva-e-cancelamento, tempo_de_resposta_excedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| limite_de_requisicoes | 0,77 | sim |
| tempo_de_resposta_excedido | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[limite_de_requisicoes]`; verbetes citados: `limite_de_requisicoes`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `limite_de_requisicoes` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `limite_de_requisicoes` | confere | contexto: `limite_de_requisicoes`, `fluxo-reserva-e-cancelamento`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `limite_de_requisicoes` | confere | verbetes: `limite_de_requisicoes`, `tempo_de_resposta_excedido` |
| fonte_formato_valido | `[limite_de_requisicoes]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["limite_de_requisicoes"]} |
| fonte_contem_termo_da_causa | `limite_de_requisicoes` | confere | {"termo": "limite_de_requisicoes"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2623 | 1 | entrada | programa | ao_vivo | 2026-11-04T01:06:59 | caso run-18 |
| 2624 | 2 | candidatos | programa | ao_vivo | 2026-11-04T01:06:59 | 3 de 46 verbetes entregues |
| 2626 | 3 | prompt | programa | ao_vivo | 2026-11-04T01:06:59 | {"chars": 3460, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "cca946eeaa90", "sha": "cca946eeaa906482"} |
| 2628 | 4 | inferencia | programa | ao_vivo | 2026-11-04T01:06:59 | diagnostico: 66,9 s |
| 2629 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T01:06:59 | causa_raiz: `limite_de_requisicoes` |
| 2630 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T01:06:59 | campo: `nenhum` |
| 2631 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T01:06:59 | impacto: `O usuário recebe um erro 429 indicando que excedeu o limite de requisições, impedindo a criação da reserva.` |
| 2632 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T01:06:59 | fonte: `[limite_de_requisicoes]` |
| 2633 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T01:06:59 | fonte_citada: `limite_de_requisicoes` |
| 2634 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T01:06:59 | quatro_linhas_presentes: confere |
| 2635 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T01:06:59 | rotulo_no_conjunto: confere |
| 2636 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T01:06:59 | fonte_existe_na_biblioteca: confere |
| 2637 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T01:06:59 | fonte_estava_no_contexto: confere |
| 2638 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T01:06:59 | campo_existe_no_caso: nao_se_aplica |
| 2639 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T01:06:59 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2640 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T01:06:59 | notas_nos_verbetes_citados: informativo |
| 2641 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T01:06:59 | impacto: nao_verificavel |
| 2642 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T01:06:59 | fonte_formato_valido: confere |
| 2643 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T01:06:59 | fonte_contem_termo_da_causa: confere |
| 2644 | 20 | decisao | programa | ao_vivo | 2026-11-04T01:06:59 | diagnostico: escolha limite_de_requisicoes; divergência não |

</details>

Nós de decisão:

- evento 2644, `diagnostico`: escolha `limite_de_requisicoes`; resultado rotulo_emitido; evidência: evento 2624 (verbete_entregue, limite_de_requisicoes), evento 2624 (verbete_entregue, fluxo-reserva-e-cancelamento), evento 2624 (verbete_entregue, tempo_de_resposta_excedido), evento 2628 (resposta), evento 2633 (verbete_citado, limite_de_requisicoes); divergência: não; falha: nenhuma; prov.used: limite_de_requisicoes, fluxo-reserva-e-cancelamento, tempo_de_resposta_excedido (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2623 a 2644 da trilha; hash dos eventos deste caso: `0fd53247019d4df3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
