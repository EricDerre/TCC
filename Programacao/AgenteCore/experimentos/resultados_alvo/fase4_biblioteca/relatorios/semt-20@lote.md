<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-20@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,46)

**IMPACTO (declarado):** `O usuário vê o preço como 'R$ -10,00', que é inválido para um preço.`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo preco porque os verbetes entidade-produto, contrato-produto, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,53. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,46); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": -10, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: O botao de preco da Picanha ao Alho mostra 'R$ -10,00'; o tipo do campo esta certo (numero), so o valor que nao faz sentido pra um preco.
```

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não tipo_divergente: a escolha tem probabilidade 0,46 contra 0,53; verbete(s) na evidência: entidade-produto, contrato-produto, nulo_inesperado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,53 |  |
| valor_fora_do_dominio | 0,46 | sim |
| escala_ou_unidade_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["entidade-produto", "contrato-produto"]} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "valor_fora_do_dominio"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2369 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:56:51 | caso semt-20 |
| 2370 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:56:51 | 3 de 46 verbetes entregues |
| 2372 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:56:51 | {"chars": 3429, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "7e7f576ac385", "sha": "7e7f576ac385b1bd"} |
| 2374 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:56:51 | diagnostico: 35,5 s |
| 2375 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:56:51 | causa_raiz: `valor_fora_do_dominio` |
| 2376 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:56:51 | campo: `preco` |
| 2377 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:56:51 | impacto: `O usuário vê o preço como 'R$ -10,00', que é inválido para um preço.` |
| 2378 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:56:51 | fonte: `[entidade-produto], [contrato-produto]` |
| 2379 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:56:51 | fonte_citada: `entidade-produto` |
| 2380 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T00:56:51 | fonte_citada: `contrato-produto` |
| 2381 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | quatro_linhas_presentes: confere |
| 2382 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | rotulo_no_conjunto: confere |
| 2383 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | fonte_existe_na_biblioteca: confere |
| 2384 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | fonte_existe_na_biblioteca: confere |
| 2385 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | fonte_estava_no_contexto: confere |
| 2386 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | fonte_estava_no_contexto: confere |
| 2387 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | campo_existe_no_caso: confere |
| 2388 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2389 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | notas_nos_verbetes_citados: informativo |
| 2390 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | impacto: nao_verificavel |
| 2391 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | fonte_formato_valido: confere |
| 2392 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | fonte_contem_termo_da_causa: nao_confere |
| 2393 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T00:56:51 | fonte_contem_termo_da_causa: nao_confere |
| 2394 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:56:51 | diagnostico: escolha valor_fora_do_dominio; divergência não |

</details>

Nós de decisão:

- evento 2394, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 2370 (verbete_entregue, entidade-produto), evento 2370 (verbete_entregue, contrato-produto), evento 2370 (verbete_entregue, nulo_inesperado), evento 2374 (resposta), evento 2379 (verbete_citado, entidade-produto), evento 2380 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2369 a 2394 da trilha; hash dos eventos deste caso: `ede7f7b8669eb85a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
