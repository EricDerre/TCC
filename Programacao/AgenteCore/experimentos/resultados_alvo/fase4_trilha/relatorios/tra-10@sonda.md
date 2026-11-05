<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-10@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-10@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `chave_de_juncao_errada` · **CAMPO:** `login_usuario` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: o campo apontado (login_usuario) não aparece no caso

**IMPACTO (declarado):** `O usuário vê uma reserva vinculada ao login do administrador, ao invés do seu próprio CPF.`

Justificativa (gerada por molde): O agente respondeu chave_de_juncao_errada no campo login_usuario porque os verbetes contrato-pedido, pedido-reserva, usuario-e-login estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): o campo apontado (login_usuario) não aparece no caso. Este nó está marcado com a falha campo_errado (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 3063): regras diff_contra_contrato; antes {"chars": 126}, depois {"chars": 126}.

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
| registro_duplicado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido], [usuario-e-login]`; verbetes citados: `contrato-pedido`, `usuario-e-login`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado existe na biblioteca | `usuario-e-login` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `usuario-e-login` |
| O verbete citado estava no contexto entregue ao modelo | `usuario-e-login` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `usuario-e-login` |
| Algum verbete do contexto trata da causa respondida | `chave_de_juncao_errada` | confere | verbetes: `pedido-reserva`, `usuario-e-login` |
| fonte_formato_valido | `[contrato-pedido], [usuario-e-login]` | confere | {"ids": ["contrato-pedido", "usuario-e-login"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "chave_de_juncao_errada"} |
| fonte_contem_termo_da_causa | `usuario-e-login` | **não confere** | {"termo": "chave_de_juncao_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `login_usuario` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-10 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3062 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:51:19 | caso tra-10@sonda |
| 3063 | 2 | poda | programa | ao_vivo | 2026-11-05T01:51:19 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3064 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:51:19 | poda: escolha json/lista; sem diferença; divergência não |
| 3065 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:51:19 | 3 de 39 verbetes entregues |
| 3066 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:51:19 | recuperacao: escolha contrato-pedido,pedido-reserva,usuario-e-login; divergência não |
| 3068 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:51:19 | {"etapa": "diagnostico", "sha": "82bcc9682a46b2d6", "prompt_sha256": "82bcc9682a46", "chars": 3465, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3070 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:51:19 | diagnostico: 54,5 s |
| 3071 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:51:19 | causa_raiz: `chave_de_juncao_errada` |
| 3072 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:51:19 | campo: `login_usuario` |
| 3073 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:51:19 | impacto: `O usuário vê uma reserva vinculada ao login do administrador, ao invés do seu próprio CPF.` |
| 3074 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:51:19 | fonte: `[contrato-pedido], [usuario-e-login]` |
| 3075 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:51:19 | fonte_citada: `contrato-pedido` |
| 3076 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T01:51:19 | fonte_citada: `usuario-e-login` |
| 3077 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | quatro_linhas_presentes: confere |
| 3078 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | rotulo_no_conjunto: confere |
| 3079 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | fonte_existe_na_biblioteca: confere |
| 3080 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | fonte_existe_na_biblioteca: confere |
| 3081 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | fonte_estava_no_contexto: confere |
| 3082 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | fonte_estava_no_contexto: confere |
| 3083 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | campo_existe_no_caso: nao_confere |
| 3084 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3085 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | notas_nos_verbetes_citados: informativo |
| 3086 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | impacto: nao_verificavel |
| 3087 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | fonte_formato_valido: confere |
| 3088 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | fonte_contem_termo_da_causa: nao_confere |
| 3089 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T01:51:19 | fonte_contem_termo_da_causa: nao_confere |
| 3090 | 27 | decisao | programa | ao_vivo | 2026-11-05T01:51:19 | diagnostico: escolha chave_de_juncao_errada; divergência sim |

</details>

Nós de decisão:

- evento 3064, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 3063 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3066, `recuperacao`: escolha `contrato-pedido,pedido-reserva,usuario-e-login`; resultado verbetes_entregues; evidência: evento 3065 (verbete_entregue, contrato-pedido), evento 3065 (verbete_entregue, pedido-reserva), evento 3065 (verbete_entregue, usuario-e-login); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, usuario-e-login (gen_ai: retrieval)
- evento 3090, `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido; evidência: evento 3065 (verbete_entregue, contrato-pedido), evento 3065 (verbete_entregue, pedido-reserva), evento 3065 (verbete_entregue, usuario-e-login), evento 3070 (resposta), evento 3075 (verbete_citado, contrato-pedido), evento 3076 (verbete_citado, usuario-e-login); divergência: sim; falha: campo_errado; prov.used: contrato-pedido, pedido-reserva, usuario-e-login (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3062 a 3090 da trilha; hash dos eventos deste caso: `b1216ed570f1fa9e`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
