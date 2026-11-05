<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-2`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-2@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nome_nulo_vindo_da_view` · **CAMPO:** `nome` · selo de probabilidade: **medio** (p = 0,85) · **CONFLITO**: a causa respondida nome_nulo_vindo_da_view está fora das 23 permitidas; nenhum verbete entregue trata da causa respondida nome_nulo_vindo_da_view

**IMPACTO (declarado):** `O usuário vê o nome do administrador em vez do seu próprio nome na reserva.`

Justificativa (gerada por molde): O agente respondeu nome_nulo_vindo_da_view no campo nome porque os verbetes usuario-e-login, contrato-pedido, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,08. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a causa respondida nome_nulo_vindo_da_view está fora das 23 permitidas; nenhum verbete entregue trata da causa respondida nome_nulo_vindo_da_view. Este nó está marcado com a falha rotulo_fora_da_taxonomia (origem: modelo).

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (arquivo_inexistente) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso tra-2. A proposta 1 (retificacao em [chave_de_juncao_errada]) foi recusada por a validação da Fase 3 com o código arquivo_inexistente: ARQUIVOS cita 'cliente/index.php': ambíguo: 3 arquivos com esse nome em Programacao/.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `chave_de_juncao_errada` | recusada: `arquivo_inexistente` | nenhum | recusada: `arquivo_inexistente` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Administrador", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A reserva do Cliente Teste aparece com o nome do Administrador.

OBSERVAÇÃO ADICIONAL: tbusuarios: id 1 = admin/Administrador (sup), id 2 = 11122233344/Cliente Teste (cli).
```

## 3. Contraste com a segunda causa

nome_nulo_vindo_da_view e não campo_ausente: a escolha tem probabilidade 0,85 contra 0,08; verbete(s) na evidência: usuario-e-login, contrato-pedido, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nome_nulo_vindo_da_view | 0,85 | sim |
| campo_ausente | 0,08 |  |
| campo_renomeado | 0,08 |  |
| chave_de_juncao_errada | 0,03 |  |
| valor_fora_do_dominio | 0,02 |  |
| escala_ou_unidade_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[usuario-e-login]`; verbetes citados: `usuario-e-login`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `usuario-e-login` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `usuario-e-login` | confere | contexto: `usuario-e-login`, `contrato-pedido`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `nome_nulo_vindo_da_view` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[usuario-e-login]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["usuario-e-login"]} |
| fonte_contem_termo_da_causa | `usuario-e-login` | **não confere** | {"termo": "nome_nulo_vindo_da_view"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 342 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:36:41 | caso tra-2 |
| 343 | 2 | candidatos | programa | ao_vivo | 2026-11-03T21:36:41 | 3 de 40 verbetes entregues |
| 345 | 3 | prompt | programa | ao_vivo | 2026-11-03T21:36:41 | {"chars": 3267, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "c9f8fadf49d2", "sha": "c9f8fadf49d2fd01"} |
| 347 | 4 | inferencia | programa | ao_vivo | 2026-11-03T21:36:41 | diagnostico: 64,5 s |
| 348 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T21:36:41 | causa_raiz: `nome_nulo_vindo_da_view` |
| 349 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T21:36:41 | campo: `nome` |
| 350 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T21:36:41 | impacto: `O usuário vê o nome do administrador em vez do seu próprio nome na reserva.` |
| 351 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T21:36:41 | fonte: `[usuario-e-login]` |
| 352 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T21:36:41 | fonte_citada: `usuario-e-login` |
| 353 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T21:36:41 | quatro_linhas_presentes: confere |
| 354 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T21:36:41 | rotulo_no_conjunto: nao_confere |
| 355 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T21:36:41 | fonte_existe_na_biblioteca: confere |
| 356 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T21:36:41 | fonte_estava_no_contexto: confere |
| 357 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T21:36:41 | campo_existe_no_caso: confere |
| 358 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T21:36:41 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 359 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T21:36:41 | notas_nos_verbetes_citados: informativo |
| 360 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T21:36:41 | impacto: nao_verificavel |
| 361 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T21:36:41 | fonte_formato_valido: confere |
| 362 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T21:36:41 | fonte_contem_termo_da_causa: nao_confere |
| 363 | 20 | decisao | programa | ao_vivo | 2026-11-03T21:36:41 | diagnostico: escolha nome_nulo_vindo_da_view; divergência sim |
| 366 | 21 | inferencia | programa | ao_vivo | 2026-11-03T21:37:50 | proposta: 149,2 s |
| 368 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:37:50 | proposta 1: retificacao em [chave_de_juncao_errada]: recusada: arquivo_inexistente |
| 369 | 23 | decisao | programa | ao_vivo | 2026-11-03T21:37:50 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 363, `diagnostico`: escolha `nome_nulo_vindo_da_view`; resultado rotulo_emitido; evidência: evento 343 (verbete_entregue, usuario-e-login), evento 343 (verbete_entregue, contrato-pedido), evento 343 (verbete_entregue, pedido-reserva), evento 347 (resposta), evento 352 (verbete_citado, usuario-e-login); divergência: sim; falha: rotulo_fora_da_taxonomia; prov.used: usuario-e-login, contrato-pedido, pedido-reserva (gen_ai: chat)
- evento 369, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 347 (resposta), evento 366 (resposta), evento 368 (verbete_entregue, chave_de_juncao_errada); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: chave_de_juncao_errada, contrato-pedido, pedido-reserva, usuario-e-login

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 342 a 369 da trilha; hash dos eventos deste caso: `d860879c2b66a48c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
