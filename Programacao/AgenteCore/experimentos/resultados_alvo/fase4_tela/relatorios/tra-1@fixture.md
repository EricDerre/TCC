<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-1@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê preços cem vezes maiores do que o esperado, como 'R$ 8.990,00' para a picanha.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque os verbetes entidade-produto, escala_ou_unidade_errada, contrato-produto estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 8990, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: Os precos aparecem cem vezes maiores: 'R$ 8.990,00' para a picanha.

OBSERVAÇÃO ADICIONAL: No banco, tbprodutos.valor_produto do id 1 vale 89.90.
```

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: entidade-produto, escala_ou_unidade_errada, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,99 | sim |
| valor_fora_do_dominio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[escala_ou_unidade_errada]`; verbetes citados: `escala_ou_unidade_errada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `escala_ou_unidade_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `escala_ou_unidade_errada` | confere | contexto: `entidade-produto`, `escala_ou_unidade_errada`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto`, `escala_ou_unidade_errada` |
| fonte_formato_valido | `[escala_ou_unidade_errada]` | confere | {"ids": ["escala_ou_unidade_errada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `escala_ou_unidade_errada` | confere | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-1 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 364 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:23:54 | caso tra-1 |
| 365 | 2 | candidatos | programa | ao_vivo | 2026-11-01T11:23:54 | 3 de 40 verbetes entregues |
| 367 | 3 | prompt | programa | ao_vivo | 2026-11-01T11:23:54 | {"etapa": "diagnostico", "sha": "d3ee8627b360f3f2", "prompt_sha256": "d3ee8627b360", "chars": 3896, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 369 | 4 | inferencia | programa | ao_vivo | 2026-11-01T11:23:54 | diagnostico: 68,6 s |
| 370 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T11:23:54 | causa_raiz: `escala_ou_unidade_errada` |
| 371 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T11:23:54 | campo: `preco` |
| 372 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T11:23:54 | impacto: `O usuário vê preços cem vezes maiores do que o esperado, como 'R$ 8.990,00' para a picanha.` |
| 373 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T11:23:54 | fonte: `[escala_ou_unidade_errada]` |
| 374 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T11:23:54 | fonte_citada: `escala_ou_unidade_errada` |
| 375 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:23:54 | quatro_linhas_presentes: confere |
| 376 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T11:23:54 | rotulo_no_conjunto: confere |
| 377 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T11:23:54 | fonte_existe_na_biblioteca: confere |
| 378 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T11:23:54 | fonte_estava_no_contexto: confere |
| 379 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T11:23:54 | campo_existe_no_caso: confere |
| 380 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T11:23:54 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 381 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T11:23:54 | notas_nos_verbetes_citados: informativo |
| 382 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T11:23:54 | impacto: nao_verificavel |
| 383 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T11:23:54 | fonte_formato_valido: confere |
| 384 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T11:23:54 | fonte_contem_termo_da_causa: confere |
| 385 | 20 | decisao | programa | ao_vivo | 2026-11-01T11:23:54 | diagnostico: escolha escala_ou_unidade_errada; divergência não |

</details>

Nós de decisão:

- evento 385, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 365 (verbete_entregue, entidade-produto), evento 365 (verbete_entregue, escala_ou_unidade_errada), evento 365 (verbete_entregue, contrato-produto), evento 369 (resposta), evento 374 (verbete_citado, escala_ou_unidade_errada); divergência: não; falha: nenhuma; prov.used: entidade-produto, escala_ou_unidade_errada, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 364 a 385 da trilha; hash dos eventos deste caso: `0c392d8bbaaa6bcf`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
