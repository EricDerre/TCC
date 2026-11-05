<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-10`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-10@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `chave_de_juncao_errada` · **CAMPO:** `cpf` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: a inferência sem documentação mudou a resposta de chave_de_juncao_errada para valor_fora_do_dominio

**IMPACTO (declarado):** `O usuário vê uma reserva vinculada ao login do administrador, ao invés do seu próprio CPF.`

Justificativa (gerada por molde): O agente respondeu chave_de_juncao_errada no campo cpf porque os verbetes contrato-pedido, pedido-reserva, usuario-e-login estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. A remoção do verbete contrato-pedido não mudou a resposta: sem efeito medido do contexto. A troca do verbete contrato-pedido por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação mudou a resposta (de chave_de_juncao_errada para valor_fora_do_dominio). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a inferência sem documentação mudou a resposta de chave_de_juncao_errada para valor_fora_do_dominio.

## 2. Evidência

Poda de `corpo_http` (evento 3019): regras diff_contra_contrato; antes {"chars": 126}, depois {"chars": 126}.

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
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

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

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `contrato-pedido` | chave_de_juncao_errada | chave_de_juncao_errada | 1,00 | 1,00 | sem efeito medido do contexto |
| troca | `contrato-pedido` | chave_de_juncao_errada | chave_de_juncao_errada | 1,00 | 1,00 | sem efeito medido do contexto |
| sem_documentacao | `` | chave_de_juncao_errada | valor_fora_do_dominio | 1,00 | 0,16 | mudou a resposta: o verbete pesou na decisão |
| repeticao_da_base | `` | chave_de_juncao_errada | chave_de_juncao_errada | 1,00 | 1,00 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `cpf` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-10 --sem-seletor`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3017 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:47:44 | caso tra-10 |
| 3019 | 2 | poda | programa | ao_vivo | 2026-11-05T01:47:44 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3020 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:47:44 | poda: escolha json/lista; sem diferença; divergência não |
| 3021 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:47:44 | 3 de 39 verbetes entregues |
| 3022 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:47:44 | recuperacao: escolha contrato-pedido,pedido-reserva,usuario-e-login; divergência não |
| 3024 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:47:44 | {"etapa": "diagnostico", "sha": "83f72fa4a787eba2", "prompt_sha256": "83f72fa4a787", "chars": 3345, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3026 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:47:44 | diagnostico: 48,9 s |
| 3027 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:47:44 | causa_raiz: `chave_de_juncao_errada` |
| 3028 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:47:44 | campo: `cpf` |
| 3029 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:47:44 | impacto: `O usuário vê uma reserva vinculada ao login do administrador, ao invés do seu próprio CPF.` |
| 3030 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:47:44 | fonte: `[contrato-pedido], [usuario-e-login]` |
| 3031 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:47:44 | fonte_citada: `contrato-pedido` |
| 3032 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T01:47:44 | fonte_citada: `usuario-e-login` |
| 3033 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | quatro_linhas_presentes: confere |
| 3034 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | rotulo_no_conjunto: confere |
| 3035 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | fonte_existe_na_biblioteca: confere |
| 3036 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | fonte_existe_na_biblioteca: confere |
| 3037 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | fonte_estava_no_contexto: confere |
| 3038 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | fonte_estava_no_contexto: confere |
| 3039 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | campo_existe_no_caso: confere |
| 3040 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3041 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | notas_nos_verbetes_citados: informativo |
| 3042 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | impacto: nao_verificavel |
| 3043 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | fonte_formato_valido: confere |
| 3044 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | fonte_contem_termo_da_causa: nao_confere |
| 3045 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T01:47:44 | fonte_contem_termo_da_causa: nao_confere |
| 3048 | 27 | inferencia | programa | ao_vivo | 2026-11-05T01:47:44 | intervencao:remocao: 54,6 s |
| 3049 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T01:47:44 | remocao de contrato-pedido: rótulo chave_de_juncao_errada para chave_de_juncao_errada |
| 3052 | 29 | inferencia | programa | ao_vivo | 2026-11-05T01:47:44 | intervencao:troca: 62,7 s |
| 3053 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T01:47:44 | troca de contrato-pedido: rótulo chave_de_juncao_errada para chave_de_juncao_errada |
| 3056 | 31 | inferencia | programa | ao_vivo | 2026-11-05T01:47:44 | intervencao:sem_documentacao: 28,6 s |
| 3057 | 32 | intervencao | verificacao | ao_vivo | 2026-11-05T01:47:44 | sem_documentacao de None: rótulo chave_de_juncao_errada para valor_fora_do_dominio |
| 3059 | 33 | inferencia | programa | ao_vivo | 2026-11-05T01:47:44 | intervencao:repeticao_da_base: 15,6 s |
| 3060 | 34 | intervencao | verificacao | ao_vivo | 2026-11-05T01:47:44 | repeticao_da_base de None: rótulo chave_de_juncao_errada para chave_de_juncao_errada |
| 3061 | 35 | decisao | programa | ao_vivo | 2026-11-05T01:47:44 | diagnostico: escolha chave_de_juncao_errada; divergência sim |

</details>

Nós de decisão:

- evento 3020, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 3019 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3022, `recuperacao`: escolha `contrato-pedido,pedido-reserva,usuario-e-login`; resultado verbetes_entregues; evidência: evento 3021 (verbete_entregue, contrato-pedido), evento 3021 (verbete_entregue, pedido-reserva), evento 3021 (verbete_entregue, usuario-e-login); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, usuario-e-login (gen_ai: retrieval)
- evento 3061, `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido; evidência: evento 3021 (verbete_entregue, contrato-pedido), evento 3021 (verbete_entregue, pedido-reserva), evento 3021 (verbete_entregue, usuario-e-login), evento 3026 (resposta), evento 3031 (verbete_citado, contrato-pedido), evento 3032 (verbete_citado, usuario-e-login); divergência: sim; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, usuario-e-login (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3017 a 3061 da trilha; hash dos eventos deste caso: `8b26f696fec187d7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
