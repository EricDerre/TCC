<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-26`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/tra-26@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id` · selo de probabilidade: **medio** (p = 0,92)

**IMPACTO (declarado):** `O usuário vê o conteúdo do produto vizinho ao clicar no "Saiba Mais...".`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id porque os verbetes entidade-produto, contrato-produto, ancora-saiba-mais estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,03. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 4, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 5, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}, {"id": 6, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}]

SINTOMA OBSERVADO: A grade aparece normal, mas cada 'Saiba Mais...' abre o produto vizinho: o botao do cartao da Fraldinha abre o modal da Costelona, o da Costelona abre o da Alcatra na Pedra e o da Alcatra na Pedra abre o da Maminha. O clique no cartao da Fraldinha disparou GET /api/produtos/4, que respondeu 200 com os dados da Costelona.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os cartoes da Fraldinha, da Costelona e da Alcatra na Pedra; a lista completa tem 14.
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não campo_ausente: a escolha tem probabilidade 0,92 contra 0,03; verbete(s) na evidência: entidade-produto, contrato-produto, ancora-saiba-mais

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,92 | sim |
| campo_ausente | 0,03 |  |
| campo_renomeado | 0,03 |  |
| resposta_truncada | 0,03 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| tipo_divergente | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `ancora-saiba-mais` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids tra-26 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1274 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:15:59 | caso tra-26 |
| 1275 | 2 | candidatos | programa | ao_vivo | 2026-11-06T12:15:59 | 3 de 39 verbetes entregues |
| 1277 | 3 | prompt | programa | ao_vivo | 2026-11-06T12:15:59 | {"etapa": "diagnostico", "sha": "35d49244e83aa9d1", "prompt_sha256": "35d49244e83a", "chars": 4117, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1279 | 4 | inferencia | programa | ao_vivo | 2026-11-06T12:15:59 | diagnostico: 63,5 s |
| 1280 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T12:15:59 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 1281 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T12:15:59 | campo: `id` |
| 1282 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T12:15:59 | impacto: `O usuário vê o conteúdo do produto vizinho ao clicar no "Saiba Mais...".` |
| 1283 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T12:15:59 | fonte: `[contrato-produto]` |
| 1284 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T12:15:59 | fonte_citada: `contrato-produto` |
| 1285 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T12:15:59 | quatro_linhas_presentes: confere |
| 1286 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:15:59 | rotulo_no_conjunto: confere |
| 1287 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:15:59 | fonte_existe_na_biblioteca: confere |
| 1288 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:15:59 | fonte_estava_no_contexto: confere |
| 1289 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T12:15:59 | campo_existe_no_caso: confere |
| 1290 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T12:15:59 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1291 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T12:15:59 | notas_nos_verbetes_citados: informativo |
| 1292 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:15:59 | impacto: nao_verificavel |
| 1293 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:15:59 | fonte_formato_valido: confere |
| 1294 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:15:59 | fonte_contem_termo_da_causa: nao_confere |
| 1295 | 20 | decisao | programa | ao_vivo | 2026-11-06T12:15:59 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 1295, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 1275 (verbete_entregue, entidade-produto), evento 1275 (verbete_entregue, contrato-produto), evento 1275 (verbete_entregue, ancora-saiba-mais), evento 1279 (resposta), evento 1284 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, ancora-saiba-mais (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1274 a 1295 da trilha; hash dos eventos deste caso: `9971bee5bb717535`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
