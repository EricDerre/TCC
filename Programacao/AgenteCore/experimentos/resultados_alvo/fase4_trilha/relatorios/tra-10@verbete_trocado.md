<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-10@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-10@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `chave_de_juncao_errada` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O nome do cliente aparece como "Cliente Teste" em vez do nome do administrador.`

Justificativa (gerada por molde): O agente respondeu chave_de_juncao_errada no campo nome porque os verbetes estado_da_tela_divergente, pedido-reserva, usuario-e-login estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 3092): regras diff_contra_contrato; antes {"chars": 126}, depois {"chars": 126}.

Trecho podado (hash `d940d8436b0dee35`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "admin"}]
```

## 3. Contraste com a segunda causa

chave_de_juncao_errada e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: estado_da_tela_divergente, pedido-reserva, usuario-e-login

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| chave_de_juncao_errada | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| registro_duplicado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[usuario-e-login]`; verbetes citados: `usuario-e-login`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `usuario-e-login` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `usuario-e-login` | confere | contexto: `estado_da_tela_divergente`, `pedido-reserva`, `usuario-e-login` |
| Algum verbete do contexto trata da causa respondida | `chave_de_juncao_errada` | confere | verbetes: `pedido-reserva`, `usuario-e-login` |
| fonte_formato_valido | `[usuario-e-login]` | confere | {"ids": ["usuario-e-login"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `usuario-e-login` | **não confere** | {"termo": "chave_de_juncao_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-10 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3091 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:52:17 | caso tra-10@verbete_trocado |
| 3092 | 2 | poda | programa | ao_vivo | 2026-11-05T01:52:17 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3093 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:52:17 | poda: escolha json/lista; sem diferença; divergência não |
| 3094 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:52:17 | 3 de 39 verbetes entregues |
| 3095 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:52:17 | recuperacao: escolha estado_da_tela_divergente,pedido-reserva,usuario-e-login; divergência não |
| 3096 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:52:17 | {"etapa": "diagnostico", "sha": "cfa9916ae959528d", "prompt_sha256": "cfa9916ae959", "chars": 3280, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3097 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:52:17 | diagnostico: 13,9 s |
| 3098 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:52:17 | causa_raiz: `chave_de_juncao_errada` |
| 3099 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:52:17 | campo: `nome` |
| 3100 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:52:17 | impacto: `O nome do cliente aparece como "Cliente Teste" em vez do nome do administrador.` |
| 3101 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:52:17 | fonte: `[usuario-e-login]` |
| 3102 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:52:17 | fonte_citada: `usuario-e-login` |
| 3103 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:17 | quatro_linhas_presentes: confere |
| 3104 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:17 | rotulo_no_conjunto: confere |
| 3105 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:17 | fonte_existe_na_biblioteca: confere |
| 3106 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:17 | fonte_estava_no_contexto: confere |
| 3107 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:17 | campo_existe_no_caso: confere |
| 3108 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:17 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3109 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:17 | notas_nos_verbetes_citados: informativo |
| 3110 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:17 | impacto: nao_verificavel |
| 3111 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:17 | fonte_formato_valido: confere |
| 3112 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:52:17 | fonte_contem_termo_da_causa: nao_confere |
| 3113 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:52:17 | diagnostico: escolha chave_de_juncao_errada; divergência não |

</details>

Nós de decisão:

- evento 3093, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 3092 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3095, `recuperacao`: escolha `estado_da_tela_divergente,pedido-reserva,usuario-e-login`; resultado verbetes_entregues; evidência: evento 3094 (verbete_entregue, estado_da_tela_divergente), evento 3094 (verbete_entregue, pedido-reserva), evento 3094 (verbete_entregue, usuario-e-login); divergência: não; falha: nenhuma; prov.used: estado_da_tela_divergente, pedido-reserva, usuario-e-login (gen_ai: retrieval)
- evento 3113, `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido; evidência: evento 3094 (verbete_entregue, estado_da_tela_divergente), evento 3094 (verbete_entregue, pedido-reserva), evento 3094 (verbete_entregue, usuario-e-login), evento 3097 (resposta), evento 3102 (verbete_citado, usuario-e-login); divergência: não; falha: nenhuma; prov.used: estado_da_tela_divergente, pedido-reserva, usuario-e-login (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3091 a 3113 da trilha; hash dos eventos deste caso: `c1491926f4e113d3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
