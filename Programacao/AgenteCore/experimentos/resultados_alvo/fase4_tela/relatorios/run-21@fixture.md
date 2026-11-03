<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/run-21@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `registro_duplicado` · **CAMPO:** `id` · selo de probabilidade: **baixo** (p = 0,60) · **CONFLITO**: nenhum verbete entregue trata da causa respondida registro_duplicado

**IMPACTO (declarado):** `O usuário vê a Picanha ao Alho listada duas vezes seguidas, causando redundância na exibição dos produtos.`

Justificativa (gerada por molde): O agente respondeu registro_duplicado no campo id porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,36. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,60); trate como hipótese e confira o campo id antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}]

SINTOMA OBSERVADO: A Picanha ao Alho aparece duas vezes seguidas na grade de produtos, com exatamente os mesmos dados.

OBSERVAÇÃO ADICIONAL: tbprodutos.id_produto e chave primaria; nao tem como a linha existir duas vezes na tabela — a duplicata esta na consulta ou na montagem da resposta, nao no cadastro.
```

## 3. Contraste com a segunda causa

registro_duplicado e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,60 contra 0,36; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| registro_duplicado | 0,60 | sim |
| colecao_no_lugar_de_objeto | 0,36 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| tipo_divergente | 0,01 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| recurso_inexistente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [entidade-produto]`; verbetes citados: `contrato-produto`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto] [entidade-produto]` | confere | {"ids": ["contrato-produto", "entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "registro_duplicado"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "registro_duplicado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids run-21 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2251 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:32:51 | caso run-21 |
| 2252 | 2 | candidatos | programa | ao_vivo | 2026-11-01T12:32:51 | 3 de 40 verbetes entregues |
| 2254 | 3 | prompt | programa | ao_vivo | 2026-11-01T12:32:51 | {"etapa": "diagnostico", "sha": "c425f3276e69c029", "prompt_sha256": "c425f3276e69", "chars": 3927, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2256 | 4 | inferencia | programa | ao_vivo | 2026-11-01T12:32:51 | diagnostico: 59,1 s |
| 2257 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T12:32:51 | causa_raiz: `registro_duplicado` |
| 2258 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T12:32:51 | campo: `id` |
| 2259 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T12:32:51 | impacto: `O usuário vê a Picanha ao Alho listada duas vezes seguidas, causando redundância na exibição dos produtos.` |
| 2260 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T12:32:51 | fonte: `[contrato-produto] [entidade-produto]` |
| 2261 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T12:32:51 | fonte_citada: `contrato-produto` |
| 2262 | 10 | declaracao | modelo | ao_vivo | 2026-11-01T12:32:51 | fonte_citada: `entidade-produto` |
| 2263 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | quatro_linhas_presentes: confere |
| 2264 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | rotulo_no_conjunto: confere |
| 2265 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | fonte_existe_na_biblioteca: confere |
| 2266 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | fonte_existe_na_biblioteca: confere |
| 2267 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | fonte_estava_no_contexto: confere |
| 2268 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | fonte_estava_no_contexto: confere |
| 2269 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | campo_existe_no_caso: confere |
| 2270 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2271 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | notas_nos_verbetes_citados: informativo |
| 2272 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | impacto: nao_verificavel |
| 2273 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | fonte_formato_valido: confere |
| 2274 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | fonte_contem_termo_da_causa: nao_confere |
| 2275 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:32:51 | fonte_contem_termo_da_causa: nao_confere |
| 2276 | 24 | decisao | programa | ao_vivo | 2026-11-01T12:32:51 | diagnostico: escolha registro_duplicado; divergência sim |

</details>

Nós de decisão:

- evento 2276, `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido; evidência: evento 2252 (verbete_entregue, entidade-produto), evento 2252 (verbete_entregue, contrato-produto), evento 2252 (verbete_entregue, tipo_divergente), evento 2256 (resposta), evento 2261 (verbete_citado, contrato-produto), evento 2262 (verbete_citado, entidade-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2251 a 2276 da trilha; hash dos eventos deste caso: `189b1f781c1212ec`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
