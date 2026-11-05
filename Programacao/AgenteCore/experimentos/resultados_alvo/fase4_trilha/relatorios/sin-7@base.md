<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-7`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/sin-7@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `id_pedido` · selo de probabilidade: **medio** (p = 0,91) · **CONFLITO**: a inferência sem documentação mudou a resposta de campo_ausente para tipo_divergente

**IMPACTO (declarado):** `O botão de cancelar reserva não funciona porque o campo `id_pedido` está ausente na resposta da API, impedindo a identificação do pedido a ser cancelado.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo id_pedido porque o sinal id_pedido: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes contrato-pedido, pedido-reserva, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_renomeado, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete contrato-pedido não mudou a resposta: sem efeito medido do contexto. A troca do verbete contrato-pedido por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação mudou a resposta (de campo_ausente para tipo_divergente). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a inferência sem documentação mudou a resposta de campo_ausente para tipo_divergente.

## 2. Evidência

Poda de `corpo_http` (evento 2118): regras diff_contra_contrato; antes {"chars": 116}, depois {"chars": 116}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id_pedido | inteiro |  |

Trecho podado (hash `b88406ab40b56cca`):

```text
[{"pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

campo_ausente e não campo_renomeado: a escolha tem probabilidade 0,91 contra 0,00; verbete(s) na evidência: contrato-pedido, pedido-reserva, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,91 | sim |
| campo_renomeado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| registro_duplicado | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-pedido`, `campo_ausente` |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"ids": ["contrato-pedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "campo_ausente"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `contrato-pedido` | campo_ausente | campo_ausente | 0,91 | 1,00 | sem efeito medido do contexto |
| troca | `contrato-pedido` | campo_ausente | campo_ausente | 0,91 | 1,00 | sem efeito medido do contexto |
| sem_documentacao | `` | campo_ausente | tipo_divergente | 0,91 | 0,08 | mudou a resposta: o verbete pesou na decisão |
| repeticao_da_base | `` | campo_ausente | campo_ausente | 0,91 | 0,88 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `id_pedido` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids sin-7 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2116 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:02:40 | caso sin-7 |
| 2118 | 2 | poda | programa | ao_vivo | 2026-11-05T01:02:40 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2119 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:02:40 | poda: escolha json/lista; id_pedido:ausente; divergência não |
| 2120 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:02:40 | 3 de 39 verbetes entregues |
| 2121 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:02:40 | recuperacao: escolha contrato-pedido,pedido-reserva,campo_ausente; divergência não |
| 2123 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:02:40 | {"etapa": "diagnostico", "sha": "47120d5b142238cf", "prompt_sha256": "47120d5b1422", "chars": 3372, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2125 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:02:40 | diagnostico: 66,0 s |
| 2126 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:02:40 | causa_raiz: `campo_ausente` |
| 2127 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:02:40 | campo: `id_pedido` |
| 2128 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:02:40 | impacto: `O botão de cancelar reserva não funciona porque o campo `id_pedido` está ausente na resposta da API, impedindo a identificação do pedido a ser cancelado.` |
| 2129 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:02:40 | fonte: `[contrato-pedido]` |
| 2130 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:02:40 | fonte_citada: `contrato-pedido` |
| 2131 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:02:40 | quatro_linhas_presentes: confere |
| 2132 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:02:40 | rotulo_no_conjunto: confere |
| 2133 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:02:40 | fonte_existe_na_biblioteca: confere |
| 2134 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:02:40 | fonte_estava_no_contexto: confere |
| 2135 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:02:40 | campo_existe_no_caso: confere |
| 2136 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:02:40 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2137 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:02:40 | notas_nos_verbetes_citados: informativo |
| 2138 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:02:40 | impacto: nao_verificavel |
| 2139 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:02:40 | fonte_formato_valido: confere |
| 2140 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:02:40 | fonte_contem_termo_da_causa: nao_confere |
| 2143 | 23 | inferencia | programa | ao_vivo | 2026-11-05T01:02:40 | intervencao:remocao: 59,1 s |
| 2144 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T01:02:40 | remocao de contrato-pedido: rótulo campo_ausente para campo_ausente |
| 2147 | 25 | inferencia | programa | ao_vivo | 2026-11-05T01:02:40 | intervencao:troca: 68,5 s |
| 2148 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T01:02:40 | troca de contrato-pedido: rótulo campo_ausente para campo_ausente |
| 2151 | 27 | inferencia | programa | ao_vivo | 2026-11-05T01:02:40 | intervencao:sem_documentacao: 48,8 s |
| 2152 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T01:02:40 | sem_documentacao de None: rótulo campo_ausente para tipo_divergente |
| 2154 | 29 | inferencia | programa | ao_vivo | 2026-11-05T01:02:40 | intervencao:repeticao_da_base: 17,2 s |
| 2155 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T01:02:40 | repeticao_da_base de None: rótulo campo_ausente para campo_ausente |
| 2156 | 31 | decisao | programa | ao_vivo | 2026-11-05T01:02:40 | diagnostico: escolha campo_ausente; divergência sim |

</details>

Nós de decisão:

- evento 2119, `poda`: escolha `json/lista; id_pedido:ausente`; resultado sinais_em_codigo; evidência: evento 2118 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id_pedido (gen_ai: plan)
- evento 2121, `recuperacao`: escolha `contrato-pedido,pedido-reserva,campo_ausente`; resultado verbetes_entregues; evidência: evento 2120 (verbete_entregue, contrato-pedido), evento 2120 (verbete_entregue, pedido-reserva), evento 2120 (verbete_entregue, campo_ausente); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, campo_ausente (gen_ai: retrieval)
- evento 2156, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 2118 (sinal_em_codigo), evento 2120 (verbete_entregue, contrato-pedido), evento 2120 (verbete_entregue, pedido-reserva), evento 2120 (verbete_entregue, campo_ausente), evento 2125 (resposta), evento 2130 (verbete_citado, contrato-pedido); divergência: sim; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2116 a 2156 da trilha; hash dos eventos deste caso: `e7c4e2a87ed1cdad`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
