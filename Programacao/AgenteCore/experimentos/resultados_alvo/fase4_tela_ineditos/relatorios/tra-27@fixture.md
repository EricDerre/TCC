<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-27`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/tra-27@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,96)

**IMPACTO (declarado):** `O preço exibido no detalhe do produto difere do preço no cartão, causando confusão para o usuário.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque os verbetes entidade-produto, contrato-produto, pagina-produtos-api estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,03 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/2

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 8490.0, "imagem": "picanha_sem.jpg", "destaque": false}

SINTOMA OBSERVADO: O modal da Picanha Simples abre normal (ele so mostra nome e descricao), mas a conferencia de preco do roteiro falha: o preco do detalhe nao bate com o do cartao.

OBSERVAÇÃO ADICIONAL: A listagem GET /api/produtos, feita antes, trouxe este produto (id 2) com preco 84.9, e o cartao mostra 'R$ 84,90'.
```

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 0,96 contra 0,03; verbete(s) na evidência: entidade-produto, contrato-produto, pagina-produtos-api

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,96 | sim |
| valor_fora_do_dominio | 0,03 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [entidade-produto]`; verbetes citados: `contrato-produto`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `pagina-produtos-api` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `pagina-produtos-api` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto`, `pagina-produtos-api` |
| fonte_formato_valido | `[contrato-produto] [entidade-produto]` | confere | {"ids": ["contrato-produto", "entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids tra-27 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1341 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:18:17 | caso tra-27 |
| 1342 | 2 | candidatos | programa | ao_vivo | 2026-11-06T12:18:17 | 3 de 39 verbetes entregues |
| 1344 | 3 | prompt | programa | ao_vivo | 2026-11-06T12:18:17 | {"etapa": "diagnostico", "sha": "308e3ad66e290926", "prompt_sha256": "308e3ad66e29", "chars": 3626, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1346 | 4 | inferencia | programa | ao_vivo | 2026-11-06T12:18:17 | diagnostico: 55,7 s |
| 1347 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T12:18:17 | causa_raiz: `tipo_divergente` |
| 1348 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T12:18:17 | campo: `preco` |
| 1349 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T12:18:17 | impacto: `O preço exibido no detalhe do produto difere do preço no cartão, causando confusão para o usuário.` |
| 1350 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T12:18:17 | fonte: `[contrato-produto] [entidade-produto]` |
| 1351 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T12:18:17 | fonte_citada: `contrato-produto` |
| 1352 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T12:18:17 | fonte_citada: `entidade-produto` |
| 1353 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | quatro_linhas_presentes: confere |
| 1354 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | rotulo_no_conjunto: confere |
| 1355 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | fonte_existe_na_biblioteca: confere |
| 1356 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | fonte_existe_na_biblioteca: confere |
| 1357 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | fonte_estava_no_contexto: confere |
| 1358 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | fonte_estava_no_contexto: confere |
| 1359 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | campo_existe_no_caso: confere |
| 1360 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1361 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | notas_nos_verbetes_citados: informativo |
| 1362 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | impacto: nao_verificavel |
| 1363 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | fonte_formato_valido: confere |
| 1364 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | fonte_contem_termo_da_causa: nao_confere |
| 1365 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T12:18:17 | fonte_contem_termo_da_causa: nao_confere |
| 1366 | 24 | decisao | programa | ao_vivo | 2026-11-06T12:18:17 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1366, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1342 (verbete_entregue, entidade-produto), evento 1342 (verbete_entregue, contrato-produto), evento 1342 (verbete_entregue, pagina-produtos-api), evento 1346 (resposta), evento 1351 (verbete_citado, contrato-produto), evento 1352 (verbete_citado, entidade-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, pagina-produtos-api (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1341 a 1366 da trilha; hash dos eventos deste caso: `a5b19cd165fc1293`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
