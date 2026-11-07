<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/run-21@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `registro_duplicado` · **CAMPO:** `id` · selo de probabilidade: **medio** (p = 0,91) · **CONFLITO**: nenhum verbete entregue trata da causa respondida registro_duplicado

**IMPACTO (declarado):** `O usuário vê a Picanha ao Alho listada duas vezes seguidas, causando redundância na exibição dos produtos.`

Justificativa (gerada por molde): O agente respondeu registro_duplicado no campo id porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,06. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

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

registro_duplicado e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,91 contra 0,06; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| registro_duplicado | 0,91 | sim |
| colecao_no_lugar_de_objeto | 0,06 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| recurso_inexistente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids run-21 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2192 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:55:13 | caso run-21 |
| 2193 | 2 | candidatos | programa | ao_vivo | 2026-11-05T19:55:13 | 3 de 39 verbetes entregues |
| 2195 | 3 | prompt | programa | ao_vivo | 2026-11-05T19:55:13 | {"etapa": "diagnostico", "sha": "569b1995a49e52d3", "prompt_sha256": "569b1995a49e", "chars": 4085, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2197 | 4 | inferencia | programa | ao_vivo | 2026-11-05T19:55:13 | diagnostico: 46,1 s |
| 2198 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T19:55:13 | causa_raiz: `registro_duplicado` |
| 2199 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T19:55:13 | campo: `id` |
| 2200 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T19:55:13 | impacto: `O usuário vê a Picanha ao Alho listada duas vezes seguidas, causando redundância na exibição dos produtos.` |
| 2201 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T19:55:13 | fonte: `[contrato-produto] [entidade-produto]` |
| 2202 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T19:55:13 | fonte_citada: `contrato-produto` |
| 2203 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T19:55:13 | fonte_citada: `entidade-produto` |
| 2204 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | quatro_linhas_presentes: confere |
| 2205 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | rotulo_no_conjunto: confere |
| 2206 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | fonte_existe_na_biblioteca: confere |
| 2207 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | fonte_existe_na_biblioteca: confere |
| 2208 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | fonte_estava_no_contexto: confere |
| 2209 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | fonte_estava_no_contexto: confere |
| 2210 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | campo_existe_no_caso: confere |
| 2211 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2212 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | notas_nos_verbetes_citados: informativo |
| 2213 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | impacto: nao_verificavel |
| 2214 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | fonte_formato_valido: confere |
| 2215 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | fonte_contem_termo_da_causa: nao_confere |
| 2216 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:55:13 | fonte_contem_termo_da_causa: nao_confere |
| 2217 | 24 | decisao | programa | ao_vivo | 2026-11-05T19:55:13 | diagnostico: escolha registro_duplicado; divergência sim |

</details>

Nós de decisão:

- evento 2217, `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido; evidência: evento 2193 (verbete_entregue, entidade-produto), evento 2193 (verbete_entregue, contrato-produto), evento 2193 (verbete_entregue, tipo_divergente), evento 2197 (resposta), evento 2202 (verbete_citado, contrato-produto), evento 2203 (verbete_citado, entidade-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2192 a 2217 da trilha; hash dos eventos deste caso: `4dbd4306ad15f74a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
