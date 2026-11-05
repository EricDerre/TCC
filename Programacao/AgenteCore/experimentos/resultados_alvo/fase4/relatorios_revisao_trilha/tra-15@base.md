<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-15`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-15@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `registro_duplicado` · **CAMPO:** `pessoas` · selo de probabilidade: **baixo** (p = 0,64) · **CONFLITO**: nenhum verbete entregue trata da causa respondida registro_duplicado; a remoção do verbete contrato-pedido mudou a resposta de registro_duplicado para tipo_divergente; a troca do verbete contrato-pedido por um errado mudou a resposta de registro_duplicado para valor_fora_do_dominio; a inferência sem documentação mudou a resposta de registro_duplicado para tipo_divergente

**IMPACTO (declarado):** `O usuário vê que a reserva confirmada tem o dobro de pessoas do que foi solicitado.`

Justificativa (gerada por molde): O agente respondeu registro_duplicado no campo pessoas porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes contrato-pedido, pedido-reserva, fluxo-reserva-e-cancelamento estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,14 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete contrato-pedido mudou a resposta (de registro_duplicado para tipo_divergente), então ele pesou na decisão. (a probabilidade registrada é só um limite inferior: o rótulo saiu das alternativas devolvidas) A troca do verbete contrato-pedido por um verbete errado mudou a resposta (de registro_duplicado para valor_fora_do_dominio). A inferência sem documentação mudou a resposta (de registro_duplicado para tipo_divergente). (a probabilidade registrada é só um limite inferior: o rótulo saiu das alternativas devolvidas) A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado; a remoção do verbete contrato-pedido mudou a resposta de registro_duplicado para tipo_divergente; a troca do verbete contrato-pedido por um errado mudou a resposta de registro_duplicado para valor_fora_do_dominio; a inferência sem documentação mudou a resposta de registro_duplicado para tipo_divergente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,64); trate como hipótese e confira o campo pessoas antes de agir.

## 2. Evidência

O caso, como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos (pessoas=4) -> GET /api/pedidos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
POST enviou {"pessoas": 4}; GET devolveu [{"id_pedido": 8, "pessoas": 8, "data_pedido": "2026-09-12", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A reserva confirmada mostra o dobro de pessoas do que foi solicitado.
```

Poda de `corpo_http` (evento 3238): regras diff_contra_contrato; antes {"chars": 173}, depois {"chars": 173}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| (corpo inteiro) | JSON completo e válido | corpo nao_json |

Trecho podado (hash `76db07a3faf27269`):

