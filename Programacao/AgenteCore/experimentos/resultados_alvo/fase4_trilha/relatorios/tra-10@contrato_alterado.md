<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-10@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-10@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `chave_de_juncao_errada` · **CAMPO:** `cpf` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê uma reserva associada ao administrador em vez do cliente esperado.`

Justificativa (gerada por molde): O agente respondeu chave_de_juncao_errada no campo cpf porque o sinal id_pedido: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes contrato-pedido, pedido-reserva, usuario-e-login estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3116): regras diff_contra_contrato; antes {"chars": 126}, depois {"chars": 126}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id_pedido | texto | inteiro |

Trecho podado (hash `d940d8436b0dee35`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "admin"}]
```

## 3. Contraste com a segunda causa

chave_de_juncao_errada e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-pedido, pedido-reserva, usuario-e-login

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| chave_de_juncao_errada | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| registro_duplicado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[usuario-e-login], [pedido-reserva]`; verbetes citados: `usuario-e-login`, `pedido-reserva`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `usuario-e-login` | confere |  |
| O verbete citado existe na biblioteca | `pedido-reserva` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `usuario-e-login` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `usuario-e-login` |
| O verbete citado estava no contexto entregue ao modelo | `pedido-reserva` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `usuario-e-login` |
| Algum verbete do contexto trata da causa respondida | `chave_de_juncao_errada` | confere | verbetes: `pedido-reserva`, `usuario-e-login` |
| fonte_formato_valido | `[usuario-e-login], [pedido-reserva]` | confere | {"ids": ["usuario-e-login", "pedido-reserva"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `usuario-e-login` | **não confere** | {"termo": "chave_de_juncao_errada"} |
| fonte_contem_termo_da_causa | `pedido-reserva` | **não confere** | {"termo": "chave_de_juncao_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `cpf` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-10 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3115 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:52:35 | caso tra-10@contrato_alterado |
| 3116 | 2 | poda | programa | ao_vivo | 2026-11-05T01:52:35 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3117 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:52:35 | poda: escolha json/lista; id_pedido:tipo_diferente; divergência não |
| 3118 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:52:35 | 3 de 39 verbetes entregues |
| 3119 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:52:35 | recuperacao: escolha contrato-pedido,pedido-reserva,usuario-e-login; divergência não |
| 3121 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:52:35 | {"etapa": "diagnostico", "sha": "e23cc67ecc9095f2", "prompt_sha256": "e23cc67ecc90", "chars": 3343, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3123 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:52:35 | diagnostico: 35,4 s |
| 3124 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:52:35 | causa_raiz: `chave_de_juncao_errada` |
| 3125 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:52:35 | campo: `cpf` |
| 3126 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:52:35 | impacto: `O usuário vê uma reserva associada ao administrador em vez do cliente esperado.` |
| 3127 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:52:35 | fonte: `[usuario-e-login], [pedido-reserva]` |
| 3128 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:52:35 | fonte_citada: `usuario-e-login` |
| 3129 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T01:52:35 | fonte_citada: `pedido-reserva` |
| 3130 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | quatro_linhas_presentes: confere |
| 3131 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | rotulo_no_conjunto: confere |
| 3132 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | fonte_existe_na_biblioteca: confere |
| 3133 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | fonte_existe_na_biblioteca: confere |
| 3134 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | fonte_estava_no_contexto: confere |
| 3135 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | fonte_estava_no_contexto: confere |
| 3136 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | campo_existe_no_caso: confere |
| 3137 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3138 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | notas_nos_verbetes_citados: informativo |
| 3139 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | impacto: nao_verificavel |
| 3140 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | fonte_formato_valido: confere |
| 3141 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | fonte_contem_termo_da_causa: nao_confere |
| 3142 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:35 | fonte_contem_termo_da_causa: nao_confere |
| 3143 | 27 | decisao | programa | ao_vivo | 2026-11-05T01:52:35 | diagnostico: escolha chave_de_juncao_errada; divergência não |

</details>

Nós de decisão:

- evento 3117, `poda`: escolha `json/lista; id_pedido:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 3116 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id_pedido (gen_ai: plan)
- evento 3119, `recuperacao`: escolha `contrato-pedido,pedido-reserva,usuario-e-login`; resultado verbetes_entregues; evidência: evento 3118 (verbete_entregue, contrato-pedido), evento 3118 (verbete_entregue, pedido-reserva), evento 3118 (verbete_entregue, usuario-e-login); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, usuario-e-login (gen_ai: retrieval)
- evento 3143, `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido; evidência: evento 3116 (sinal_em_codigo), evento 3118 (verbete_entregue, contrato-pedido), evento 3118 (verbete_entregue, pedido-reserva), evento 3118 (verbete_entregue, usuario-e-login), evento 3123 (resposta), evento 3128 (verbete_citado, usuario-e-login), evento 3129 (verbete_citado, pedido-reserva); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, usuario-e-login (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3115 a 3143 da trilha; hash dos eventos deste caso: `ea8467735438d542`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
