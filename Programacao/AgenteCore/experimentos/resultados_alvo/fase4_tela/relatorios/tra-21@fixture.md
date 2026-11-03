<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-21@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,97)

**IMPACTO (declarado):** `O usuário vê uma lista incompleta de produtos, com um item ausente que deveria estar presente.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente porque os verbetes contagem_inconsistente, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
(13 itens retornados; falta o id 13, "Hamburguer Artesanal")

SINTOMA OBSERVADO: GET /api/produtos devolve 13 itens; o cadastro (tbprodutos) tem 14 produtos. O Hamburguer Artesanal (id 13) nao aparece em nenhuma pagina do site.

OBSERVAÇÃO ADICIONAL: tbprodutos tem 14 linhas cadastradas, ids 1 a 14 (seed.sql); nao existe coluna de exclusao logica em tbprodutos.
```

## 3. Contraste com a segunda causa

contagem_inconsistente e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,97 contra 0,00; verbete(s) na evidência: contagem_inconsistente, entidade-produto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,97 | sim |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-21 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2132 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:27:56 | caso tra-21 |
| 2133 | 2 | candidatos | programa | ao_vivo | 2026-11-01T12:27:56 | 3 de 40 verbetes entregues |
| 2135 | 3 | prompt | programa | ao_vivo | 2026-11-01T12:27:56 | {"etapa": "diagnostico", "sha": "9e83a057c99fa6ae", "prompt_sha256": "9e83a057c99f", "chars": 3523, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2137 | 4 | inferencia | programa | ao_vivo | 2026-11-01T12:27:56 | diagnostico: 49,6 s |
| 2138 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T12:27:56 | causa_raiz: `contagem_inconsistente` |
| 2139 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T12:27:56 | campo: `nenhum` |
| 2140 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T12:27:56 | impacto: `O usuário vê uma lista incompleta de produtos, com um item ausente que deveria estar presente.` |
| 2141 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T12:27:56 | fonte: `[contagem_inconsistente]` |
| 2142 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T12:27:56 | fonte_citada: `contagem_inconsistente` |
| 2143 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:56 | quatro_linhas_presentes: confere |
| 2144 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:56 | rotulo_no_conjunto: confere |
| 2145 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:56 | fonte_existe_na_biblioteca: confere |
| 2146 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:56 | fonte_estava_no_contexto: confere |
| 2147 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:56 | campo_existe_no_caso: nao_se_aplica |
| 2148 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:56 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2149 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:56 | notas_nos_verbetes_citados: informativo |
| 2150 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:56 | impacto: nao_verificavel |
| 2151 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:56 | fonte_formato_valido: confere |
| 2152 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:56 | fonte_contem_termo_da_causa: confere |
| 2153 | 20 | decisao | programa | ao_vivo | 2026-11-01T12:27:56 | diagnostico: escolha contagem_inconsistente; divergência não |

</details>

Nós de decisão:

- evento 2153, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 2133 (verbete_entregue, contagem_inconsistente), evento 2133 (verbete_entregue, entidade-produto), evento 2133 (verbete_entregue, contrato-produto), evento 2137 (resposta), evento 2142 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2132 a 2153 da trilha; hash dos eventos deste caso: `132b2b02ad4d49c5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