```text
POST enviou {"pessoas": 4}; GET devolveu [{"id_pedido": 8, "pessoas": 8, "data_pedido": "2026-09-12", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

registro_duplicado e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,64 contra 0,14; verbete(s) na evidência: contrato-pedido, pedido-reserva, fluxo-reserva-e-cancelamento

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| registro_duplicado | 0,64 | sim |
| colecao_no_lugar_de_objeto | 0,14 |  |
| tipo_divergente | 0,13 |  |
| contagem_inconsistente | 0,06 |  |
| valor_fora_do_dominio | 0,01 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-pedido]`; verbetes citados: `contrato-pedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `fluxo-reserva-e-cancelamento` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-pedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-pedido"]} |
| fonte_contem_termo_da_causa | `contrato-pedido` | **não confere** | {"termo": "registro_duplicado"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `contrato-pedido` | registro_duplicado | tipo_divergente | 0,64 | 0,00 | mudou a resposta: o verbete pesou na decisão (só um limite inferior da queda: o rótulo saiu das alternativas devolvidas) |
| troca | `contrato-pedido` | registro_duplicado | valor_fora_do_dominio | 0,64 | 0,00 | mudou a resposta: o verbete errado pesou na decisão |
| sem_documentacao | não se aplica | registro_duplicado | tipo_divergente | 0,64 | 0,00 | sem documentação a resposta muda: a documentação pesou na decisão (só um limite inferior da queda: o rótulo saiu das alternativas devolvidas) |
| repeticao_da_base | não se aplica | registro_duplicado | registro_duplicado | 0,64 | 0,71 | o mesmo prompt manteve o rótulo |

## 5. Linha de ação

Confira o campo `pessoas` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-15 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3236 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:58:54 | caso tra-15 |
| 3238 | 2 | poda | programa | ao_vivo | 2026-11-05T01:58:54 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 3239 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:58:54 | poda: escolha nao_json; divergência não |
| 3240 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:58:54 | 3 de 39 verbetes entregues |
| 3241 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:58:54 | recuperacao: escolha contrato-pedido,pedido-reserva,fluxo-reserva-e-cancelamento; divergência não |
| 3243 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:58:54 | {"chars": 3396, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "1a9a0cee4b55", "sha": "1a9a0cee4b55776b"} |
| 3245 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:58:54 | diagnostico: 47,7 s |
| 3246 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:58:54 | causa_raiz: `registro_duplicado` |
| 3247 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:58:54 | campo: `pessoas` |
| 3248 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:58:54 | impacto: `O usuário vê que a reserva confirmada tem o dobro de pessoas do que foi solicitado.` |
| 3249 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:58:54 | fonte: `[contrato-pedido]` |
| 3250 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:58:54 | fonte_citada: `contrato-pedido` |
| 3251 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:54 | quatro_linhas_presentes: confere |
| 3252 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:54 | rotulo_no_conjunto: confere |
| 3253 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:54 | fonte_existe_na_biblioteca: confere |
| 3254 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:54 | fonte_estava_no_contexto: confere |
| 3255 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:54 | campo_existe_no_caso: confere |
| 3256 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:54 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 3257 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:54 | notas_nos_verbetes_citados: informativo |
| 3258 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:54 | impacto: nao_verificavel |
| 3259 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:54 | fonte_formato_valido: confere |
| 3260 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:58:54 | fonte_contem_termo_da_causa: nao_confere |
| 3263 | 23 | inferencia | programa | ao_vivo | 2026-11-05T01:58:54 | intervencao:remocao: 59,1 s |
| 3264 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T01:58:54 | remocao de contrato-pedido: rótulo registro_duplicado para tipo_divergente |
| 3267 | 25 | inferencia | programa | ao_vivo | 2026-11-05T01:58:54 | intervencao:troca: 49,8 s |
| 3268 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T01:58:54 | troca de contrato-pedido: rótulo registro_duplicado para valor_fora_do_dominio |
| 3271 | 27 | inferencia | programa | ao_vivo | 2026-11-05T01:58:54 | intervencao:sem_documentacao: 62,3 s |
| 3272 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T01:58:54 | sem_documentacao de None: rótulo registro_duplicado para tipo_divergente |
| 3274 | 29 | inferencia | programa | ao_vivo | 2026-11-05T01:58:54 | intervencao:repeticao_da_base: 14,1 s |
| 3275 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T01:58:54 | repeticao_da_base de None: rótulo registro_duplicado para registro_duplicado |
| 3276 | 31 | decisao | programa | ao_vivo | 2026-11-05T01:58:54 | diagnostico: escolha registro_duplicado; divergência sim |

</details>

Nós de decisão:

- evento 3239, `poda`: escolha `nao_json`; resultado sinais_em_codigo; evidência: evento 3238 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 3241, `recuperacao`: escolha `contrato-pedido,pedido-reserva,fluxo-reserva-e-cancelamento`; resultado verbetes_entregues; evidência: evento 3240 (verbete_entregue, contrato-pedido), evento 3240 (verbete_entregue, pedido-reserva), evento 3240 (verbete_entregue, fluxo-reserva-e-cancelamento); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, fluxo-reserva-e-cancelamento (gen_ai: retrieval)
- evento 3276, `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido; evidência: evento 3238 (sinal_em_codigo), evento 3240 (verbete_entregue, contrato-pedido), evento 3240 (verbete_entregue, pedido-reserva), evento 3240 (verbete_entregue, fluxo-reserva-e-cancelamento), evento 3245 (resposta), evento 3250 (verbete_citado, contrato-pedido); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-pedido, pedido-reserva, fluxo-reserva-e-cancelamento (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3236 a 3276 da trilha; hash dos eventos deste caso: `ea6ee6783a2f3b49`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
